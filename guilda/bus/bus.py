import numpy as np
from numpy.linalg import norm
from cmath import phase

from guilda.component import Component, ComponentEmpty

class Bus(object):

    def __init__(self, shunt):
        self.V_equilibrium = None
        self.I_equilibrium = None
        self.set_component(ComponentEmpty())
        self.set_shunt(shunt)

    def get_nx(self):
        return len(self.component.x_equilibrium)

    def get_nu(self):
        return len(self.component.get_nu())

    def set_equilibrium(self, Veq, Ieq):
        if type(Veq) == list:
            Veq = complex(Veq[0],Veq[0])
        if type(Ieq) == list:
            Ieq = complex(Ieq[0],Ieq[0])
        self.V_equilibrium = Veq
        self.I_equilibrium = Ieq
        self.component.set_equilibrium(Veq, Ieq)

    def set_component(self, component):
        if isinstance(component, Component):
            self.component = component
            if not self.V_equilibrium:
                return
            self.component.set_equilibrium(self.V_equilibrium, self.I_equilibrium)
        else:
            raise TypeError("must be a child of component")

    def set_shunt(self, shunt):
        if type(shunt) == list:
            shunt = complex(shunt[0],shunt[1])
        self.shunt = shunt
