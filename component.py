import numpy as np

class Component():
    def __init__(self) -> None:
        pass

class ComponentEmpty(Component):

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
