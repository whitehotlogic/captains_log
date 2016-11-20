import geopy
import geopy.distance
import random


def get_fake_speed():
    """Returns an arbitrary speed integer, representing knots"""

    return random.randint(0, 8)


def get_fake_direction(last_direction=None):
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

        if deviation_is_positive:

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
        speed=None, last_direction=None,
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
        new_speed = get_fake_speed()
    else:  # speed was provided, do not create fake
        new_speed = speed

    if last_direction is None:
        new_direction = get_fake_direction()
    else:
        new_direction = get_fake_direction(last_direction=last_direction)

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


POSITION = {  # example call: POSITION["lat_long"](last_direction=75)
    "lat_lon": get_fake_position,
    "speed": get_fake_speed,
    "direction": get_fake_direction
}
