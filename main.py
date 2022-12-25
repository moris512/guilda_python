import numpy as np
from cmath import phase

from power_network import PowerNetwork
from bus import BusSlack, BusPV, BusPQ
from branch import BranchPi


y12 = 1.3652 - 11.6040j
y23 = -10.5107j

net = PowerNetwork()
net.add_bus(BusSlack(2, 0, 0))
net.add_bus(BusPQ(-3, 0, 0))
net.add_bus(BusPV(0.5, 2, 0))

a = BranchPi(1, 2, 1/y12, 0)

net.add_branch(BranchPi(1, 2, 1/y12, 0))
net.add_branch(BranchPi(2, 3, 1/y23, 0))


Y, _ = net.get_admittance_matrix()
V, I = net.calculate_power_flow()

PQ = V * I.conjugate()
P  = PQ.real
Q  = PQ.imag

print(P)
print(Q)
