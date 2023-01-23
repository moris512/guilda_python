import numpy as np
from numpy.linalg import inv
from scipy.optimize import root
from  cmath import phase

from bus.bus import Bus
from branch.branch import Branch
from typing import *

from scipy.linalg import block_diag

from power_network.simulate_options import SimulateOptions
from utils.io import from_dict
from utils.data import expand_complex_arr


class PowerNetwork(object):
    
    def __init__(self):
        
        self.a_bus: List[Bus] = []
        self.a_branch: List[Branch] = []
        self.a_controller_local = []
        self.a_controller_global = []

    @property
    def x_equilibrium(self):
        return [b.component.x_equilibrium for b in self.a_bus]
    
    @property
    def V_equilibrium(self):
        return [b.V_equilibrium for b in self.a_bus]
    
    @property
    def I_equilibrium(self):
        return [b.I_equilibrium for b in self.a_bus]
    

    def add_bus(self, bus):
        if type(bus) != list:
            bus = [bus]

        for b in bus:
            if isinstance(b, Bus):
                self.a_bus.append(b)
            else:
                print("Type must a child of Bus")

    def add_branch(self, branch):
        if type(branch) != list:
            branch = [branch]

        for b in branch:
            if isinstance(b, Branch):
                self.a_branch.append(b)
            else:
                print("Type must a child of Branch")


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
            self.a_bus[idx].set_equilibrium(V[idx][0],I[idx][0])

    def initialize(self):
        V, I = self.calculate_power_flow()
        self.set_equilibrium(V, I)

    def get_sys(self):
        #A, B, C, D, BV, DV, BI, DI, R, S
        mats = [[] for _ in range(10)]
        for b in self.a_bus:
            mat = b.component.get_linear_matrix()
            for i in range(len(mats)):
                if mat[i].shape == (0,0):
                    continue
                mats[i].append(mat[i])
        [A, B, C, D, BV, DV, BI, DI, R, S] = list(map(lambda mat: block_diag(*mat), mats))
        nI = C.shape[0]
        nx = A.shape[0]


        nV = BV.shape[1]
        nd = R.shape[1]
        nu = B.shape[1]
        nz = S.shape[0]
        [_, Ymat] = self.get_admittance_matrix()

        A11 = A
        A12 = np.hstack([BV, BI])
        A21 = np.vstack([C, np.zeros((nI, nx))])
        A22 = np.block([[DV, DI], [Ymat, -np.eye(nI)]])
        B1  = np.hstack([B, R])
        B2  = np.block([[D, np.zeros([nV, nd])], [np.zeros([nI, nu+nd])]])
        C1  = np.vstack([np.eye(nx), S, np.zeros([nI+nV, nx])])
        C2  = np.vstack([np.zeros([nx+nz, nV+nI]), np.eye(nV+nI)])

        A_  = A11-A12 @ inv(A22) @ A21
        B_  = B1-A12 @ inv(A22) @ B2
        C_  = C1-C2 @ inv(A22) @ A21
        D_  = -C2 @ inv(A22) @ B2
        return [A_, B_, C_, D_]

    def simulate(
        self, 
        t: Tuple[float, float], 
        u: List[float] = None, 
        idx_u: List[int] = None, 
        options: Union[SimulateOptions, Dict[str, Any]] = {}, 
        **kwargs):
        
        # process options
        if isinstance(options, dict):
            options = from_dict(SimulateOptions, {**options, **kwargs})
        elif (isinstance(options, SimulateOptions)):
            for k, v in kwargs.items:
                options.__setattr__(k, v)
        else:
            raise TypeError()
        options.set_parameter_from_pn(self)
        
        # process u and index of u
        if u is None:
            u = []
        if idx_u is None:
            idx_u = []
        
        out = self.solve_odes(t, u, idx_u,
                                options.fault,
                                options.x0_sys,
                                options.x0_con_global,
                                options.x0_con_local,
                                expand_complex_arr(options.V0),
                                expand_complex_arr(options.I0),
                                options.linear,
                                options)
            
        # simulate
        # TODO......
        
    

    