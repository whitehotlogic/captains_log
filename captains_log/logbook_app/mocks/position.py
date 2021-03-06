import geopy
import geopy.distance
import random


class MockPosition(object):

    def get_fake_speed(self, last_speed=None):
        """Returns an arbitrary speed integer, representing knots"""
        new_speed = 0

        if last_speed is not None:
            deviation = 0
            chance_of_large_deviation = random.randint(1, 15)

            if chance_of_large_deviation < 75:
                deviation = random.randint(0, 1)
            else:  # deviation is large
                deviation = random.randint(0, 4)

            deviation_is_positive = bool(random.getrandbits(1))

            if deviation_is_positive:

                if last_speed + deviation <= 8:
                    new_speed = last_speed + deviation
                else:  # result is higher than 359 degrees
                    new_speed = 8

            else:  # deviation will be negative

                if last_speed - deviation >= 0:
                    new_speed = last_speed - deviation
                else:  # result is lower than 0 degrees
                    new_speed = 0

        else:
            new_speed = random.randint(0, 8)

        return new_speed

    def get_fake_direction(self, last_direction=None):
        """Returns a new heading integer based on an existing one, if provided.
        Otherwise, return a random heading integer if not provided.

        Keyword arguments:
        last_direction -- previous heading (default None)
        """

        new_direction = 0

        if last_direction is None:
            new_direction = random.randint(0, 360)
        else:
            deviation = 0
            chance_of_large_deviation = random.randint(1, 75)

            if chance_of_large_deviation < 75:
                deviation = random.randint(0, 2)
            else:  # deviation is large
                deviation = random.randint(0, 15)

            deviation_is_positive = bool(random.getrandbits(1))

            if deviation_is_positive:  # deviation will be clockwise

                if last_direction + deviation <= 359:
                    new_direction = last_direction + deviation
                else:  # result is higher than 359 degrees
                    new_direction = last_direction + deviation - 360

            else:  # deviation will be negative/counter-clockwise

                if last_direction - deviation >= 0:
                    new_direction = last_direction - deviation
                else:  # result is lower than 0 degrees
                    new_direction = last_direction - deviation + 360

        return new_direction

    def get_fake_position(
            self, speed=None, last_direction=None,
            last_latitude=None, last_longitude=None):
        """Returns a new {latitude, longitude} position from generated or provided
        speed, direction, and last position.

        Keyword arguments:
        speed -- provided speed to abide (default None)
        last_direction -- previous heading (default None)
        last_latitude -- previous latitude (default None)
        last_longitude -- previous longitude (default None)
        """

        new_speed = 0
        new_latitude = 0.0
        new_longitude = 0.0
        new_direction = 0

        if speed is None:
            if last_latitude is None and last_longitude is None:
                new_speed = self.get_fake_speed(last_speed=random.randint(3, 8))
            else:
                new_speed = self.get_fake_speed()
        else:  # speed was provided, do not create fake
            new_speed = speed

        if last_direction is None:
            new_direction = self.get_fake_direction()
        else:
            new_direction = self.get_fake_direction(last_direction=last_direction)

        if last_latitude is not None and last_longitude is not None:
            distance_traveled = new_speed * 1.852  # distance in km, from nm
            start = geopy.Point(last_latitude, last_longitude)
            distance = geopy.distance.VincentyDistance(
                kilometers=distance_traveled)
            end = distance.destination(point=start, bearing=new_direction)
            new_latitude = end.latitude
            new_longitude = end.longitude
        else:  # a latitude or longitude was provided, but both were not
            new_latitude = random.uniform(-90, 90)
            new_longitude = random.uniform(-180, 180)

        new_position = {
            "latitude": new_latitude,
            "longitude": new_longitude
        }

        return new_position
