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
        if not self.sensor_values:
            self.sensor_values = []
            for sensor in self.sensors:
                # Checks if the sensors value have
                if sensor.get_value():
                    sensor.update()
                self.sensor_values.append(sensor.get_value())

    def reset(self):
        self.sensor_values = None
        self.value = None

# ****** LineDetector subclass ******


class LineDetector(Sensob):
    """Only require the reflectance sensor array"""

    def __init__(self, reflectanceSensor):
        super().__init__([reflectanceSensor])

    def update(self):
        """Is this necessary?"""
        super().update()
        # converting value of the sensors (low number is black) to indicate if there
        # is a line on the right: 'R' left: 'L', front: 'F' or no line 'N'

        threshhold = 0.7

        print(self.sensor_values)

        if self.sensor_values[0][0] < threshhold and self.sensor_values[0][5] < threshhold:
            self.value = "F"
            print("FRONT")
        elif self.sensor_values[0][0] < threshhold:
            self.value = "L"
            print("line on L")
        elif self.sensor_values[0][5] < threshhold:
            self.value = "R"
            print("line on R")
        else:
            self.value = "N"
            print("NO line")

# ****** CheckColor ******


class CheckColor(Sensob):
    """Takes a picture and evaluates it"""

    def __init__(self, cameraSensor, color):
        super.__init__(cameraSensor)
        self.color = color                 # the color to search for

    def update(self):
        """Via the superclass update we now have an Image or Imager CHECK THIS
        object in self.sensor_values"""
        super().update()

    def color_check(self):
        """A help-method to check for color"""
        image_object = self.sensor_values            # to shorten from self.sensor_values
        resized_image = image_object.resize(30, 30)
        wta_image = resized_image.map_color_wta()    # checks the difference between the rgb values. With a base threshold of 0.34. If no image is input, uses self.image
        wta_image.get_image_dims()
        for i in range(wta_image.xmax):
            for j in range(wta_image.ymax):
                wta_image.getpixel((i, j))




