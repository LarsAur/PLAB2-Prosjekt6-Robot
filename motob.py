class Motob:
    def __init__(self):
        self.motors = []
        self.value = []

    def update(self, value):
        self.value = value
        self.operationalize()

    def operationalize(self):
        rot_const = 1 # Constant to calibrate rotation
        dist_const = 1 # Constants to calibrate distance
        # ('F', s) Forward distance
        # ('B', s) Backward distance
        # ('L', a) Left angle
        # ('R', a)  Right angle
        letter = self.value[0].upper()
        val = self.value[1]

        assert(letter in ('B', 'F', 'L', 'R')) 

        # TODO needs change to what controlls duration and speed

        if letter in ('B', 'F'):
            direction = 1 if letter == 'F' else -1
            speed = direction*val
            for motor in self.motors:
                motor.set_value((speed, speed), dist_const)

        elif letter in ('L', 'R') :
            rotation_direction = 1 if letter == 'R' else -1
            speed = direction * val
            for motor in self.motors:
                motor.set_value((speed, -speed), rot_const)