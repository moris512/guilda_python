import numpy as np
from scipy.optimize import root
from  cmath import phase

from bus import Bus
from branch import Branch

class PowerNetwork():
    def __init__(self):
        self.x_equilibrium = None
        self.V_equilibrium = None
        self.I_equilibrium = None
        self.a_bus = []
        self.a_branch = []

    def add_bus(self, bus):
        if type(bus) != list:
            bus = [bus]

        for b in bus:
            if isinstance(b, Bus):
                self.a_bus.append(b)
            else:
                print("Type must a chile of Bus")

    def add_branch(self, branch):
        if type(branch) != list:
            branch = [branch]

        for b in branch:
            if isinstance(b, Branch):
                self.a_branch.append(b)
            else:
                print("Type must a chile of Branch")


    def get_admittance_matrix(self, a_index_bus=None):
        if not a_index_bus:
            a_index_bus = [i for i in range(len(self.a_bus))]

        n = len(self.a_bus)
        Y = np.zeros((n, n), dtype=complex)

        for br in self.a_branch:
            if (br.from_-1 in a_index_bus) and (br.to-1 in a_index_bus):
                Y_sub = br.get_admittance_matrix()
                Y[br.from_-1, br.from_-1] += Y_sub[0, 0]
                Y[br.from_-1, br.to-1]    += Y_sub[0, 1]
                Y[br.to-1, br.from_-1]    += Y_sub[1, 0]
                Y[br.to-1, br.to-1]       += Y_sub[1, 1]

        for idx in a_index_bus:
            Y[idx, idx] += self.a_bus[idx].shunt

        Ymat = np.zeros((2*n, 2*n))
        Ymat[ ::2, ::2] =  Y.real
        Ymat[ ::2,1::2] = -Y.imag
        Ymat[1::2, ::2] =  Y.imag
        Ymat[1::2,1::2] =  Y.real

        return [Y, Ymat]

    def calculate_power_flow(self):
        n = len(self.a_bus)

        def func_eq(Y, x):
            Vr = np.array([[x[i]] for i in range(0, len(x), 2)])
            Vi = np.array([[x[i]] for i in range(1, len(x), 2)])
            V = Vr + 1j*Vi

            I = Y @ V
            PQhat = V * I.conjugate()
            P  = PQhat.real
            Q  = PQhat.imag

            out = []
            for i in range(n):
                bus = self.a_bus[i]
                out_i = bus.get_constraint(V[i].real, V[i].imag, P[i], Q[i])
                out.extend(out_i[:, 0].tolist())
            return out

        Y, _ = self.get_admittance_matrix()
        x0 = [1, 0] * n

        ans = root(lambda x: func_eq(Y, x), x0, method="hybr")

        Vrans = np.array([[ans.x[i]] for i in range(0, len(ans.x), 2)])
        Vians = np.array([[ans.x[i]] for i in range(1, len(ans.x), 2)])
        Vans = Vrans + 1j*Vians

        Ians = Y @ Vans
        return [Vans, Ians]

    def set_equilibrium(self, V, I):
        for idx in range(len(self.a_bus)):
            self.a_bus[idx].set_equilibrium(V[idx],I[idx])

    def initialize(self):
        V, I = self.calculate_power_flow()
        self.set_equilibrium(V, I)



