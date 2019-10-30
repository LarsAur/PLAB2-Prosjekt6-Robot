"""Ulike typer oppførsler roboten kan velge"""


class Behavior():

    def __init__(self, bbcon, sensobs):
        self.bbcon = bbcon
        self.sensobs = sensobs
        self.motor_recommendations
        self.active_flag #boolean - er oppførselen aktiv eller inaktiv
        self.halt_request #oppførsel kan be roboten om å stanse all aktivitet
        self.match_degree #hvor mye oppførselen matcher nåværende forhold
        self.weight

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass

    def update(self):
        """interface mellom bbcon og behavior"""
        #oppdaterer aktivitetsstatus
        #self.sense_and_act()
        #self.weight = self.priority * self.match_degree

        pass

    def sense_and_act(self):
        #benytter sensob-verdier til å utføre motoranbefalinger
        #self.match_degree
        pass


class StayWithinLines(Behavior):
    """Holder seg innenfor den svarte linjen"""

    PRIORITY = 3

    def __init__(self, bbcon, sensobs):
        self.bbcon = bbcon
        self.sensobs = sensobs #tar inn objekter fra IR-sensor
        self.motor_recommendations
        self.active_flag = False
        self.halt_request = False
        self.match_degree
        self.weight


    def consider_activation(self):
        return True

    def consider_deactivation(self):
        pass

    def update(self):
        if self.consider_activation():
            self.active_flag = True

        self.sense_and_act(self)

        self.weight = self.match_degree * self.priority

    def sense_and_act(self):
        array = self.sensobs.get_value() #tar inn et array med 6 elementer
        none_black = True

        for i in len(array):
            if array[i] > 0.3:
                none_black = False

        if none_black:
            self.motor_recommendations = ('F', 1)
            self.match_degree = 3

        else:
            darkest_area = array.min()

            if array.index(darkest_area) == 0 | array.index(darkest_area) == 1 | array.index(darkest_area) == 2:
                self.motor_recommendations = ('R', 30)

            elif array.index(darkest_area) == 3 | array.index(darkest_area) == 4 | array.index(darkest_area) == 5:
                self.motor_recommendations = ('L', 30)

            self.match_degree = 3

        return









