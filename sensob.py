"""The sensob (sensor object) superclass and subclass"""


class Sensob:
    """The sensob superclass"""

    def __init__(self, sensors):
        self.sensors = sensors
        self.values = []

    def update(self):
        """Retrieves the values from the sensor object(s) it is raw -
        nothing has been done to it."""
        if not self.values:             # if the sensob has no values from its sensors
            for sensor in self.sensors:
                self.values.append(sensor.get_value())
        return self.values
        # values is an array with varying data types
        # depending on the sensor that is called

    def reset(self):
        self.values = []