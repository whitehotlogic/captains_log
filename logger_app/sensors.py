from .mocks.position import MockPosition
from .mocks.vessel import MockVessel
from .mocks.weather import MockWeather


class Sensors:
    def __init__(self, mock=False):
        self.mock = mock
        self.latitude = None
        self.longitude = None
        self.course = None
        self.speed = None
        self.fuel_level = None
        self.water_level = None
        self.weather = None
        self.wind_speed = None
        self.wind_direction = None
        self.visibility = None
        self.engine_hours = None

    def update(self):
        self.get_position()
        self.get_weather()
        self.get_vessel_details()

    def get_position(self):
        if self.mock:
            mock_position = MockPosition()
            self.speed = mock_position.get_fake_speed(last_speed=self.speed)
            self.course = mock_position.get_fake_direction(
                last_direction=self.course)
            lat_lon = mock_position.get_fake_position(
                speed=self.speed, last_direction=self.course,
                last_latitude=self.latitude, last_longitude=self.longitude
            )
            self.latitude = lat_lon['latitude']
            self.longitude = lat_lon['longitude']

    def get_weather(self):
        if self.mock:
            mock_weather = MockWeather()
            self.wind_speed = mock_weather.get_fake_wind_speed(
                last_wind_speed=self.wind_speed)
            self.wind_direction = mock_weather.get_fake_wind_direction(
                last_wind_direction=self.wind_direction)
            self.visibility = mock_weather.get_fake_visibility(
                last_visibility=self.visibility)

    def get_vessel_details(self):
        if self.mock:
            mock_vessel = MockVessel()
            self.engine_hours = mock_vessel.get_fake_engine_hours(
                last_engine_hours=self.engine_hours)
            self.fuel_level = mock_vessel.get_fake_fuel_level(
                last_fuel_level=self.fuel_level, wind_speed=self.wind_speed,
                speed=self.speed
            )
            self.water_level = mock_vessel.get_fake_water_level(
                last_water_level=self.water_level)
