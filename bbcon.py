from behavior import *
from project6_supply.reflectance_sensors import ReflectanceSensors
from arbitrator import Arbitrator
from sensob import Sensob
from motob import Motob
from project6_supply.motors import Motors
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
    motob = Motob()
    motob.motors.append(Motors())
    controller.motobs.append(motob)
    rs = ReflectanceSensors()
    rsob = Sensob(rs)
    swl = StayWithinLines(controller, rsob)
    controller.add_behavior(swl)
    controller.activate_behavior(swl)
    while not controller.halt:
        controller.run_one_timestep()
