""" Contains Helper functions for AstroWeather."""

from datetime import datetime, timedelta, timezone
import logging
import ephem
import math
from decimal import Decimal
from ephem import degree
from math import degrees as deg
import pytz

# The introduction of the module [timezonefinder](https://github.com/jannikmi/timezonefinder)
# with it's nested dependency to [py-h3](https://github.com/uber/h3-py) failed while compiling
# the `c`-module h3 on some home assistant deployment variants (e.g. Home Assistant
# Operating System on RPi).
# from timezonefinder import TimezoneFinder
from pyastroweatherio.const import (
    DEFAULT_ELEVATION,
    DEFAULT_TIMEZONE,
    HOME_LATITUDE,
    HOME_LONGITUDE,
    CIVIL_TWILIGHT,
    CIVIL_DUSK_DAWN,
    NAUTICAL_TWILIGHT,
    NAUTICAL_DUSK_DAWN,
    ASTRONOMICAL_TWILIGHT,
    ASTRONOMICAL_DUSK_DAWN,
    MAGNUS_COEFFICIENT_A,
    MAGNUS_COEFFICIENT_B,
    CONSTANT_C,
    MAG_DEGRATION_MAX,
)

_LOGGER = logging.getLogger(__name__)


class ConversionFunctions:
    """Convert between different Weather Units."""

    async def epoch_to_datetime(self, value) -> str:
        """Converts EPOC time to Date Time String."""
        return datetime.datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S")

    async def anchor_timestamp(self, value) -> datetime:
        """Converts the datetime string from 7Timer to DateTime."""
        _LOGGER.debug("7timer anchor timestamp: %s", str(datetime.strptime(value, "%Y%m%d%H")))
        return datetime.strptime(value, "%Y%m%d%H")


class AstronomicalLiftedIndex:
    """Calculate astronomical lifted index"""

    def __init__(
        self,
    ):
        _LOGGER.debug("AstronomicalLiftedIndex calculation mode active")

    def calculate_vapor_pressure(self, surface_temp):
        """
        Calculate the actual vapor pressure at the surface using the Magnus-Tetens formula.

        Args:
        - surface_temp: Surface temperature in Celsius.

        Returns:
        - e: Actual vapor pressure at the surface in millibars (mb) or hectopascals (hPa).
        """
        # Constants
        A = 6.112
        B = 17.67
        C = 243.5

        # Calculate actual vapor pressure using Magnus-Tetens formula
        e = A * math.exp((B * surface_temp) / (surface_temp + C))

        return e

    def calculate_mixing_ratio(self, e, air_pressure_at_sea_level):
        """
        Calculate the mixing ratio.

        Args:
        - e: Vapor pressure
        - air_pressure_at_sea_level: Air pressure at sea level

        Returns:
        - w: mixing ratio at surface in grams per kilogram
        """
        # Constants
        A = 621.97

        # Calculate actual vapor pressure using Magnus-Tetens formula
        w = A * (e / (air_pressure_at_sea_level - e))

        return w

    def calculate_lifting_condensation_level(self, w, air_pressure_at_sea_level):
        """
        The Lifting Condensation Level is the level at which a parcel becomes saturated. It can be used as
        a reasonable estimate of cloud base height when parcels experience forced ascent.
        Here, we calculate it using the Clausius-Clapeyron equation. This equation relates the saturation vapor
        pressure (e) to the temperature and pressure.
        https://en.wikipedia.org/wiki/Lifted_condensation_level

        Args:
        - w: Mixing ratio
        - air_pressure_at_sea_level: Air pressure at sea level

        Returns:
        - lcl: LCL in meters
        """
        # Constants
        A = 2440
        B = 0.00029

        # Calculate actual vapor pressure using Magnus-Tetens formula
        lcl = (A * w) / ((air_pressure_at_sea_level - w) * (1 - B * air_pressure_at_sea_level))

        return lcl
        
    async def calculate_lifted_index(self, temperature, altitude, dew_point_temperature, air_pressure_at_sea_level):
        # https://en.wikipedia.org/wiki/Lifted_index
        
        # Constants
        env_temp_500mb = -20  # Celsius (environmental temperature at 500 mb level)

        # Calculate saturation vapor pressure at surface temperature
        # Checked with https://www.weather.gov/epz/wxcalc_vaporpressure
        es = self.calculate_vapor_pressure(temperature)

        # Calculate actual vapor pressure at surface
        # Checked with https://www.weather.gov/epz/wxcalc_vaporpressure
        e = self.calculate_vapor_pressure(dew_point_temperature)  #6.112 * (10 ** (7.5 * (Td - Tn) / (Td - 35.85)))

        # Calculate mixing ratio at surface in grams per kilogram
        # Checked with https://www.weather.gov/epz/wxcalc_mixingratio
        w = self.calculate_mixing_ratio(e, air_pressure_at_sea_level)

        # Calculate Lifting Condensation Level
        lcl = self.calculate_lifting_condensation_level(w, air_pressure_at_sea_level)
        
        _LOGGER.debug("Air pressure at sea level (AP): {} mbar".format(air_pressure_at_sea_level))
        _LOGGER.debug("Dew point(DP): {} °C".format(dew_point_temperature))
        _LOGGER.debug("Temperature (T): {} °C".format(temperature))
        _LOGGER.debug("Saturation vapor pressure at surface (ES): {} mbar".format(es))
        _LOGGER.debug("Actual vapor pressure at surface (E): {} mbar".format(e))
        _LOGGER.debug("Mixing ratio at surface (W): {} grams per kg".format(w))
        _LOGGER.debug("Lifting Condensation Level (LCL): {} meters".format(lcl))
        
        # Calculate temperature of lifted parcel at 500 mb level
        lifted_temp_500mb = env_temp_500mb + (temperature - lcl) * 0.5  # Assumption: 500 mb is halfway through the troposphere

        # Calculate Lifted Index
        lifted_index = env_temp_500mb - lifted_temp_500mb
    
        _LOGGER.debug("Temperature of the lifted parcel (T Parcel): {} °C".format(lifted_temp_500mb))
        _LOGGER.debug("Lifted Index (LI): {} °C".format(lifted_index))

        return lifted_index


