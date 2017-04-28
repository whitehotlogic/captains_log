import random
# from config.config import CONFIG

WEIGHT_OF_DIESEL = 7.1089  # in pounds/lbs, per gallon


class MockVessel(object):

    def get_fake_engine_hours(
            self, last_engine_hours=None, wind_speed=None,
            speed=None, fuel_level=None):
        new_engine_hours = 0

        if fuel_level is not None and fuel_level < 0.1:
            return last_engine_hours

        if last_engine_hours is not None:
            if wind_speed is not None and speed is not None:
                if wind_speed < 3 and speed > 0:

                    return last_engine_hours + 1
                else:

                    return last_engine_hours
            else:
                increase_engine_hours = bool(random.getrandbits(1))
                if increase_engine_hours:

                    return last_engine_hours + 1
                else:

                    return last_engine_hours
        else:
            new_engine_hours = random.randint(1, 10000)

        return new_engine_hours

    def get_fake_fuel_level(
            self, last_fuel_level=None, wind_speed=None, speed=None):

        # new_fuel_level = 0
        # fuel_capacity = CONFIG["fuel_capacity"]
        # weight_of_fuel = last_fuel_level * WEIGHT_OF_DIESEL  # in pounds/lbs
        # minimum_fuel_level = fuel_capacity / 2.0

        # if last_fuel_level is None:
        #     new_fuel_level = random.uniform(minimum_fuel_level, fuel_capacity)
        # else:
        #     pass

        return 60

    def get_fake_water_level(
            self, last_water_level=None):

        return 50
