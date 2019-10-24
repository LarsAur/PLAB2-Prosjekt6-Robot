"""Selects behaviors"""
class Arbitrator():
    """Selects behaviors based weight"""

    def __init__(self, BBCON):
        """Initializes a Arbitrator, with a bbcon with behaviors to select actions from"""
        self.bbcon = BBCON

    def choose_action(self):
        """selects the behavior from BBCONs active_behaviors with the highest weight and returns
            a tuple containing (halt_request, [motor_recommendations])"""
        selected_behavior = self.bbcon.behaviors[0]
        for behavior in self.bbcon.behaviors:
            if behavior.weight > selected_behavior.weight:
                selected_behavior = behavior

        return (selected_behavior.halt_request, selected_behavior.motor_recommendations)