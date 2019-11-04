from project6_supply.reflectance_sensors import ReflectanceSensors
from project6_supply.ultrasonic import Ultrasonic
from project6_supply.zumo_button import ZumoButton
from project6_supply.motors import Motors
from Behavior import *
from arbitrator import Arbitrator
from sensob import *
from motob import Motob
import time

class BBCON:

    def __init__(self):
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motobs = []
        self.arbitrator = Arbitrator(self)
        self.halt = False

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        if behavior in self.behaviors:
            self.active_behaviors.append(behavior)
            return True
        return False

    def deactivate_behavior(self, active_behavior):
        if active_behavior in self.active_behaviors:
            self.active_behaviors.remove(active_behavior)
            return True
        return False

    def run_one_timestep(self):
        for sensob in self.sensobs:
            sensob.update()

        for behavior in self.active_behaviors:
            behavior.update()

        halt, action = self.arbitrator.choose_action()
        if halt:
            self.halt = True

        for motob in self.motobs:
            motob.update(action)

        time.sleep(.5)

        for sensob in self.sensobs:
            sensob.reset()

if __name__ == "__main__":
    controller = BBCON()
    zumobutton = ZumoButton()
    zumobutton.wait_for_press()
    #Creating motob and adding Motors to the motob
    motob = Motob()
    motob.motors.append(Motors())
    controller.motobs.append(motob)

    #Creating sensor objects
    reflectance_sensor = ReflectanceSensors(True) # True for auto calibration
    ultrasonic_sensor = Ultrasonic()

    #Creating sensobs
    line_sensob = LineDetector(reflectance_sensor)
    distance_sensob = DistanceSensor(ultrasonic_sensor)

    #Adding sensobs to controller
    controller.sensobs.append(line_sensob)
    controller.sensobs.append(distance_sensob)

    #Creating behaviors
    swl = StayWithinLines(controller, line_sensob)
    dnc = DoNotCrash(controller, distance_sensob)

    #Adding behaviors
    controller.add_behavior(swl)
    controller.add_behavior(dnc)
            
    #Adding active behaviors
    controller.activate_behavior(swl)
    controller.activate_behavior(dnc)

    #Starts the run
    for i in range(20):
        if(not controller.halt):
            controller.run_one_timestep()

    controller.motobs[0].update(('F', 0)) # turns of motor after the program is finished
