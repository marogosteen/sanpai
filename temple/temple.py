import math

MAX_DEGREES = 360
EARTH_CIRCUMFERENCE = 4*10**4


class Temple():
    zfill_size = 2

    def __init__(
        self, id: str, name: str, latitude: float, longitude: float
    ) -> None:
        self.id = str(id).zfill(self.zfill_size)
        self.name = name
        # TODO change 34 to average
        radian = 2 * math.pi * 34 / MAX_DEGREES
        self.x = EARTH_CIRCUMFERENCE * longitude / \
            MAX_DEGREES * math.cos(radian)
        self.y = EARTH_CIRCUMFERENCE * latitude / MAX_DEGREES
