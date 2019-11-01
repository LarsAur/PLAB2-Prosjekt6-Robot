"""The sensob (sensor object) superclass and subclass"""


class Sensob:
    """The sensob superclass"""

    def __init__(self, sensors):
        self.sensors = sensors
        self.sensor_values = None
        self.value = None

    def update(self):
        """Retrieves the values from the sensor object(s) it is raw -
        nothing has been done to it."""
        if not (self.sensor_values):
            self.sensor_values = []
            for sensor in self.sensors:
                # Checks if the sensors value have
                if sensor.get_value():
                    sensor.update()
                self.sensor_values.append(sensor.get_value())

    def reset(self):
        self.sensor_values = None
        self.value = None


class LineDetector(Sensob):

    """Only require the reflectance sensor array"""

    def __init__(self, reflectanceSensor):
        super().__init__([reflectanceSensor])

    def update(self):
        super().update()
        self.values = self.sensor_values
        # converting value of the sensors (low number is black) to indicate if there
        # is a line on the right: 'R' left: 'L', front: 'F' or no line 'N'
        threshhold = 0.7
        if self.sensor_values[0][0] < threshhold and self.sensor_values[0][5] < threshhold:
            self.value = "F"
        elif self.sensor_values[0][0] < threshhold:
            self.value = "L"
        elif self.sensor_values[0][5] < threshhold:
            self.value = "R"
        else:
            self.value = "N"
            print("NO line")

class DistanceSensor(Sensob):
    """ """
    def __init__(self, distanceSensor):
        super.__init__([distanceSensor])

    def update(self):
        super().update()
        self.value = self.sensor_values[0]

    def reset(self):
        self.sensor_values = None
        self.value = None
