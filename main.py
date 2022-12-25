import numpy as np
from scipy.optimize import root
from cmath import phase
from bus import BusSlack, BusGenerator, BusLoad
from power_network import PowerNetwork

x0 = np.array([1, 0, 1, 0, 1, 0])
y12 = 1.3652 - 11.6040j
y23 = -10.5107j
Y =  np.array([[y12 , -y12   , 0],
               [-y12, y12+y23, -y23],
               [0   , -y23   , y23]])

a_bus = [None] * 3
a_bus[0] = BusSlack(2, 0)
a_bus[1] = BusLoad(-3, 0)
a_bus[2] = BusGenerator(0.5, 2)

net = PowerNetwork()


xsol2 = root(lambda x: net.func_power_flow(x, Y, a_bus), x0, method="hybr")

"""
現状メモ
func_power_flow(x0, Y, a_bus) は計算できるようになった。
しかし、おそらくroot() の引数 x のサイズが(6, )でなければならないので、
現状の (6, 1) とマッチしていない.
"""



[V, I, P, Q] = net.helper(xsol2.x, Y)
# Vabs = list(map(abs, V))
# Vangle = list(map(phase, V))
#
# print('Vabs', Vabs)
# print('Vangle', Vangle)
# print('P', P)
# print('Q', Q)
#