class AstronomicalTransparency:
    """Calculate astronomical transparency"""

    # Write a python3 program to calculate atmospheric transparence based on humidity, temperature, clouds, wind, altitude, dew_point_temperature, and air_pressure_at_sea_level and convert the transparency to magnitude degradation

    def __init__(
        self,
    ):
        _LOGGER.debug("AstronomicalTransparency calculation mode active")
        # Relative humidity (0.0 to 1.0)
        # Temperature in Celsius
        # Cloud cover fraction (0.0 to 1.0)
        # Wind speed in meters per second
        # Altitude in meters
        # Dew point temperature in Celsius
        # Air pressure at sea level in hPa

    def calculate_transparency(self, humidity, temperature, cloud_cover, wind_speed, altitude, dew_point_temperature, air_pressure_at_sea_level):
        # Coefficients for the linear model (you can adjust these based on your requirements)
        humidity_coefficient = 0.02  # 0.02
        temperature_coefficient = 0.03  #0.03
        cloud_cover_coefficient = -0.1
        wind_speed_coefficient = -0.05
        altitude_coefficient = -0.01
        dew_point_temperature_coefficient = 0.02
        air_pressure_coefficient = 0.01

        # Calculate transparency using the linear model
        transparency = (1 - (humidity * humidity_coefficient) +
                        (temperature * temperature_coefficient) +
                        (cloud_cover * cloud_cover_coefficient / 100) +
                        (wind_speed * wind_speed_coefficient) +
                        # (altitude * altitude_coefficient) +
                        # (air_pressure_at_sea_level * air_pressure_coefficient) +
                        (dew_point_temperature * dew_point_temperature_coefficient))

        # print(humidity, temperature, cloud_cover, wind_speed, altitude, dew_point_temperature, air_pressure_at_sea_level, ":", transparency)
        # Ensure transparency is within the valid range [0, 1]
        transparency = max(0, min(1, transparency))

        return transparency

    def transparency_to_magnitude_degradation(self, transparency):

        # if transparency == 0:
        #     return float(2.5)  #float('inf')
        # else:
        #     magnitude_degradation = -2.5 * math.log10(transparency)
        #     magnitude_degradation = max(0, min(2.5, magnitude_degradation))

        #     return magnitude_degradation

        if transparency == 0:
            return float(MAG_DEGRATION_MAX)  #float('inf')
        else:
            magnitude_degradation = -2.5 * math.log10(transparency)
            magnitude_degradation = max(0, min(MAG_DEGRATION_MAX, magnitude_degradation))

            return magnitude_degradation

    async def calculate_transparency_model(self, humidity, temperature, cloud_cover, wind_speed, altitude, dew_point_temperature, air_pressure_at_sea_level):

        # Calculate transparency
        transparency = self.calculate_transparency(humidity, temperature, cloud_cover, wind_speed, altitude, dew_point_temperature, air_pressure_at_sea_level)

        # Convert transparency to magnitude degradation
        magnitude_degradation = self.transparency_to_magnitude_degradation(transparency)

        # print("Estimated Atmospheric Transparency: {:.2f}".format(transparency))
        # print("Magnitude Degradation: {:.2f}".format(magnitude_degradation))
        
        return magnitude_degradation


