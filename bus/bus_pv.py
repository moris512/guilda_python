from bus.bus import Bus
import numpy as np
from numpy.linalg import norm


class BusPV(Bus):
    def __init__(self, P, Vabs, shunt):
        super().__init__(shunt)
        self.P = P
        self.Vabs = Vabs

    def get_constraint(self, Vr, Vi, P, Q):
        Vabs = np.array([ norm([Vr, Vi]) ])
        return np.array([P-self.P, Vabs-self.Vabs])
