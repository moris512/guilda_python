import numpy as np
from numpy.linalg import norm
from component import ComponentEmpty
from cmath import phase

class Bus():
    def __init__(self, shunt):
        self.component = ComponentEmpty()
        self.shunt = shunt

class BusSlack(Bus):
    def __init__(self, Vabs, Vangle, shunt):
        super().__init__(shunt)
        self.Vabs = Vabs
        self.Vangle = Vangle

    def get_constraint(self, Vr, Vi, P, Q):
        Vabs = np.array([ norm([Vr, Vi]) ])
        Vangle = np.array([ phase(complex(Vr, Vi)) ])
        return np.array([Vabs-self.Vabs, Vangle-self.Vangle])

class BusPV(Bus):
    def __init__(self, P, Vabs, shunt):
        super().__init__(shunt)
        self.P = P
        self.Vabs = Vabs

    def get_constraint(self, Vr, Vi, P, Q):
        Vabs = np.array([ norm([Vr, Vi]) ])
        return np.array([P-self.P, Vabs-self.Vabs])

class BusPQ(Bus):
    def __init__(self, P, Q, shunt):
        super().__init__(shunt)
        self.P = P
        self.Q = Q

    def get_constraint(self, Vr, Vi, P, Q):
        return np.array([P-self.P, Q-self.Q])


