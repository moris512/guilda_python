import numpy as np
from bus import Bus
from branch import Branch
from  cmath import phase

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

    def get_admittance_matrix(self, a_index_bus=None):
        if not a_index_bus:
            a_index_bus = [i for i in range(len(self.a_bus))]

        n = len(self.a_bus)
        Y = np.zeros(n, n)

        for br in self.a_branch:
            if (br.from_ in a_index_bus) and (br.to_ in a_index_bus):
                Y_sub = br.get_admittance_matrix()
                Y[br.from_, br.from_] += Y_sub[0, 0]
                Y[br.from_, br.to_]   += Y_sub[0, 1]
                Y[br.to_, br.from_]   += Y_sub[1, 0]
                Y[br.to_, br.to_]     += Y_sub[1, 1]

        for idx in a_index_bus:
            Y[idx, idx] += self.a_bus[idx].shunt

        Ymat = np.zeros(2*n, 2*n)
        Ymat[ ::2, ::2] = Y.real
        Ymat[ ::2,1::2] =-Y.imag
        Ymat[1::2, ::2] = Y.imag
        Ymat[1::2,1::2] = Y.real

        return [Y, Ymat]


    def add_branch(self, branch):
        if type(branch) != list:
            branch = [branch]

        for b in branch:
            if isinstance(b, Branch):
                self.a_branch.append(b)
            else:
                print("Type must a chile of Branch")


    def helper(self, x, Y):
        V = np.array([[complex(x[i], x[i+1])] for i in range(0, len(x), 2)])
        I = Y @ V


        PQhat = V * I.conjugate()
        P  = PQhat.real
        Q  = PQhat.imag
        return [V, I, P, Q]

    def func_power_flow(self, x, Y, a_bus):
        # x: V1.real, V1.imag, V2.real, V2.imag, V3.real, V3.imag,
        [V, I, P, Q] = self.helper(x, Y)
        n = len(a_bus)

        for i in range(n):
            bus = a_bus[i]
            out_i = bus.get_constraint(V[i].real, V[i].imag, P[i], Q[i])
            if i == 0:
                out = out_i
            else:
                out = np.vstack((out, out_i))

        return out