class AstronomicalSeeing:
    """Calculate astronomical seeing"""

    def __init__(
        self,
    ):
        _LOGGER.debug("AstronomicalSeeing calculation mode active")
        # temperature = 15  # in Celsius
        # wind_speed = 5  # in m/s
        # humidity = 50  # in Percent
        # aerosol_density = 0.1  # in kg/m^3
        # altitude = 1000  # in Meters

    # Modell 4:
    # This algorithm first calculates the seeing factor based on temperature, humidity, wind speed
    # and altitude above sea level. The seeing factor is then used to calculate the astronomical
    # seeing in arcseconds. The empirical relationship used here states that the seeing in arcseconds
    # is approximately equal to the reciprocal of the seeing factor multiplied by a conversion
    # factor of 0.98.
    def calculate_saturation_vapor_pressure(self, dew_point):
        """
        Calculate the actual vapor pressure at the surface using the Magnus-Tetens formula.

        Args:
        - dew_point: Dew point temperature in Celsius.

        Returns:
        - e: Saturation vapor pressure at the surface in millibars (mb) or hectopascals (hPa).
        """
        # Constants
        A = 6.112
        B = 17.67
        C = 243.5

        # Calculate actual vapor pressure using Magnus-Tetens formula
        es = A * math.exp((B * dew_point) / (dew_point + C))

        return es
    
    def calculate_water_vapor_pressure(self, dew_point_temperature, humidity):
        dew_point = dew_point_temperature
        es = self.calculate_saturation_vapor_pressure(dew_point)
        water_vapor_pressure = (humidity / 100) * es

        return water_vapor_pressure

    # Modell 6:
    # This algorithm first calculates the seeing factor based on temperature, humidity, wind speed
    # and altitude above sea level. It is similar to Model 4 and 5 but uses the air pressure at sea level
    # and dew point provided by Met.no.
    async def calculate_seeing_model(
        self, temperature, humidity, dew_point_temperature, wind_speed, cloud_cover, altitude, air_pressure_at_sea_level
    ):
        water_vapor_pressure = self.calculate_water_vapor_pressure(dew_point_temperature, humidity)

        adjusted_pressure = air_pressure_at_sea_level * math.exp(-0.00012 * altitude)
        relative_pressure = adjusted_pressure / air_pressure_at_sea_level

        seeing_factor = CONSTANT_C * (water_vapor_pressure / 10) ** 0.35 * (wind_speed / 10) ** 0.65 * relative_pressure
        seeing = 0.98 / seeing_factor

        _LOGGER.debug(
            "AstronomicalSeeing calculation model6: T %s, H %s, DP %s, W %s, E %s, P %s - wvp %s rp %s - S %s",
            str(temperature),
            str(humidity),
            str(dew_point_temperature),
            str(wind_speed),
            str(altitude),
            str(air_pressure_at_sea_level),
            str(water_vapor_pressure),
            str(relative_pressure),
            str(seeing),
        )

        if seeing > 2.5:
            seeing = 2.5  # max out seeing

        return seeing

    # Modell 7:
    # This algorithm first calculates the seeing factor based on temperature, humidity, wind speed
    # and altitude above sea level. It is similar to Model 6 but takes the cloud coverage into account.
    # This somehow doesn't seem to be correct, since seeing can be good even with clouds.
    async def calculate_seeing_model7(
        self, temperature, humidity, dew_point_temperature, wind_speed, cloud_cover, altitude, air_pressure_at_sea_level
    ):
        water_vapor_pressure = self.calculate_water_vapor_pressure(dew_point_temperature, humidity)

        adjusted_pressure = air_pressure_at_sea_level * math.exp(-0.00012 * altitude)
        relative_pressure = adjusted_pressure / air_pressure_at_sea_level

        # Take care on the clouds
        cloud_factor = 1 - (cloud_cover / 100)

        seeing_factor = (
            CONSTANT_C
            * (water_vapor_pressure / 10) ** 0.2
            * (wind_speed / 10) ** 0.6
            * relative_pressure**0.3
            * cloud_factor
        )
        if seeing_factor == 0:
            seeing = 2.5  # max out seeing
        else:
            seeing = 0.98 / seeing_factor

        _LOGGER.debug(
            "AstronomicalSeeing calculation model7: T %s, H %s, DP %s, W %s, C %s, E %s, P %s - S %s",
            str(temperature),
            str(humidity),
            str(dew_point_temperature),
            str(wind_speed),
            str(cloud_cover),
            str(altitude),
            str(air_pressure_at_sea_level),
            str(seeing),
        )

        if seeing > 2.5:
            seeing = 2.5  # max out seeing

        return seeing


