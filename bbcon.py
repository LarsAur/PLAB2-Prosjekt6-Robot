from project6_supply.reflectance_sensors import ReflectanceSensors
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

        time.sleep(.1)

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
    rs = ReflectanceSensors(True)
    
    #Creating sensobs
    rsob = LineDetector(rs)

    #Adding sensobs to controller
    controller.sensobs.append(rsob)

    #Creating behaviors
    swl = StayWithinLines(controller, rsob)

    #Adding behaviors
    controller.add_behavior(swl)

    #Adding active behaviors
    controller.activate_behavior(swl)

    #Starts the run
    for i in range(20):
        if(not controller.halt):
            controller.run_one_timestep()
