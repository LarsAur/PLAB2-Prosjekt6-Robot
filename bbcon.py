class BBCON:

    def __init__(self):
        self.behaviors = []
        self.active_behaviors = []
        self.sensobs = []
        self.motobs = []
        self.arbitrator = Arbitrator(self)

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
            """TODO: """
            sensob.values
        self.arbitrator.choose_action()

        for motob in self.motobs:

