from guilda.bus.bus import Bus
import numpy as np


class BusPQ(Bus):
    def __init__(self, P, Q, shunt):
        super().__init__(shunt)
        self.P = P
        self.Q = Q

    def get_constraint(self, Vr, Vi, P, Q):
        return np.array([P-self.P, Q-self.Q])
