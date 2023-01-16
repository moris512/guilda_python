import numpy as np

class Component():
    def __init__(self) -> None:
        pass

class ComponentEmpty(Component):

    def __init__(self):
        self.x_equilibrium = None

    def set_equilibrium(self, V_eq, I_eq):
        self.x_equilibrium = np.array([]).reshape(-1, 1)

    def get_nu(self):
        return 0

    def get_dx_constraint(*arg, **kwargs):
        dx = np.array([]).reshape(-1,1)
        I = np.zeros([2, 1])
        return [dx, I]

    def get_dx_constraint_linear(*args, **kwargs):
        dx = np.array([]).reshape(-1,1)
        I = np.zeros([2, 1])
        return [dx, I]

    def get_linear_matrix(self, *args, **kwargs):
        A = np.array([]).reshape(-1,1)
        B = np.array([]).reshape(-1,1)
        C = np.zeros([2, 0])
        D = np.zeros([2, 0])
        BV = np.zeros([0, 2])
        DV = np.zeros([2, 2])
        R = np.array([]).reshape(-1,1)
        S = np.array([]).reshape(-1,1)
        DI = -np.identity(2)
        BI = np.zeros([0, 2])

        return [A, B, C, D, BV, DV, BI, DI, R, S]
        