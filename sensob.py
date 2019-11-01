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
        if not (self.sensor_values):
            self.sensor_values = []
            for sensor in self.sensors:
                # Checks if the sensors value have
                if sensor.get_value():
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
        # converting value of the sensors (low number is black) to indicate if there
        # is a line on the right: 'R' left: 'L', front: 'F' or no line 'N'
        right_mask = (1, 1, 1, -1, -1)
        left_mask = (-1, -1, -1, 1, 1)
        front_mask = (-1,-1,-1,-1,-1)
        none_mask = (1, 1, 1, 1, 1)

        right_mask_sum = 0
        left_mask_sum = 0
        front_mask_sum = 0
        none_mask_sum = 0

        for i in range(len(self.sensor_values)):
            v = (self.sensor_values[0][i] - 0.5)
            right_mask_sum += v * right_mask[i]
            left_mask_sum += v * left_mask[i]
            front_mask_sum += v * front_mask[i]
            none_mask_sum += v * none_mask[i]

        print(self.sensor_values)
        print((right_mask_sum, left_mask_sum, front_mask_sum, none_mask_sum))

        max_mask_sum = max((right_mask_sum, left_mask_sum, front_mask_sum, none_mask_sum))

        if max_mask_sum == right_mask_sum:
            self.values = "R"
        
        if max_mask_sum == left_mask_sum:
            self.values = "L"
        
        if max_mask_sum == front_mask_sum:
            self.values = "F"
        
        if max_mask_sum == none_mask_sum:
            self.values = "N"