"""The sensob (sensor object) superclass and subclass"""

class Sensob:
    """The sensob superclass"""

    def __init__(self, sensors):
        self.sensors = sensors
        self.sensor_values = None
        self.values = None

    def update(self):
        """Retrieves the values from the sensor object(s) it is raw -
        nothing has been done to it."""
        if not self.values:
            self.sensor_values = []
            for sensor in self.sensors:
                #Checks if the sensors value have 
                if not sensor.get_value():
                    sensor.update()
                self.sensor_values.append(sensor.get_value())

    def reset(self):
        self.sensor_values = None
        self.values = None

class LineDetector(Sensob):

    """Only require the reflectance sensor array"""

    def __init__(self, reflectanceSensor):
        super().__init__([reflectanceSensor])

    def update(self):
        super().update()
        self.values = self.sensor_values
        
        