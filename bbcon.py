from project6_supply.reflectance_sensors import ReflectanceSensors
from project6_supply.ultrasonic import Ultrasonic
from project6_supply.camera import Camera
from project6_supply.zumo_button import ZumoButton
from project6_supply.motors import Motors
from Behavior import *
from sensob import *
from arbitrator import Arbitrator
from motob import Motob
import time

class BBCON:
    """Controller managing behaviors, sensobs and motobs, updating and resetting them"""

    def __init__(self):
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motobs = []
        self.arbitrator = Arbitrator(self)
        self.halt = False
        self.closeObject = False
        self.redObject = False

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        if not behavior in self.active_behaviors:
            print("ACTIVATING:", behavior)
            self.active_behaviors.append(behavior)
            return True
        return False

    def deactivate_behavior(self, active_behavior):
        if active_behavior in self.active_behaviors:
            print("DEACTIVATING:", active_behavior)
            self.active_behaviors.remove(active_behavior)
            return True
        return False

    def run_one_timestep(self):
        #for sensob in self.sensobs:
        #    sensob.update()

        for behavior in self.active_behaviors:
            behavior.sensob.update()

        for behavior in self.behaviors:
            behavior.update()

        halt, action = self.arbitrator.choose_action()
        if halt:
            self.halt = True

        for motob in self.motobs:
            motob.update(action)

        time.sleep(.2)

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
    print("DEBUG: init sensors")
    reflectance_sensor = ReflectanceSensors(False) # True for auto calibration
    ultrasonic_sensor = Ultrasonic()
    camara_sensor = Camera()

    #Creating sensobs
    print("DEBUG: init sensobs")
    line_sensob = LineDetector(reflectance_sensor)
    distance_sensob = DistanceSensor(ultrasonic_sensor)
    color_sensob = CheckColor(camara_sensor, "red")

    #Adding sensobs to controller
    print("DEBUG: appending sensobs")
    controller.sensobs.append(line_sensob)
    controller.sensobs.append(distance_sensob)
    controller.sensobs.append(color_sensob)

    #Creating behaviors
    print("DEBUG: creating behaviors")
    swl = StayWithinLines(controller, line_sensob)
    dnc = DoNotCrash(controller, distance_sensob)
    chs = ChaseObject(controller, [distance_sensob, color_sensob])

    #Adding behaviors
    print("DEBUG: adding behaviors")
    controller.add_behavior(swl)
    controller.add_behavior(dnc)
    controller.add_behavior(chs)
   
    #Adding active behaviors
    print("DEBUG: activating behaviors")
    controller.activate_behavior(swl)
    controller.activate_behavior(dnc)
    #controller.activate_behavior(chs)

    #Starts the run
    for i in range(50):
        if not controller.halt:
            print("run")
            controller.run_one_timestep()
            print("----------------------------------------------------")

    controller.motobs[0].update(('F', 0)) # turns of motor after the program is finished
