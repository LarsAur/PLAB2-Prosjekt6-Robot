from project6_supply.imager2 import Imager

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
                if not sensor.get_value():
                    sensor.update()
                self.sensor_values.append(sensor.get_value())

    def reset(self):
        """Resets all values to none, such that they can be updated again"""
        self.sensor_values = None
        self.value = None
        for sensor in self.sensors:
            sensor.reset()


# ****** LineDetector subclass ******

class LineDetector(Sensob):
    """Linedetector which require the reflectance sensors"""

    def __init__(self, reflectanceSensor):
        super().__init__([reflectanceSensor])

    def update(self):
        """Reads from the reflectance sesors and sets the value to indicate where there is a line
        'L' for left, 'R' for right, 'F' for front and 'N' if there is no line"""
        
        if not self.sensor_values:
            self.sensor_values = []
            for sensor in self.sensors:
                # Checks if the sensors value have
                if not sensor.get_value():
                    sensor.update()
                self.sensor_values.append(sensor.get_value())

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


# ****** CheckColor ******


class CheckColor(Sensob):
    """Takes a picture and evaluates it"""

    def __init__(self, cameraSensor, color):
        super().__init__([cameraSensor])
        self.color = color  # the color to search for
        self.color_array = [0, 0, 0]  # "red", "green", "blue"

    def update(self):
        """Via the superclass update we now have an Image or Imager CHECK THIS
        object in self.sensor_values"""
        
        self.sensor_values = self.sensors[0].update()

        colors = {0: "red",
                  1: "green",
                  2: "blue"}
        
        """A help-method to check for color"""
        image_object = Imager(image=self.sensor_values)  # to shorten from self.sensor_values
        # resized_image = image_object.resize(30, 30)
        wta_image = image_object.map_color_wta()  # checks the difference between the rgb values. With a base threshold of 0.34. If no image is input, uses self.image
        wta_image.get_image_dims()
        for i in range(wta_image.xmax):
            for j in range(wta_image.ymax):
                r, g, b = wta_image.get_pixel(i, j)
                if r > 40:
                    self.color_array[0] += 1
                elif g > 40:
                    self.color_array[1] += 1
                elif b > 40:
                    self.color_array[2] += 1
        found_color = self.color_array.index(max(self.color_array))
        # print("DEBUG: processed camera image: ", wta_image.image)
        print("DEBUG: found color: ", colors[found_color], self.color)
        if colors[found_color] == self.color:
            self.value = True
        else:
            self.value = False

    def reset(self):
        """To reset subclass parameters"""
        super().reset()
        self.color_array = [0, 0, 0]


class DistanceSensor(Sensob):

    def __init__(self, distanceSensor):
        super().__init__([distanceSensor])

    def update(self):
        """Reads from the ultrasonic sensor and sets the value to the distance in centimeters"""
        super().update()
        print("DEBUG: Distance Sensor values ", self.sensor_values)
        self.value = self.sensor_values[0]
