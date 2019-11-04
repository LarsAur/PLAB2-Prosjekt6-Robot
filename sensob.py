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
        """Resets all values to none, such that they can be updated again"""
        self.sensor_values = None
        self.value = None


class LineDetector(Sensob):
    """Linedetector which require the reflectance sensors"""

    def __init__(self, reflectanceSensor):
        super().__init__([reflectanceSensor])

    def update(self):
        """Reads from the reflectance sesors and sets the value to indicate where there is a line
        'L' for left, 'R' for right, 'F' for front and 'N' if there is no line"""
        super().update()
        # converting value of the sensors (low number is black)
        if not self.value:
            threshhold = 0.7
            if self.sensor_values[0][0] < threshhold and self.sensor_values[0][5] < threshhold:
                self.value = "F"
            elif self.sensor_values[0][0] < threshhold:
                self.value = "L"
            elif self.sensor_values[0][5] < threshhold:
                self.value = "R"
            else:
                self.value = "N"

class DistanceSensor(Sensob):
    
    def __init__(self, distanceSensor):
        super.__init__([distanceSensor])

    def update(self):
        """Reads from the ultrasonic sensor and sets the value to the distance in centimeters"""
        super().update()
        self.value = self.sensor_values[0]