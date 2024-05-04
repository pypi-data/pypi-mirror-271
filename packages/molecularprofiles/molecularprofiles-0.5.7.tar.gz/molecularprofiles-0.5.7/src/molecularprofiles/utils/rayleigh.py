import functools
import numpy as np
import astropy.units as u
from molecularprofiles.utils import humidity
from molecularprofiles.utils.constants import (
    STD_NUMBER_DENSITY,
    STD_AIR_PRESSURE,
    STD_AIR_TEMPERATURE,
    STD_RELATIVE_HUMIDITY,
    NITROGEN_RATIO,
    OXYGEN_RATIO,
    ARGON_RATIO,
    GAS_CONSTANT,
)


class Rayleigh:
    """
    A small Rayleigh-scattering program based on:
    C. Tomasi, V. Vitale, B. Petkov, A. Lupi, A. Cacciari
    "Improved algorithm for calculations of Rayleigh-scattering optical
    depth in standard atmospheres"
    Applied Optics 44 Nr. 16 (2005) 3320

    The calculation of refractive index is based on:
    P.E. Ciddor, "Refractive index of air: new equations for hte visible and near infrared",
    Applied Optics 35 (1996) 1566

    P.E. Ciddor, "Refractive index of air: 3. The roles of CO2, H20 and refractivity virals",
    Applied Optics 41 (2002) 2292

    The principal King factor formula is based on:
    D.R. Bates, "Rayleigh scattering by air",
    Planet. Space Sci. 32 (1984) 785

    B.A. Bodhaine, N.B. Wood, E.G. Dutton, J.R. Slusser, "On Rayleigh optical depth calculations",
    J. Atmosph. Osceanic Technol. 16 (1999) 1854

    The calculation of the Chandrasekhar phase function is based on:
    S. Chandrasekhar, Radiative Transfer, Dover Publications, 1960.

    E.J. McCartney, "Optics of the Atmosphere. Scattering by Molecules and Particles"
    Wiley & Sons, New York, 1977.

    Adapted from MRayleigh, written by Markus Gaug <markus.gaug@uab.cat>, 04/2013
    .. moduleauthor:: Scott Griffiths <sgriffiths@ifae.es>
    """

    def __init__(
        self,
        wavelength,
        co2_bkg,
        pressure=STD_AIR_PRESSURE,
        temperature=STD_AIR_TEMPERATURE,
        relative_humidity=STD_RELATIVE_HUMIDITY,
    ):
        """
        Constructor for Rayleigh-scattering class.

        Parameters
        ----------
        wavelength : astropy.units.Quantity
            Wavelength of light.
        co2_bkg : float
            CO2 concentration [ppmv]
        pressure : astropy.units.Quantity
            Atmospheric pressure
        temperature : astropy.units.Quantity
            Air temperature
        relative_humidity : astropy.units.Quantity
            Relative humidity [%]
        """
        # check inputs for bad values
        if np.any(wavelength < 200 * u.nm) or np.any(wavelength > 4000 * u.nm):
            raise ValueError("Wavelength range only from 200 nm - 4 micrometer allowed.")
        if np.any(pressure < 0 * u.hPa) or np.any(pressure > 1400 * u.hPa):
            raise ValueError("Pressure only in range 0 - 1400 hPa allowed.")
        if np.any(temperature < 150 * u.K) or np.any(temperature > 400 * u.K):
            raise ValueError("Temperatures only in range 150 - 400 K allowed.")
        # if np.any(relative_humidity < 0) or np.any(relative_humidity > 100 * u.percent):
        #    raise ValueError("Relative humity must lie between 0 - 100.")
        # FIXME: Relative humidity can exceed 100%, in case of supersaturated air.
        # The maximum limit should be thought better. However relative humidity cannot go negative.
        # If we receive negative values it is most probably due to interpolation problems.
        # Till we fix these issues it is better to comment out the minimum limit.
        if co2_bkg < 200 or co2_bkg > 1000:
            raise ValueError("CO2 concentrations only in range 200 - 1000 ppmv allowed.")

        self.wavelength = wavelength.to(u.nm)
        self.pressure = pressure.to(u.hPa)
        self.temperature = temperature.to(u.K, equivalencies=u.temperature())
        self.relative_humidity = relative_humidity.to(u.percent)
        self.co2_bkg = co2_bkg  # [ppmv]  CO2 concentration of air

    @functools.cached_property
    def molecular_number_density(self):
        """
        Returns
        -------
        astropy.units.Quantity
            Molecular number density [cm^-3]

        Notes
        -----
        See Eq. 3 in [1]_.

        References
        ----------
        .. [1] C. Tomasi, V. Vitale, B. Petkov, A. Lupi, A. Cacciari
           "Improved algorithm for calculations of Rayleigh-scattering optical depth
           in standard atmospheres", Applied Optics 44 Nr. 16 (2005) 3320
        """
        return (
            (
                STD_NUMBER_DENSITY
                * self.pressure
                / STD_AIR_PRESSURE
                * STD_AIR_TEMPERATURE
                / self.temperature
            )
            .decompose()
            .to(1 / u.cm**3)
        )

    @functools.cached_property
    def scattering_cross_section(self):
        """
        Returns
        -------
        astropy.units.Quantity
            Total Rayleigh scattering cross section per molecule [cm^2].

        Notes
        -----
        See Eq. 4 in [1]_.

        References
        ----------
        .. [1] C. Tomasi, V. Vitale, B. Petkov, A. Lupi, A. Cacciari
           "Improved algorithm for calculations of Rayleigh-scattering optical depth
           in standard atmospheres", Applied Optics 44 Nr. 16 (2005) 3320
        """
        return (
            (
                24
                * np.pi**3
                * (self.refractive_index**2 - 1) ** 2
                / (
                    self.wavelength**4
                    * self.molecular_number_density**2
                    * (self.refractive_index**2 + 2) ** 2
                )
                * self.king_factor
            )
            .decompose()
            .to(u.cm**2)
        )

    @functools.cached_property
    def beta(self):
        """
        Calculates the monochromatic volume coefficient for the total molecular
        scattering in cloudless air, beta.

        Returns
        -------
        astropy.units.Quantity
            Monochromatic volume coefficient for the total molecular scattering
            in cloudless air [1/km]

        Notes
        -----
        See Eq. 2 in [1]_.

        References
        ----------
        .. [1] C. Tomasi, V. Vitale, B. Petkov, A. Lupi, A. Cacciari
           "Improved algorithm for calculations of Rayleigh-scattering optical depth
           in standard atmospheres", Applied Optics 44 Nr. 16 (2005) 3320
        """
        return (
            (self.molecular_number_density * self.scattering_cross_section).decompose().to(1 / u.km)
        )

    @functools.cached_property
    def refractive_index(self):
        """
        Ciddor formula for calculation of refractive index in moist air.
        The obtained refractive index is precise to 1e-7.

        Returns
        -------
        float
            Index of refraction of moist air

        Notes
        -----
        Cross-checked with:
        http://emtoolbox.nist.gov/Wavelength/Documentation.asp#IndexofRefractionofAir
        """
        refractive_index_dry = (
            1e-8
            * (
                5792105 / (238.0185 - 1 / self.wavelength.to_value(u.micron) ** 2)
                + 167917 / (57.362 - 1 / self.wavelength.to_value(u.micron) ** 2)
            )
            + 1
        )  # Tomasi eq. 17

        # refractive index of dry air at standard p and T, for given C (e = 0)
        refractive_index_dry_std_air = (1 + 0.534e-6 * (self.co2_bkg - 450)) * (
            refractive_index_dry - 1
        ) + 1  # Tomasi eq. 18

        # refractive index of pure water vapor at standard T and e
        # (T* = 293.15 K = 20 C, and e* = 1333 Pa)
        refractive_index_water_vapour = (
            1.022e-8
            * (
                295.235
                + 2.6422 / self.wavelength.to_value(u.micron) ** 2
                - 0.032380 / self.wavelength.to_value(u.micron) ** 4
                + 0.004028 / self.wavelength.to_value(u.micron) ** 6
            )
            + 1
        )  # Tomasi eq. 19

        # calculate the respective densities (see Tomasi et al., pp. 3325 ff)
        molar_mass_dry_air = (
            1e-3 * (28.9635 + 12.011e-6 * (self.co2_bkg - 400)) * u.kg / u.mol
        )  # Tomasi eq. 13
        molar_mass_water_vapour = 0.018015 * u.kg / u.mol
        molar_fraction_water_vapour = humidity.molar_fraction_water_vapor(
            self.pressure, self.temperature, self.relative_humidity
        )  # molar fraction of water vapor in moist air
        compressibility_dry_air = humidity.compressibility(
            STD_AIR_PRESSURE, STD_AIR_TEMPERATURE, 0
        )  # compressibility of dry air
        compressibility_water_vapour = humidity.compressibility(
            1333 * u.Pa, 293.15 * u.K, 1
        )  # compressibility of pure water vapor
        compressibility_moist_air = humidity.compressibility(
            self.pressure, self.temperature, molar_fraction_water_vapour
        )  # compressibility of moist air

        # density of dry air at standard p and T
        dry_air_density_stdpt = humidity.density_moist_air(
            STD_AIR_PRESSURE, STD_AIR_TEMPERATURE, compressibility_dry_air, 0, self.co2_bkg
        )

        # density of pure water vapor at at standard T and e (T* = 293.15 K = 20 C, and e* = 1333 Pa)
        water_vapour_density_stdpt = humidity.density_moist_air(
            1333 * u.Pa, 293.15 * u.K, compressibility_water_vapour, 1, self.co2_bkg
        )

        # density of the dry component of moist air
        density_dry_comp_moist_air = (
            self.pressure
            * molar_mass_dry_air
            * (1 - molar_fraction_water_vapour)
            / (compressibility_moist_air * GAS_CONSTANT * self.temperature)
        ).decompose()

        # density of the water vapor component of moist air
        density_water_vapour_moist_air = (
            self.pressure
            * molar_mass_water_vapour
            * molar_fraction_water_vapour
            / (compressibility_moist_air * GAS_CONSTANT * self.temperature)
        ).decompose()

        return (
            1
            + (density_dry_comp_moist_air / dry_air_density_stdpt)
            * (refractive_index_dry_std_air - 1)
            + (density_water_vapour_moist_air / water_vapour_density_stdpt)
            * (refractive_index_water_vapour - 1)
        )  # Ciddor eq. 5, Tomasi eq. 11

    @functools.cached_property
    def king_factor(self):
        """
        Calculates the current best estimate of the King factor of moist air.

        Returns
        -------
        float
            King factor [dimensionless]

        Notes
        -----
        The King factor is used to take into account effects due to the anisotropic
        properties of air molecules since anisotropic molecules scatter more radiation
        at 90 degrees scattering angles than isotropic molecules with the same index
        of refraction.

        Precision not stated in Tomasi et al., but probably better than 1e-4.
        Effects of relative_humidity are of the order of several times 1e-4.
        """
        water_vapour_partial_pressure = humidity.partial_pressure_water_vapor(
            self.temperature, self.relative_humidity
        )  # water vapor partial pressure [hPa]

        king_factor_n2 = (
            1.034 + 3.17e-4 / self.wavelength.to_value(u.micron) ** 2
        )  # partial King factor for N2 molecules
        king_factor_o2 = (
            1.096
            + 1.385e-3 / self.wavelength.to_value(u.micron) ** 2
            + 1.448e-4 / self.wavelength.to_value(u.micron) ** 4
        )  # partial King factor for O2 molecules
        king_factor_ar = 1.00  # partial King factor for Ar molecules
        king_factor_co2 = 1.15  # partial King factor for CO2 molecules
        king_factor_wv = 1.001  # partial King factor for water vapor

        co2_ratio = 1e-6 * self.co2_bkg  # CO2
        water_vapour_ratio = (water_vapour_partial_pressure / self.pressure).decompose().to_value()

        return (
            NITROGEN_RATIO * king_factor_n2
            + OXYGEN_RATIO * king_factor_o2
            + ARGON_RATIO * king_factor_ar
            + co2_ratio * king_factor_co2
            + water_vapour_ratio * king_factor_wv
        ) / (
            NITROGEN_RATIO + OXYGEN_RATIO + ARGON_RATIO + co2_ratio + water_vapour_ratio
        )  # Tomasi eq. 22

    @functools.cached_property
    def depolarization(self):
        """
        Current best estimate of the depolarization factor of moist air.

        Precision not stated in Tomasi et al., but probably better than 1e-4.
        Effects of relative_humidity are of the order of several times 1e-4.

        Returns
        -------
        float
            Depolarization factor of moist air.
        """
        return (
            6 * (self.king_factor - 1) / (3 + 7 * self.king_factor)
        )  # Tomasi eq. 5, solved for rho

    def phase_function(self, angle):
        """
        Calculates the Chandrasekhar phase function according to Eq. 255 of [1]_.

        Parameters
        ----------
        angle : astropy.units.Quantity
            Scattering angle.

        Returns
        -------
            Chandrasekhar phase function for scattering of natural light.

        References
        ----------
        .. [1] S. Chandrasekhar, Radiative Transfer, Dover Publications, 1960.
        """
        rho = self.depolarization

        # need to solve Chandrasekhar eq. 254 for gamma as a function of rho
        f_1 = (2 + 2 * rho) / (2 + rho)
        f_2 = (1 - rho) / (1 + rho)
        return 0.75 * f_1 * (1 + f_2 * np.cos(angle) ** 2)  # Chandrasekhar eq. 255

    # TODO: where does this come from? Needs unit test
    def back_scattering_coefficient(self, angle):
        """
        Back-scattering coefficient for a given scattering angle.

        Parameters
        ----------
        angle : astropy.units.Quantity
            Scattering angle.

        Returns
        -------
        astropy.units.Quantity
            Back-scattering coefficient [1/km]
        """
        return self.phase_function(angle) * self.beta / (4 * np.pi)

    def print_params(self):
        """Prints Rayleigh scattering parameters."""
        print(f"Wavelength:              {self.wavelength}")
        print(f"Air Pressure:            {self.pressure}")
        print(f"Air Temperature:         {self.temperature}")
        print(f"Rel. Humidity:           {self.relative_humidity}")
        print(f"CO2 concentration:       {self.co2_bkg} ppmv")
        print(f"Refractive Index:        {self.refractive_index}")
        print(f"King Factor:             {self.king_factor}")
        print(f"Depolarization:          {self.depolarization}")
        print(f"Mol. cross section:      {self.scattering_cross_section}")
        print(f"Volume scattering coeff: {self.beta}")
