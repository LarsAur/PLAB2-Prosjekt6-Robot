"""Ulike typer oppførsler roboten kan velge"""


class Behavior():
    """Superklassen til oppførselen"""

    def __init__(self, bbcon, sensob):
        self.bbcon = bbcon
        self.sensob = sensob
        self.motor_recommendations = None
        self.active_flag = False  # boolean - er oppførselen aktiv eller inaktiv
        self.halt_request = False  # oppførsel kan be roboten om å stanse all aktivitet
        self.match_degree = None  # hvor mye oppførselen matcher nåværende forhold
        self.weight = None

    def consider_deactivation(self):
        """Sjekker om oppførselen bør deaktiveres"""

    def consider_activation(self):
        """Sjekker om oppførselen bør aktiveres"""

    def update(self):
        """interface mellom bbcon og behavior"""

    def sense_and_act(self):
        """Gir motor recommendations utifra info fra sensobs"""


class StayWithinLines(Behavior):
    """Holder seg innenfor den svarte linjen"""

    PRIORITY = 1

    def consider_activation(self):
        """Skal alltid være aktiv"""
        return True

    def consider_deactivation(self):
        """Skal aldri deaktiveres"""
        return False

    def update(self):
        """Setter flagget til aktiv, kaller beregninger, setter vekt"""
        self.active_flag = True
        self.bbcon.activate_behavior(self)

        self.sense_and_act()

        self.weight = self.match_degree * StayWithinLines.PRIORITY

    def sense_and_act(self):
        """Beregner riktig oppførsel og setter motor_recommendations"""

        value = self.sensob[0].value

        if value == 'L':
            self.motor_recommendations = ('R', 30)
            self.match_degree = 4

        elif value == 'R':
            self.motor_recommendations = ('L', 30)
            self.match_degree = 4

        elif value == 'F':
            self.motor_recommendations = ('R', 90)
            self.match_degree = 4

        elif value == 'N':
            self.motor_recommendations = ('F', 0.2)
            self.match_degree = 1


class DoNotCrash(Behavior):
    """Hindrer at roboten kjører inn i ting"""

    PRIORITY = 3

    # tar in US som måler avstand i cm

    def consider_deactivation(self):
        """Deaktiveres når rødt objekt foran"""
        if self.bbcon.redObject:
            return True
        return False

    def consider_activation(self):
        """Aktiv dersom ikke rødt objekt foran"""
        if self.bbcon.redObject:
            return False
        return True

    def update(self):
        """Setter aktivt flagg, handler"""
        if self.consider_deactivation():
            self.active_flag = False
            self.bbcon.deactivate_behavior(self)
        else:
            self.active_flag = True
            self.bbcon.activate_behavior(self)

        self.sense_and_act()
        self.weight = self.match_degree * DoNotCrash.PRIORITY

    def sense_and_act(self):
        """Fortsetter å kjøre dersom rødt objekt eller ingenting foran"""

        distance = self.sensob[0].value

        if distance < 12:

            print("CLOSE")

            if not self.bbcon.closeObject:
                self.bbcon.closeObject = True
                self.motor_recommendations = ('F', 0)
                self.match_degree = 3

            else:
                if self.bbcon.redObject:  # dersom objektet er rødt, kjør
                    print("RED OBJECT FORWARD")
                    self.motor_recommendations = ('F', 0.2)
                    self.match_degree = 0
                else:
                    self.motor_recommendations = ('R', 45)  # hvis ikke, snu unna
                    self.match_degree = 3
        else:
            # hvis det ikke er noe foran, kjør
            self.bbcon.closeObject = False
            self.motor_recommendations = ('F', 0.2)
            self.match_degree = 1


class ChaseObject(Behavior):
    """Følger etter røde objekter"""

    PRIORITY = 1
    #sensobs: [US sensor, kamera]
    
    def consider_activation(self):
        """Aktiveres dersom det er røde objekter nærme"""
        if self.bbcon.redObject:
            return True
        
        if self.sensob[0].value < 12:
            print("DEBUG: activated camera")
            return True
        return False

    def consider_deactivation(self):
        if self.bbcon.redObject:
            return False
        
        if self.sensob[0].value > 12:
            return True
        return False

    def update(self):
        """Setter aktivt flagg, handler"""
        if self.consider_activation():
            
            self.active_flag = True
            self.bbcon.activate_behavior(self)

        else:
            self.active_flag = False
            self.bbcon.redObject = False
            self.bbcon.deactivate_behavior(self)

        self.sense_and_act()
        self.weight = self.match_degree * ChaseObject.PRIORITY

    def sense_and_act(self):
        """Hvis ser objektet, kjør"""

        if self.active_flag:
            
            if self.sensob[1].value: #dersom rødt objekt: kjører, setter redObject til true
                self.bbcon.redObject = True
                self.motor_recommendations = ('F', 0.2)
                self.match_degree = 10
            
            else: #dersom ikke rødt: stopper, setter redObject til false
                self.bbcon.redObject = False
                self.motor_recommendations = ('F', 0)
                self.match_degree = 0

        #dersom ikke aktiv: dårlig match, stopper
        self.motor_recommendations = ('F', 0)
        self.match_degree = 1
