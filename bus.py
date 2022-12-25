import numpy as np
from numpy.linalg import norm
from component import ComponentEmpty, Component
from cmath import phase

class Bus():
    V_equilibrium = None
    I_equilibrium = None

    def __init__(self, shunt):
        self.component = ComponentEmpty()
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
        #self.component.set_equilibrium(Veq, Ieq)

    def set_component(self, component):
        if isinstance(component, Component):
            self.component = component
            if not self.V_equilibrium:
                pass
                #self.component.set_equilibrium(self.V_equilibrium,self.I_equilibrium)
        else:
            raise TypeError("must be a child of component")

    def set_shunt(self, shunt):
        if type(shunt) == list:
            shunt = complex(shunt[0],shunt[1])
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
