from guilda.bus.bus import Bus
import numpy as np
from numpy.linalg import norm
from cmath import phase


class BusSlack(Bus):
    def __init__(self, Vabs, Vangle, shunt):
        super().__init__(shunt)
        self.Vabs = Vabs
        self.Vangle = Vangle

    def get_constraint(self, Vr, Vi, P, Q):
        Vabs = np.array([ norm([Vr, Vi]) ])
        Vangle = np.array([ phase(complex(Vr, Vi)) ])
        return np.array([Vabs-self.Vabs, Vangle-self.Vangle])