class AstronomicalRoutines:
    """Calculate different astronomical objects"""

    def __init__(
        self,
        latitude=HOME_LATITUDE,
        longitude=HOME_LONGITUDE,
        elevation=DEFAULT_ELEVATION,
        timezone_info=DEFAULT_TIMEZONE,
        forecast_time=None,
    ):
        self._latitude = latitude
        self._longitude = longitude
        self._elevation = elevation
        self._timezone_info = timezone_info
        # tz_find = TimezoneFinder()
        # self._timezone_info = tz_find.timezone_at(lng=longitude, lat=latitude)
        self._test_mode = False
        _LOGGER.debug("Timezone: %s", self._timezone_info)
        if forecast_time is None:
            self._forecast_time = datetime.now(timezone.utc).replace(tzinfo=pytz.utc)
        else:
            self._forecast_time = forecast_time.replace(tzinfo=pytz.utc)
            self._test_mode = True
        _LOGGER.debug("Forecast Time: %s", self._forecast_time)

        self._sun_observer = None
        self._sun_observer_nautical = None
        self._sun_observer_astro = None
        self._moon_observer = None
        self._sun_next_rising_civil = None
        self._sun_next_setting_civil = None
        self._sun_next_rising_nautical = None
        self._sun_next_setting_nautical = None
        self._sun_next_rising_astro = None
        self._sun_next_setting_astro = None
        self._sun_altitude = None
        self._sun_azimuth = None
        self._moon_next_rising = None
        self._moon_next_setting = None
        self._moon_next_new_moon = None
        self._moon_next_full_moon = None
        self._moon_altitude = None
        self._moon_azimuth = None
        self._sun = None
        self._moon = None

        # Internal only
        self._sun_previous_rising_astro = None
        self._sun_previous_setting_astro = None
        self._moon_previous_rising = None
        self._moon_previous_setting = None
        # self._moon_day_after_next_rising = None
        # self._moon_day_after_next_setting = None

    def utc_to_local(self, utc_dt):
        """Localizes the datetime"""
        local_tz = pytz.timezone(self._timezone_info)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)

    def utc_to_local_diff(self):
        """returns the UTC Offset"""
        now = datetime.now(pytz.timezone(self._timezone_info))
        return now.utcoffset().total_seconds() / 3600

    #
    # Observers
    #
    def get_sun_observer(self, below_horizon=ASTRONOMICAL_DUSK_DAWN) -> ephem.Observer:
        """Retrieves the ephem sun observer for the current location"""
        observer = ephem.Observer()
        observer.lon = str(self._longitude)  # * degree
        observer.lat = str(self._latitude)  # * degree
        observer.elevation = self._elevation
        observer.horizon = below_horizon * degree
        observer.pressure = 0
        observer.epoch = datetime.now().strftime("%Y/%m/%d")
        return observer

    def get_moon_observer(self) -> ephem.Observer:
        """Retrieves the ephem mon observer for the current location"""
        observer = ephem.Observer()
        observer.lon = str(self._longitude)  # * degree
        observer.lat = str(self._latitude)  # * degree
        observer.elevation = self._elevation
        # Naval Observatory Risings and Settings
        # Set horizon to minus 34 arcminutes
        # https://aa.usno.navy.mil/data/RS_OneDay
        observer.horizon = "-0:34"
        observer.pressure = 0
        observer.epoch = datetime.now().strftime("%Y/%m/%d")
        return observer

    #
    # Sun & Moon
    #
    def calculate_sun(self):
        """Calculates sun risings and settings"""
        if self._sun_observer is None:
            self._sun_observer = self.get_sun_observer(CIVIL_DUSK_DAWN)
        if self._sun_observer_nautical is None:
            self._sun_observer_nautical = self.get_sun_observer(NAUTICAL_DUSK_DAWN)
        if self._sun_observer_astro is None:
            self._sun_observer_astro = self.get_sun_observer(ASTRONOMICAL_DUSK_DAWN)
        if self._sun is None:
            self._sun = ephem.Sun()

        # Rise and Setting (Civil)
        try:
            self._sun_next_rising_civil = (
                self._sun_observer.next_rising(ephem.Sun(), use_center=True).datetime().replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next rising
            start = self._sun_observer.date.datetime()
            end = self._sun_observer.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer.date = timestamp
                try:
                    self._sun_next_rising_astro = self._sun_observer.next_rising(
                        ephem.Sun(), use_center=True
                    ).datetime()
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_next_setting_civil = (
                self._sun_observer.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next setting
            start = self._sun_observer.date.datetime()
            end = self._sun_observer.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer.date = timestamp
                try:
                    self._sun_next_setting_astro = self._sun_observer.next_setting(
                        ephem.Sun(), use_center=True
                    ).datetime()
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        # Rise and Setting (Nautical)
        self._sun_observer_nautical.date = self._forecast_time
        self._sun.compute(self._sun_observer_nautical)

        try:
            self._sun_next_rising_nautical = (
                self._sun_observer_nautical.next_rising(ephem.Sun(), use_center=True)
                .datetime()
                .replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next astronomical rising
            start = self._sun_observer_nautical.date.datetime()
            end = self._sun_observer_nautical.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer_nautical.date = timestamp
                try:
                    self._sun_next_rising_nautical = (
                        self._sun_observer_nautical.next_rising(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=pytz.utc)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_next_setting_nautical = (
                self._sun_observer_nautical.next_setting(ephem.Sun(), use_center=True)
                .datetime()
                .replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next astronomical setting
            start = self._sun_observer_nautical.date.datetime()
            end = self._sun_observer_nautical.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer_nautical.date = timestamp
                try:
                    self._sun_next_setting_nautical = (
                        self._sun_observer_nautical.next_setting(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=pytz.utc)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        # Rise and Setting (Astronomical)
        self._sun_observer_astro.date = self._forecast_time
        self._sun.compute(self._sun_observer_astro)

        try:
            self._sun_next_rising_astro = (
                self._sun_observer_astro.next_rising(ephem.Sun(), use_center=True).datetime().replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next astronomical rising
            start = self._sun_observer_astro.date.datetime()
            end = self._sun_observer_astro.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer_astro.date = timestamp
                try:
                    self._sun_next_rising_astro = (
                        self._sun_observer_astro.next_rising(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=pytz.utc)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_previous_rising_astro = (
                self._sun_observer_astro.previous_rising(ephem.Sun(), use_center=True)
                .datetime()
                .replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the previous astronomical rising
            start = self._sun_observer_astro.date.datetime()
            end = self._sun_observer_astro.date.datetime() - timedelta(days=365)
            timestamp = start
            while timestamp > end:
                timestamp -= timedelta(minutes=1440)
                self._sun_observer_astro.date = timestamp
                try:
                    self._sun_previous_rising_astro = (
                        self._sun_observer_astro.previous_rising(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=pytz.utc)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_next_setting_astro = (
                self._sun_observer_astro.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the next astronomical setting
            start = self._sun_observer_astro.date.datetime()
            end = self._sun_observer_astro.date.datetime() + timedelta(days=365)
            timestamp = start
            while timestamp < end:
                timestamp += timedelta(minutes=1440)
                self._sun_observer_astro.date = timestamp
                try:
                    self._sun_next_setting_astro = (
                        self._sun_observer_astro.next_setting(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=pytz.utc)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

        try:
            self._sun_previous_setting_astro = (
                self._sun_observer_astro.previous_setting(ephem.Sun(), use_center=True)
                .datetime()
                .replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            # Search for the previous astronomical setting
            start = self._sun_observer_astro.date.datetime()
            end = self._sun_observer_astro.date.datetime() - timedelta(days=365)
            timestamp = start
            while timestamp > end:
                timestamp -= timedelta(minutes=1440)
                self._sun_observer_astro.date = timestamp
                try:
                    self._sun_previous_setting_astro = (
                        self._sun_observer_astro.previous_setting(ephem.Sun(), use_center=True)
                        .datetime()
                        .replace(tzinfo=pytz.utc)
                    )
                except (ephem.AlwaysUpError, ephem.NeverUpError):
                    continue
                break

    def calculate_sun_altaz(self):
        """Calculates sun altitude and azimuth"""
        if self._sun_observer is None:
            self._sun_observer = self.get_sun_observer(CIVIL_DUSK_DAWN)
        if self._sun is None:
            self._sun = ephem.Sun()

        self._sun_observer.date = self._forecast_time
        self._sun.compute(self._sun_observer)

        # Sun Altitude
        self._sun_altitude = deg(float(self._sun.alt))

        # Sun Azimuth
        self._sun_azimuth = deg(float(self._sun.az))

    def calculate_moon(self):
        """Calculates moon rising and setting"""
        if self._moon_observer is None:
            self._moon_observer = self.get_moon_observer()
        if self._moon is None:
            self._moon = ephem.Moon()

        # Rise and Setting
        self._moon_observer.date = self._forecast_time
        self._moon.compute(self._moon_observer)

        try:
            self._moon_next_rising = self._moon_observer.next_rising(ephem.Moon()).datetime().replace(tzinfo=pytz.utc)
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            pass

        try:
            self._moon_next_setting = self._moon_observer.next_setting(ephem.Moon()).datetime().replace(tzinfo=pytz.utc)
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            pass

        try:
            self._moon_previous_rising = (
                self._moon_observer.previous_rising(ephem.Moon()).datetime().replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            pass

        try:
            self._moon_previous_setting = (
                self._moon_observer.previous_setting(ephem.Moon()).datetime().replace(tzinfo=pytz.utc)
            )
        except (ephem.AlwaysUpError, ephem.NeverUpError):
            pass

        # self._moon_observer.date = self._forecast_time + timedelta(days=1)
        # self._moon.compute(self._moon_observer)

        # try:
        #     self._moon_day_after_next_rising = self._moon_observer.next_rising(ephem.Moon()).datetime().replace(tzinfo=pytz.utc)
        # except (ephem.AlwaysUpError, ephem.NeverUpError):
        #     pass

        # try:
        #     self._moon_day_after_next_setting = self._moon_observer.next_setting(ephem.Moon()).datetime().replace(tzinfo=pytz.utc)
        # except (ephem.AlwaysUpError, ephem.NeverUpError):
        #     pass

        # Next new Moon
        self._moon_next_new_moon = ephem.next_new_moon(self._forecast_time).datetime().replace(tzinfo=pytz.utc)

        # Next full Moon
        self._moon_next_full_moon = ephem.next_full_moon(self._forecast_time).datetime().replace(tzinfo=pytz.utc)

    def calculate_moon_altaz(self):
        """Calculates moon altitude and azimuth"""
        if self._moon_observer is None:
            self._moon_observer = self.get_moon_observer()
        if self._moon is None:
            self._moon = ephem.Moon()

        self._moon_observer.date = self._forecast_time
        self._moon.compute(self._moon_observer)

        # Moon Altitude
        self._moon_altitude = deg(float(self._moon.alt))

        # Moon Azimuth
        self._moon_azimuth = deg(float(self._moon.az))

    async def sun_previous_rising_astro(self) -> datetime:
        """Returns sun previous astronomical rising"""
        if self._sun_previous_rising_astro is None or self._forecast_time > self._sun_previous_rising_astro:
            _LOGGER.debug("Astronomical calculations updating sun_previous_rising_astro")
            self.calculate_sun()

        if self._sun_previous_rising_astro is not None:
            return self._sun_previous_rising_astro

    async def sun_previous_setting_astro(self) -> datetime:
        """Returns sun previous astronomical setting"""
        if self._sun_previous_setting_astro is None or self._forecast_time > self._sun_previous_setting_astro:
            _LOGGER.debug("Astronomical calculations updating sun_previous_setting_astro")
            self.calculate_sun()

        if self._sun_previous_setting_astro is not None:
            return self._sun_previous_setting_astro

    def astronomical_darkness(self) -> bool:
        """Returns true during astronomical night"""

        if self._sun_next_setting_astro > self._sun_next_rising_astro:
            return True
        return False

    def moon_down(self) -> bool:
        """Returns true while moon is set"""

        if self._moon_next_setting > self._moon_next_rising:
            return True
        return False

    #
    # Public methods
    #
    async def time_shift(self) -> int:
        """Returns the time_shift to UTC"""
        return int(self.utc_to_local_diff() * 3600)

    async def need_update(self, forecast_time=None):
        """Update Sun and Moon"""
        if forecast_time is not None:
            self._forecast_time = forecast_time.replace(tzinfo=pytz.utc)

        self.calculate_sun_altaz()
        self.calculate_moon_altaz()

        if (
            self._sun_next_setting_civil is None
            or self._sun_next_setting_nautical is None
            or self._sun_next_setting_astro is None
            or self._sun_next_rising_astro is None
            or self._sun_next_rising_nautical is None
            or self._sun_next_rising_civil is None
            or self._moon_next_rising is None
            or self._moon_next_setting is None
            or self._forecast_time > self._sun_next_setting_civil
            or self._forecast_time > self._sun_next_setting_nautical
            or self._forecast_time > self._sun_next_setting_astro
            or self._forecast_time > self._sun_next_rising_astro
            or self._forecast_time > self._sun_next_rising_nautical
            or self._forecast_time > self._sun_next_rising_civil
            or self._forecast_time > self._moon_next_rising
            or self._forecast_time > self._moon_next_setting
        ):
            _LOGGER.debug("Astronomical calculations updating")
            self.calculate_sun()
            self.calculate_moon()

    # Return Sun information
    async def sun_next_rising(self) -> datetime:
        """Returns sun next rising"""
        if (
            self._sun_next_rising_astro is None
            or self._sun_next_rising_nautical is None
            or self._sun_next_rising_civil is None
            or self._forecast_time > self._sun_next_rising_astro
            or self._forecast_time > self._sun_next_rising_nautical
            or self._forecast_time > self._sun_next_rising_civil
        ):
            _LOGGER.debug("Astronomical calculations updating sun_next_rising")
            self.calculate_sun()

        if self._sun_next_rising_astro is not None:
            return self._sun_next_rising_astro
        if self._sun_next_rising_nautical is not None:
            return self._sun_next_rising_nautical
        if self._sun_next_rising_civil is not None:
            return self._sun_next_rising_civil

    async def sun_next_rising_civil(self) -> datetime:
        """Returns sun next rising"""
        if self._sun_next_setting_civil is None or self._forecast_time > self._sun_next_setting_civil:
            _LOGGER.debug("Astronomical calculations updating sun_next_rising_civil")
            self.calculate_sun()

        if self._sun_next_rising_civil is not None:
            return self._sun_next_rising_civil

    async def sun_next_rising_nautical(self) -> datetime:
        """Returns sun next nautical rising"""
        if self._sun_next_rising_nautical is None or self._forecast_time > self._sun_next_rising_nautical:
            _LOGGER.debug("Astronomical calculations updating sun_next_rising_nautical")
            self.calculate_sun()

        if self._sun_next_rising_nautical is not None:
            return self._sun_next_rising_nautical

    async def sun_next_rising_astro(self) -> datetime:
        """Returns sun next astronomical rising"""
        if self._sun_next_rising_astro is None or self._forecast_time > self._sun_next_rising_astro:
            _LOGGER.debug("Astronomical calculations updating sun_next_rising_astro")
            self.calculate_sun()

        if self._sun_next_rising_astro is not None:
            return self._sun_next_rising_astro

    async def sun_next_setting(self) -> datetime:
        """Returns sun next setting"""
        if (
            self._sun_next_setting_civil is None
            or self._sun_next_setting_nautical is None
            or self._sun_next_setting_astro is None
            or self._forecast_time > self._sun_next_setting_civil
            or self._forecast_time > self._sun_next_setting_nautical
            or self._forecast_time > self._sun_next_setting_astro
        ):
            _LOGGER.debug("Astronomical calculations updating sun_next_setting")
            self.calculate_sun()

        if self._sun_next_setting_astro is not None:
            return self._sun_next_setting_astro
        if self._sun_next_setting_nautical is not None:
            return self._sun_next_setting_nautical
        if self._sun_next_setting_civil is not None:
            return self._sun_next_setting_civil

    async def sun_next_setting_civil(self) -> datetime:
        """Returns sun next setting"""
        if self._sun_next_setting_civil is None or self._forecast_time > self._sun_next_setting_civil:
            _LOGGER.debug("Astronomical calculations updating sun_next_setting_civil")
            self.calculate_sun()

        if self._sun_next_setting_civil is not None:
            return self._sun_next_setting_civil

    async def sun_next_setting_nautical(self) -> datetime:
        """Returns sun next nautical setting"""
        if self._sun_next_setting_nautical is None or self._forecast_time > self._sun_next_setting_nautical:
            _LOGGER.debug("Astronomical calculations updating sun_next_setting_nautical")
            self.calculate_sun()

        if self._sun_next_setting_nautical is not None:
            return self._sun_next_setting_nautical

    async def sun_next_setting_astro(self) -> datetime:
        """Returns sun next astronomical setting"""
        if self._sun_next_setting_astro is None or self._forecast_time > self._sun_next_setting_astro:
            _LOGGER.debug("Astronomical calculations updating sun_next_setting_astro")
            self.calculate_sun()

        if self._sun_next_setting_astro is not None:
            return self._sun_next_setting_astro

    async def sun_altitude(self) -> float:
        """Returns the sun altitude"""
        self.calculate_sun_altaz()

        if self._sun_altitude is not None:
            return self._sun_altitude

    async def sun_azimuth(self) -> float:
        """Returns the sun azimuth"""
        self.calculate_sun_altaz()

        if self._sun_azimuth is not None:
            return self._sun_azimuth

    # Return Moon information
    async def moon_next_rising(self) -> datetime:
        if self._moon_next_rising is None or self._forecast_time > self._moon_next_rising:
            _LOGGER.debug("Astronomical calculations updating moon_next_rising")
            self.calculate_moon()

        """Returns moon next rising"""
        if self._moon_next_rising is not None:
            return self._moon_next_rising

    async def moon_next_setting(self) -> datetime:
        if self._moon_next_setting is None or self._forecast_time > self._moon_next_setting:
            _LOGGER.debug("Astronomical calculations updating moon_next_setting")
            self.calculate_moon()

        """Returns moon next setting"""
        if self._moon_next_setting is not None:
            return self._moon_next_setting

    async def moon_phase(self) -> float:
        """Returns the moon phase"""
        self.calculate_moon()

        if self._moon is not None:
            return self._moon.phase

    async def moon_next_new_moon(self) -> float:
        """Returns the next new moon"""
        if self._moon_next_new_moon is None or self._forecast_time > self._moon_next_new_moon:
            _LOGGER.debug("Astronomical calculations updating moon_next_new_moon")
            self.calculate_moon()

        if self._moon_next_new_moon is not None:
            return self._moon_next_new_moon

    async def moon_next_full_moon(self) -> float:
        """Returns the next full moon"""
        if self._moon_next_full_moon is None or self._forecast_time > self._moon_next_full_moon:
            _LOGGER.debug("Astronomical calculations updating moon_next_full_moon")
            self.calculate_moon()

        if self._moon_next_full_moon is not None:
            return self._moon_next_full_moon

    async def moon_altitude(self) -> float:
        """Returns the moon altitude"""
        self.calculate_moon_altaz()

        if self._moon_altitude is not None:
            return self._moon_altitude

    async def moon_azimuth(self) -> float:
        """Returns the moon azimuth"""
        self.calculate_moon_altaz()

        if self._moon_azimuth is not None:
            return self._moon_azimuth

    # Astronomical Night and Darkness information
    async def night_duration_astronomical(self) -> float:
        """Returns the remaining timespan of astronomical darkness"""
        start_timestamp = None

        # Are we already in darkness?
        if self.astronomical_darkness():
            start_timestamp = self._sun_previous_setting_astro
        else:
            start_timestamp = self._sun_next_setting_astro

        astroduration = self._sun_next_rising_astro - start_timestamp

        return astroduration.total_seconds()

    async def deep_sky_darkness_moon_rises(self) -> bool:
        """Returns true if moon rises during astronomical night"""
        start_timestamp = None

        # Are we already in darkness?
        if self.astronomical_darkness():
            start_timestamp = self._sun_previous_setting_astro
        else:
            start_timestamp = self._sun_next_setting_astro

        if self._moon_next_rising > start_timestamp and self._moon_next_rising < self._sun_next_rising_astro:
            _LOGGER.debug("Moon rises during astronomical night")
            return True
        return False

    async def deep_sky_darkness_moon_sets(self) -> bool:
        """Returns true if moon sets during astronomical night"""
        start_timestamp = None

        # Are we already in darkness?
        if self.astronomical_darkness():
            start_timestamp = self._sun_previous_setting_astro
        else:
            start_timestamp = self._sun_next_setting_astro

        # Did Moon already set in darkness?
        if self.moon_down() and self.astronomical_darkness():
            start_timestamp_moon = self._moon_previous_setting
        else:
            start_timestamp_moon = self._moon_next_setting

        if start_timestamp_moon > start_timestamp and start_timestamp_moon < self._sun_next_rising_astro:
            _LOGGER.debug("Moon sets during astronomical night")
            return True
        return False

    async def deep_sky_darkness_moon_always_up(self) -> bool:
        """Returns true if moon is up during astronomical night"""
        start_timestamp = None

        # Are we already in darkness?
        if self.astronomical_darkness():
            start_timestamp = self._sun_previous_setting_astro
        else:
            start_timestamp = self._sun_next_setting_astro

        if self._moon_next_rising < start_timestamp and self._moon_next_setting > self._sun_next_rising_astro:
            _LOGGER.debug("Moon is up during astronomical night")
            return True
        return False

    async def deep_sky_darkness_moon_always_down(self) -> bool:
        """Returns true if moon is down during astronomical night"""
        start_timestamp = None

        # Are we already in darkness?
        if self.astronomical_darkness():
            start_timestamp = self._sun_previous_setting_astro
        else:
            start_timestamp = self._sun_next_setting_astro

        if self._moon_previous_setting < start_timestamp and self._moon_next_rising > self._sun_next_rising_astro:
            _LOGGER.debug("Moon is down during astronomical night")
            return True
        return False

    async def deep_sky_darkness(self) -> float:
        """Returns the remaining timespan of deep sky darkness"""
        dsd = timedelta(0)

        if self.astronomical_darkness():
            _LOGGER.debug(f"DSD - In astronomical darkness")
            if await self.deep_sky_darkness_moon_rises():
                dsd = self._moon_next_rising - self._forecast_time
                _LOGGER.debug(f"DSD - Sun down, Moon rises {dsd}")

            if await self.deep_sky_darkness_moon_sets():
                if self.moon_down():
                    dsd = self._sun_next_rising_astro - self._forecast_time
                    _LOGGER.debug(f"DSD - Sun down, Moon is down {dsd}")
                else:
                    dsd = self._sun_next_rising_astro - self._moon_next_setting
                    _LOGGER.debug(f"DSD - Sun down, Moon sets {dsd}")

            if await self.deep_sky_darkness_moon_always_down():
                dsd = self._sun_next_rising_astro - self._forecast_time
                _LOGGER.debug(f"DSD - Moon always down {dsd}")
            else:
                _LOGGER.debug(f"DSD - Moon NOT always down {dsd}")

        if not self.astronomical_darkness():
            _LOGGER.debug(f"DSD - At sunlight")
            if await self.deep_sky_darkness_moon_rises():
                dsd = self._moon_next_rising - self._sun_next_setting_astro
                _LOGGER.debug(f"DSD - Sun up, Moon rises {dsd}")

            if await self.deep_sky_darkness_moon_sets():
                dsd = self._sun_next_rising_astro - self._moon_next_setting
                _LOGGER.debug(f"DSD - Sun up, Moon sets {dsd}")

            if await self.deep_sky_darkness_moon_always_down():
                dsd = self._sun_next_rising_astro - self._sun_next_setting_astro
                _LOGGER.debug(f"DSD - Sun up, Moon down {dsd}")

        if await self.deep_sky_darkness_moon_always_up():
            dsd = timedelta(0)
            _LOGGER.debug(f"DSD - Moon always up {dsd}")
        else:
            _LOGGER.debug(f"DSD - Moon NOT always up {dsd}")

        return dsd.total_seconds()
