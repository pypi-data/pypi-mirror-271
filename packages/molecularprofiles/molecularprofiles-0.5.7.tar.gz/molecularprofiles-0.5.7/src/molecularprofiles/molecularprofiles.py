"""
This is a class that offers a set of functions to work with meteorological data
in ecsv or grib(2) format.

Created by Pere Munar-Adrover
email: pere.munaradrover@gmail.com
Further developed and mainted by
Mykhailo Dalchenko (mykhailo.dalchenko@unige.ch) and
Georgios Voutsinas (georgios.voutsinas@unige.ch)
"""

import os
import sys
import logging

import astropy.units as u
from astropy.table import Table, QTable, vstack, Column
import numpy as np
from scipy.interpolate import interp1d
from bisect import bisect_left

from molecularprofiles.utils.grib_utils import get_grib_file_data, extend_grib_data
from molecularprofiles.utils.constants import (
    DENSITY_SCALE_HEIGHT,
    N0_AIR,
    STD_GRAVITATIONAL_ACCELERATION,
    STD_AIR_DENSITY,
    STD_CORSIKA_ALTITUDE_PROFILE,
    RAYLEIGH_SCATTERING_ALTITUDE_BINS,
)

from molecularprofiles.utils.humidity import (
    compressibility,
    density_moist_air,
    molar_fraction_water_vapor,
    partial_pressure_water_vapor,
)
from molecularprofiles.utils.rayleigh import Rayleigh

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
log_config_file = f"{ROOTDIR}/utils/mdps_log.conf"
logging.config.fileConfig(fname=log_config_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MolecularProfile:
    """
    This class provides a series of functions to analyze the quality of the data for both
    CTA-North and CTA-South.

    Methods within this class:

    get_data:                   it retrieves the data from the input file. If the input file
                                is a grib file and there is no file in the working directory
                                with the same name but with .txt extension the program extracts
                                the data from the grib file through the grib_utils program. If
                                there is such a txt file, it reads it directly
    write_atmospheric_profile:  prints the data into a txt file which format is compliant with the input card
                                for the CORSIKA air shower simulation software
    create_mdp:                 creates an altitude profile of the molecular number density
    rayleigh_extinction:        creates a file, in format to be directly fed to simtel simulation, with the
                                extinction per altitude bin for wavelengths from 200 to 1000 nm
    """

    def __init__(self, data_file):
        """
        Constructor

        :param data_file: txt file containing the data (string)
        """

        self.data_file = data_file

    # =============================================================================================================
    # Private functions
    # =============================================================================================================
    def _interpolate_cubic(self, x_param, y_param, new_x_param):
        func = interp1d(x_param, y_param, kind="cubic", bounds_error=False)
        return func(new_x_param)

    def _compute_mass_density(self, air="moist", co2_concentration=415):
        """
        Computes regular and exponential mass density of air.

        Adds to data the following columns:
        - 'Xw': molar fraction of water vapor (0 if air is dry)
        - 'Compressibility'
        - 'Mass Density'
        - 'Exponential Mass Density'

        Parameters
        ----------
        air : str
            Type of air, can be 'moist' or 'dry'
        co2_concentration : float
            CO2 volume concentration in ppmv
        """

        if air == "moist":
            self.data["Xw"] = molar_fraction_water_vapor(
                self.data["Pressure"], self.data["Temperature"], self.data["Relative humidity"]
            )
        elif air == "dry":
            self.data["Xw"] = 0.0
        else:
            raise ValueError("Wrong air condition. It must be 'moist' or 'dry'.")

        self.data["Compressibility"] = compressibility(
            self.data["Pressure"], self.data["Temperature"], self.data["Xw"]
        )
        self.data["Mass Density"] = density_moist_air(
            self.data["Pressure"],
            self.data["Temperature"],
            self.data["Compressibility"],
            self.data["Xw"],
            co2_concentration,
        )
        self.data["Exponential Mass Density"] = (
            self.data["Mass Density"] / STD_AIR_DENSITY
        ).decompose() * np.exp((self.data["Altitude"] / DENSITY_SCALE_HEIGHT).decompose())

    # =============================================================================================================
    # Main get data function
    # =============================================================================================================
    def get_data(self):
        """
        Reads ECMWF or GDAS data in ecsv or grib(2) format
        and computes statistical description of the data
        """
        file_ext = os.path.splitext(self.data_file)[1]
        if file_ext == ".grib" or file_ext == ".grib2":
            self.data = get_grib_file_data(self.data_file)
            self.data = extend_grib_data(self.data)
        elif file_ext == ".ecsv":
            self.data = Table.read(self.data_file)
        else:
            raise NotImplementedError(
                f"Only grib (1,2) and ecsv formats are supported at the moment. Requested format: {file_ext}"
            )
        self.stat_columns = [
            "Pressure",
            "Altitude",
            "Density",
            "Temperature",
            "Wind Speed",
            "Wind Direction",
            "Relative humidity",
            "Exponential Density",
        ]
        self.stat_data = self.data[self.stat_columns].group_by("Pressure")
        self.stat_description = {
            "avg": self.stat_data.groups.aggregate(np.mean),
            "std": self.stat_data.groups.aggregate(np.std),
            "mad": self.stat_data.groups.aggregate(lambda x: np.mean(np.absolute(x - np.mean(x)))),
            "p2p_max": self.stat_data.groups.aggregate(lambda x: np.max(x) - np.mean(x)),
            "p2p_min": self.stat_data.groups.aggregate(lambda x: np.mean(x) - np.min(x)),
        }

    def _refractive_index(self, P, T, RH, wavelength, C):
        """Wrapper for Rayleigh.calculate_n()."""
        rayleigh = Rayleigh(wavelength, C, P, T, RH)
        return rayleigh.refractive_index

    def _take_closest(self, my_list, my_number):
        """
        Returns closest value to my_number.
        If two numbers are equally close, return the smallest number.
        This function comes from the answer of user:
        https://stackoverflow.com/users/566644/lauritz-v-thaulow
        found in stack overflow post:
        https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value/12141511#12141511
        """
        pos = bisect_left(my_list, my_number)
        if pos == 0:
            return my_list[0]
        if pos == len(my_list):
            return my_list[-1]
        before = my_list[pos - 1]
        after = my_list[pos]
        if after - my_number < my_number - before:
            return after
        return before

    def _get_data_altitude_range(self, altitude_profile):
        """
        Calculates the floor and ceiling of the available DAS data.

        Parameters:
        -----------
        altitude_profile : Quantity
            Tuple with the altitudes that the atmospheric parameters will be calculated. Units of length.
        Returns:
        --------
            floor, ceiling : Quantities that define the highest and lowest altitude that DAS data are available.
        """

        floor = self._take_closest(
            altitude_profile,
            (
                (self.stat_description["avg"]["Altitude"][-1])
                * (self.stat_description["avg"]["Altitude"].unit)
            ).to(altitude_profile.unit),
        )
        ceiling = self._take_closest(
            altitude_profile,
            (
                (self.stat_description["avg"]["Altitude"][0])
                * (self.stat_description["avg"]["Altitude"].unit)
            ).to(altitude_profile.unit),
        )
        return floor, ceiling

    def _create_profile(self, interpolation_centers):
        """Interpolates atmospheric parameters in the requested interpolation centers"""

        temperature = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"].to(u.km),
                self.stat_description["avg"]["Temperature"],
                interpolation_centers.to(u.km),
            )
            * self.stat_description["avg"]["Temperature"].unit
        )
        relative_humidity = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"].to(u.km),
                self.stat_description["avg"]["Relative humidity"],
                interpolation_centers.to(u.km),
            )
            * self.stat_description["avg"]["Relative humidity"].unit
        )
        pressure = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"].to(u.km),
                self.stat_description["avg"]["Pressure"],
                interpolation_centers.to(u.km),
            )
            * self.stat_description["avg"]["Pressure"].unit
        )
        density = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"].to(u.km),
                self.stat_description["avg"]["Density"],
                interpolation_centers.to(u.km),
            )
            * self.stat_description["avg"]["Density"].unit
            / N0_AIR
        )
        return temperature, relative_humidity, pressure, density

    def _pick_up_reference_atmosphere(self, ceiling, floor, reference_atmosphere):
        """
        Picks up the reference atmosphere corresponding to the season and
        the geographical location. It selects all rows above the given ceiling.

        Parameters:
        -----------
        ceiling
            Astropy quantity expressing the ceiling of the DAS data.
        reference_atmosphere
            ecsv file with the reference atmosphere profile.

        Returns:
        --------
        table
            Astropy table with the atmospheric profile above the given ceiling.
        """
        try:
            reference_atmosphere_table = Table.read(reference_atmosphere)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
            sys.exit(1)
        try:
            mask = (
                reference_atmosphere_table["altitude"]
                >= ceiling.to(reference_atmosphere_table["altitude"].unit)
            ) | (
                reference_atmosphere_table["altitude"]
                <= floor.to(reference_atmosphere_table["altitude"].unit)
            )
            return reference_atmosphere_table[mask]
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
            sys.exit(1)

    # =======================================================================================================
    # printing functions:
    # =======================================================================================================

    def write_atmospheric_profile(
        self,
        outfile,
        co2_concentration,
        floor=None,
        reference_atmosphere=None,
        altitude_list=STD_CORSIKA_ALTITUDE_PROFILE,
    ):
        """
        Write an output file in the style of a CORSIKA atmospheric configuration file:
        altitude (km)     density (g/cm^3)   thickness (g/cm^2)   refractive index -1   temperature (K)   pressure (hPA)   partial water pressure

        Parameters:
        -----------
        outfile : string
            Name of the returned file.
        co2_concentration : float
            12MACOBAC value
        floor : Quantity
            Lowest altitude level where the atmospheric parameters will be calculated. If none is provided, it gets the closer to the sea level altitude where data are available. Units of length.
        reference_atmosphere : path
            The path where the file with the reference atmosphere model is located.
        altitude_list : Quantity
            Tuple with the altitudes that the atmospheric parameters will be calculated. Units of length.

        Returns:
        --------
            Ecsv file in the style of a CORSIKA atmospheric configuration file.
        """

        floor, ceiling = self._get_data_altitude_range(
            altitude_list.to(self.stat_description["avg"]["Altitude"].unit)
        )
        altitude = altitude_list[
            (altitude_list.to_value() > floor.to_value(altitude_list.unit))
            & (altitude_list.to_value() < ceiling.to_value(altitude_list.unit))
        ]
        altitude = altitude.to(self.stat_description["avg"]["Altitude"].unit)
        temperature, relative_humidity, pressure, density = self._create_profile(altitude)
        thickness = pressure / STD_GRAVITATIONAL_ACCELERATION
        rel_water_vapor_pressure = (
            partial_pressure_water_vapor(temperature, relative_humidity) / pressure
        ).decompose()
        rel_refractive_index = (
            self._refractive_index(
                pressure, temperature, relative_humidity, 350.0 * u.nm, co2_concentration
            )
            - 1.0
        )

        corsika_input_table = Table()
        tables = []

        for i in np.arange(len(altitude)):
            outdict = {
                "altitude": altitude[i].to(u.km),
                "atmospheric_density": density[i].to(u.g / u.cm**3),
                "atmospheric_thickness": thickness[i].decompose().to(u.g / u.cm**2),
                "refractive_index_m_1": rel_refractive_index[i],
                "temperature": temperature[i],
                "pressure": pressure[i],
                "partial_water_pressure": rel_water_vapor_pressure[i],
            }
            tables.append(outdict)
        # Merge ECMWF profile with upper atmospheric profile
        if reference_atmosphere:
            reference_atmosphere_table = self._pick_up_reference_atmosphere(
                ceiling, floor, reference_atmosphere
            )
            tables.append(reference_atmosphere_table)
        else:
            logger.info(
                "Since reference atmosphere was not provided, the resulting atmospheric model will be constrained to the extent of the provided meteorological data."
            )
        corsika_input_table = vstack(tables)
        corsika_input_table.sort("altitude")
        corsika_input_table.write(outfile, overwrite=True)

    def create_mdp(self, mdp_file):
        """
        Write an output file with the molecular number density per altitude
        """

        altitudes = np.arange(0.0, 20000.0, 1000) * u.m
        altitudes = altitudes.to(self.stat_description["avg"]["Altitude"].unit)
        number_density = (
            self._interpolate_cubic(
                self.stat_description["avg"]["Altitude"],
                self.stat_description["avg"]["Density"],
                altitudes,
            )
            * self.stat_description["avg"]["Density"].unit
        )
        t = Table([altitudes, number_density], names=["altitude", "number density"])
        try:
            t.write(mdp_file, overwrite=True)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.error(message)
            sys.exit(1)

    def rayleigh_extinction(
        self,
        rayleigh_extinction_file,
        co2_concentration,
        wavelength_min=200 * u.nm,
        wavelength_max=700 * u.nm,
        reference_atmosphere=None,
        rayleigh_scattering_altitude_bins=RAYLEIGH_SCATTERING_ALTITUDE_BINS,
    ):
        """
        Calculates the absolute integral optical depth due to Rayleigh scattering
        per altitude bins as a function of wavelength.
        The optical depth (AOD) for an altitude h over the observatory will be given by
        the integral of the monochromatic volume coefficient beta, with integration limits
        h_obs up to h.

        Parameters:
        -----------
        rayleigh_extinction_file : string
            Name of the returned file with the extinction profile.
        co2_concentration : float
            12MACOBAC value
        wavelength_min : Quantity
        wavelength_max : Quantity
        reference_atmosphere : path
            The path where the file with the reference atmosphere model is located.
        rayleigh_scattering_altitude_bins : Quantity
            Tuple with the altitudes that the AOD will be calculated. Units of length.

        Returns:
        --------
            Ecsv file with absolute optical depth per altitude bin per wavelength bin. The data model is the same with MODTRAN files.
        """

        floor, ceiling = self._get_data_altitude_range(rayleigh_scattering_altitude_bins)
        altitude = rayleigh_scattering_altitude_bins.to(u.km)
        altitude = altitude[altitude < ceiling]

        interpolation_centers = (altitude[:-1] + altitude[1:]) / 2
        (
            temperature_lower,
            relative_humidity_lower,
            pressure_lower,
            density_lower,
        ) = self._create_profile(interpolation_centers)

        # Concatenate with reference atmosphere
        if reference_atmosphere:
            reference_atmosphere_table = self._pick_up_reference_atmosphere(
                ceiling, floor, reference_atmosphere
            )
            length_of_columns = len(reference_atmosphere_table)
            relative_humidity_upper = (
                np.zeros(length_of_columns) * self.stat_description["avg"]["Relative humidity"].unit
            )
            try:
                relative_humidity = np.concatenate(
                    (relative_humidity_lower, relative_humidity_upper)
                )
                pressure = np.concatenate((pressure_lower, reference_atmosphere_table["pressure"]))
                temperature = np.concatenate(
                    (temperature_lower, reference_atmosphere_table["temperature"])
                )
                altitude = np.concatenate((altitude, reference_atmosphere_table["altitude"]))
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logger.error(message)
        else:
            logger.info(
                "Since the reference atmosphere was not provided, the resulting atmospheric model will be constrained to the extent of the provided meteorological data."
            )
            temperature = temperature_lower
            pressure = pressure_lower
            relative_humidity = relative_humidity_lower

        t = QTable(
            [altitude[1:], pressure, temperature, relative_humidity],
            names=("altitude", "pressure", "temperature", "relative_humidity"),
        )
        t.sort("altitude")
        bin_widths = np.diff(np.sort(altitude))
        t["bin_widths"] = bin_widths
        mask = t["altitude"] > floor
        wavelength_range = (
            np.arange(wavelength_min.to_value(u.nm), wavelength_max.to_value(u.nm), 1) * u.nm
        )
        aod_units = len(wavelength_range) * [u.dimensionless_unscaled]
        rayleigh_extinction_table = Table(names=wavelength_range, units=aod_units)
        col_alt_max = Column(name="altitude_max", unit=u.km)
        col_alt_min = Column(name="altitude_min", unit=u.km)
        rayleigh_extinction_table.add_columns([col_alt_max, col_alt_min], indexes=[0, 0])
        aod_dict = {
            aod: 0
            for aod in np.arange(wavelength_min.to_value(u.nm), wavelength_max.to_value(u.nm))
        }
        for row in t[mask]:
            new_row = []
            new_row.append(row["altitude"])
            new_row.append(row["altitude"] - row["bin_widths"])
            for wavelength in wavelength_range:
                rayleigh = Rayleigh(
                    wavelength,
                    co2_concentration,
                    row["pressure"],
                    row["temperature"],
                    row["relative_humidity"],
                )
                beta = rayleigh.beta
                aod = row["bin_widths"] * beta
                aod_dict[wavelength.to_value(u.nm)] += aod
                new_row.append(aod_dict[wavelength.to_value(u.nm)])
            rayleigh_extinction_table.add_row(new_row)
        rayleigh_extinction_table.write(rayleigh_extinction_file, overwrite=True)
        return rayleigh_extinction_file

    def convert_to_simtel_compatible(self, input_ecsv_file, output_file, observation_altitude):
        """
        Converts an ecsv file of an extinction profile to a format digestible by sim_telarray.
        Parameters:
        -----------
        input_ecsv_file : string
            Name of the input extinction profile file in ecsv format.
        output_file : string
            Name of the output extinction profile file in simtel digestible format.
        observation_altitude : quantity
            Starting altitude measured from sea level.
        """
        extinction_table = QTable.read(input_ecsv_file)
        with open(output_file, "w") as f:
            H2 = observation_altitude.to_value(u.km)
            H1 = extinction_table["altitude_max"].to_value(u.km)
            list_of_altitude_bins = f"# H2= {H2:.3f}, H1= "
            for height in H1:
                list_of_altitude_bins += f"{height:.3f}\t"
            list_of_altitude_bins += "\n"
            f.writelines(list_of_altitude_bins)
            for wl in extinction_table.columns:
                if wl not in ("altitude_max", "altitude_min"):
                    file_line = [str(wl).split(" ")[0], "\t"]
                    for aod in extinction_table[wl]:
                        file_line += [f"{aod:.6f}", "\t"]
                    file_line += ["\n"]
                    f.writelines(file_line)

    def timeseries_analysis(self, outfile, altitude_list=STD_CORSIKA_ALTITUDE_PROFILE):
        """
        Analyses timeseries of meteorological data.
        It produces an astropy table with the scaled exponential density at 15km a.s.l. as a function of the MJD.
        This timeseries is used for the identification of seasons.
        outfile : string
            Name of the produced file where the table is stored.
        altitude_list : Quantity
            Tuple with the altitudes that the atmospheric parameters will be calculated. Units of length.
        """

        output_table = QTable()
        tables = []
        floor = 1 * u.km
        ceiling = 20 * u.km
        altitude = altitude_list[
            (altitude_list.to_value() >= floor.to_value(altitude_list.unit))
            & (altitude_list.to_value() < ceiling.to_value(altitude_list.unit))
        ]

        self.data["MJD"] = self.data["Timestamp"].mjd
        test_table = self.data.group_by("MJD")
        indices = test_table.groups.indices
        for first, second in zip(indices, indices[1:]):
            t = test_table[first:second]
            n_exp = (
                self._interpolate_cubic(
                    t["Altitude"],
                    t["Exponential Density"],
                    altitude,
                )
                * u.dimensionless_unscaled
            )
            current_table = QTable([n_exp, altitude], names=("n_exp", "altitude"))
            current_table["mjd"] = t["MJD"][1]
            mask = current_table["altitude"] == 15000 * u.m
            tables.append(current_table[mask])
        output_table = vstack(tables)
        output_table.write(outfile, overwrite=True)
