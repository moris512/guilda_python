import numpy as np

class Component():
    def __init__(self) -> None:
        pass

class ComponentEmpty(Component):
<<<<<<< Updated upstream
    def __init__(self) -> None:
        pass
=======
    def __init__(self):
        self.x_equilibrium = None

    def set_equilibrium(self, V_eq, I_eq):
        self.x_equilibrium = []

    def get_nu(self):
        return 0

    def get_dx_constraint(*arg):
        dx = []
        I = np.zeros([2, 1])
        return [dx, I]

    def get_dx_constraint_linear(*arg):
        dx = []
        I = np.zeros([2, 1])
        return [dx, I]

    def get_linear_matrix(self, *arg):
        A = []
        B = []
        C = np.zeros([2, 0])
        D = np.zeros([2, 0])
        BV = np.zeros([0, 2])
        DV = np.zeros([2, 2])
        R = []
        S = []
        DI = -np.identity(2)
        BI = np.zeros([0, 2])

        return [A, B, C, D, BV, DV, BI, DI, R, S]
        

class LoadCurrent(Component):
    def __init__(self):
        self.x_equilibrium = np.zeros(0, 1)
        self.V_equilibrium = None
        self.I_equilibrium = None
        self.Y = None
        self.R = []
        self.S = []
    
    def set_equilibrium(self, V_eq, I_eq):
        # 複素数表記で平衡点を取得
        self.V_equilibrium = V_eq
        self.I_equilibrium = I_eq
    
    def get_dx_constraint(self,  I, u, t=None, x=None, V=None):
        dx = np.zeros([0, 1])
        constraint = I - [[self.I_equilibrium.real * (1 + u[0])], \
                          [self.I_equilibrium.imag * (1 + u[1])]]

        return [dx, constraint]

    def get_dx_constraint_linear(self, x, V, I, u, t=None):
        [A, B, C, D, BV, DV, BI, DI, _, _] = self.get_linear_matrix_(x, V)
        dx = A@x + B@u + BI@np.array([[(I - self.I_equilibriumn).real], [(I - self.I_equilibrium).imag]]) + \
             BV@np.array([[(V - self.V_equilibrium).real], [(V - self.V_equilibrium).imag]])
        constraint = C@x + D@u + DI@np.array([[(I - self.I_equilibriumn).real], [(I - self.I_equilibrium).imag]]) + \
                    DV@np.array([[(V - self.V_equilibrium).real], [(V - self.V_equilibrium).imag]])
        
        return [dx, constraint]

    def get_nu(self):
        return 2

    def get_linear_matrix_(self, x=None, V=None):
        if V == None:
            [A, B, C, D, BV, DV, BI, DI, R, S] = self.get_linear_matrix_([], self.V_equilibrium)
        else:
            A = []
            B = np.zeros([0, 2])
            C = np.zeros([2, 0])
            D = np.diag([[self.I_equilibrium.real], [self.I_equilibrium.imag]])
            BV = np.zeros([0, 2])
            BI = np.zeros([0, 2])
            DV = np.zeros([2, 2])
            DI = -np.identity(2)
            R = self.R
            S = self.S

        return [A, B, C, D, BV, DV, BI, DI, R, S]

    def get_linear_matrix(self, *arg):
        # 怪しい
        varargout = list(map(self.get_linear_matrix_, arg))
        return varargout
>>>>>>> Stashed changes
