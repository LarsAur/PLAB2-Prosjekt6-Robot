"""Ulike typer oppførsler roboten kan velge"""

class Behavior():

    def __init__(self, bbcon, sensobs):
        self.bbcon = bbcon
        self.sensobs = sensobs
        self.motor_recommendations = None
        self.active_flag = None # boolean - er oppførselen aktiv eller inaktiv
        self.halt_request = None # oppførsel kan be roboten om å stanse all aktivitet
        self.match_degree = None # hvor mye oppførselen matcher nåværende forhold
        self.weight = None

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
        self.motor_recommendations = None
        self.active_flag = False
        self.halt_request = False
        self.match_degree = None
        self.weight = None


    def consider_activation(self):
        return True

    def consider_deactivation(self):
        pass

    def update(self):
        if self.consider_activation():
            self.active_flag = True

        self.sense_and_act()

        self.weight = self.match_degree * StayWithinLines.PRIORITY

    def sense_and_act(self):
        line_direction = self.sensobs.values #tar inn et array med 6 elementer

        print(line_direction)

        """ none_black = True

        print(array)

        for i in range(len(array)):
            if array[i] < -1:
                none_black = False

        if none_black:
            self.motor_recommendations = ('F', 0.2)
            self.match_degree = 3

        else:
            darkest_area = min(array)

            if array.index(darkest_area) == 0 | array.index(darkest_area) == 1 | array.index(darkest_area) == 2:
                self.motor_recommendations = ('R', 30)

            elif array.index(darkest_area) == 3 | array.index(darkest_area) == 4 | array.index(darkest_area) == 5:
                self.motor_recommendations = ('L', 30)"""

        self.match_degree = 3 
        self.motor_recommendations = ('F', 0.2)









