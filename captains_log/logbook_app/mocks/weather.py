import random

LOW_WIND_SPEED_RANGE_MIN, LOW_WIND_SPEED_RANGE_MAX = (0, 5)
STANDARD_WIND_SPEED_RANGE_MIN, STANDARD_WIND_SPEED_RANGE_MAX = (0, 19)
HIGH_WINDS_SPEED_RANGE_MIN, HIGH_WINDS_SPEED_RANGE_MAX = (20, 29)
GALE_WINDS_SPEED_RANGE_MIN, GALE_WINDS_SPEED_RANGE_MAX = (30, 50)


class MockWeather(object):

    def get_fake_wind_speed(self, last_wind_speed=None):
        """Returns an arbitrary wind speed integer, representing knots

        Keyword arguments:
        last_wind_speed -- previous wind speed (default None)
        """
        new_wind_speed = 0
        chance_of_high_winds = random.randint(1, 24)
        chance_of_gale = random.randint(1, 5)

        if last_wind_speed is not None:
            deviation = 0

            if (chance_of_high_winds < 24 and
                    last_wind_speed < HIGH_WINDS_SPEED_RANGE_MAX + 1):
                deviation = random.randint(0, 2)
                deviation_is_positive = bool(random.getrandbits(1))

                if chance_of_high_winds < 2:
                    new_wind_speed = random.randint(
                        LOW_WIND_SPEED_RANGE_MIN,
                        LOW_WIND_SPEED_RANGE_MAX)
                    return new_wind_speed

                if deviation_is_positive:

                    if last_wind_speed + deviation <= 19:
                        new_wind_speed = last_wind_speed + deviation
                    else:  # result is higher than 359 degrees
                        new_wind_speed = 19

                else:  # deviation will be negative

                    if last_wind_speed - deviation >= 0:
                        new_wind_speed = last_wind_speed - deviation
                    else:  # result is lower than 0 degrees
                        new_wind_speed = 0

            else:

                if chance_of_gale < 5:
                    new_wind_speed = random.randint(
                        HIGH_WINDS_SPEED_RANGE_MIN, HIGH_WINDS_SPEED_RANGE_MAX)
                else:
                    new_wind_speed = random.randint(
                        GALE_WINDS_SPEED_RANGE_MIN, GALE_WINDS_SPEED_RANGE_MAX)

        else:
            if chance_of_high_winds < 24:
                if chance_of_high_winds < 5:
                    new_wind_speed = random.randint(
                        LOW_WIND_SPEED_RANGE_MIN,
                        LOW_WIND_SPEED_RANGE_MAX)
                else:
                    new_wind_speed = random.randint(
                        STANDARD_WIND_SPEED_RANGE_MIN,
                        STANDARD_WIND_SPEED_RANGE_MAX)
            else:
                if chance_of_gale < 2:
                    new_wind_speed = random.randint(
                        HIGH_WINDS_SPEED_RANGE_MIN, HIGH_WINDS_SPEED_RANGE_MAX)
                else:
                    new_wind_speed = random.randint(
                        GALE_WINDS_SPEED_RANGE_MIN, GALE_WINDS_SPEED_RANGE_MAX)

        return new_wind_speed

    def get_fake_wind_direction(self, last_wind_direction=None):
        """Returns a new heading integer based on an existing one, if provided.
        Otherwise, return a random heading integer if not provided.

        Keyword arguments:
        last_wind_direction -- previous heading (default None)
        """

        new_wind_direction = 0

        if last_wind_direction is None:
            new_wind_direction = random.randint(0, 360)
        else:
            deviation = 0
            chance_of_large_deviation = random.randint(1, 24)

            if chance_of_large_deviation < 24:
                deviation = random.randint(0, 2)
            else:  # deviation is large
                deviation = random.randint(0, 90)

            deviation_is_positive = bool(random.getrandbits(1))

            if deviation_is_positive:  # deviation will be clockwise

                if last_wind_direction + deviation <= 359:
                    new_wind_direction = last_wind_direction + deviation
                else:  # result is higher than 359 degrees
                    new_wind_direction = last_wind_direction + deviation - 360

            else:  # deviation will be negative/counter-clockwise

                if last_wind_direction - deviation >= 0:
                    new_wind_direction = last_wind_direction - deviation
                else:  # result is lower than 0 degrees
                    new_wind_direction = last_wind_direction - deviation + 360

        return new_wind_direction

    def get_fake_visibility(self, last_visibility=None):
        """Returns a visbility integer based on an existing one, if provided.
        Otherwise, return a random visbility integer if not provided.

        0 == poor visibility
        1 == fair / high visbility

        Keyword arguments:
        last_visbility -- previous visbility (default None)
        """

        new_visbility = 0
        chance_of_good_visbility = random.randint(1, 40)

        if last_visibility == 0:
            chance_of_persisting_poor_visbility = random.randint(1, 5)
            if chance_of_persisting_poor_visbility > 1:
                new_visbility = 0
            else:
                new_visbility = 1

        else:

            if chance_of_good_visbility < 40:
                new_visbility = 1
            else:
                new_visbility = 0

        return new_visbility
