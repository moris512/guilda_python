import pandas as pd
from numpy import pi

from power_network import PowerNetwork
from branch import BranchPi, BranchPiTransformer
from bus.bus_pq import BusPQ
from bus.bus_pv import BusPV
from bus.bus_slack import BusSlack
from generator.generator_1axis import Generator1Axis
from avr.avr import Avr
from load.load_current import LoadCurrent


mac_data = [[1, 1, 0.1,    0.031,  0.069, 10.2, 84,   4   ],
            [2, 3, 0.295,  0.0697, 0.282, 6.56, 60.4, 9.75]]
mac_cols = ['No_machine', 'No_bus', 'Xd', 'Xd_prime', 'Xq', 'T', 'M', 'D']
macs_df = pd.DataFrame(data=mac_data, columns=mac_cols)

exc_data = [[1, 0, 0.05],
            [3, 0, 0.05]]
exc_cols = ['No_bus', 'Ka', 'Te']
excs_df = pd.DataFrame(data=exc_data, columns=exc_cols)

pss_data = [[1, 0, 10, 0.05, 0.015, 0.08, 0.01],
            [3, 0, 10, 0.05, 0.015, 0.08, 0.01]]
pss_cols = ['No_bus', 'Kpss', 'Tpss', 'TL1p', 'TL1', 'TL2p', 'TL2']
psses_df = pd.DataFrame(data=pss_data, columns=pss_cols)

def get_generator(i):
    mac_i = macs_df[macs_df['No_bus'] == i]
    if mac_i.empty:
        raise TypeError("No data for creating generator %s" % i)
    g = Generator1Axis(omega0, mac_i)
    exc_i = excs_df[excs_df['No_bus'] == i]
    g.set_avr(Avr) # 現状は avr の引数なし
#    pss_i = pss_df[pss_df['No_bus'] == i]
#    g.set_pss(pss(pss_i))
    return g



omega0 = 60*2*pi
net = PowerNetwork()


# ブランチの定義
branch_data = [[1, 2, 0, 0.0576, 0, 1, 0],
               [3, 2, 0, 0.0625, 0, 1, 0]]
branch_cols = ["bus_from", "bus_to", "x_real", "x_imag", "y", "tap", "phase"]
branches_df = pd.DataFrame(data=branch_data, columns=branch_cols)

for i in range(len(branches_df)):
    branch_i = branches_df.loc[i]
    if branch_i['tap'] == 0:
        br = BranchPi(branch_i['bus_from'], branch_i['bus_to'], \
                      branch_i[['x_real', 'x_imag']].values.tolist(), branch_i['y'])
    else:
        br = BranchPiTransformer(branch_i['bus_from'], branch_i['bus_to'], \
                                 branch_i[['x_real', 'x_imag']].values.tolist(), branch_i['y'], \
                                 branch_i['tap'], branch_i['phase'])
    net.add_branch(br)


# バスの定義
bus_data = [[1, 1.00, 0, 0.60, 0, 0  , 0  , 0, 0, 'PV'],
            [2, 1.00, 0, 5.45, 0, 1.0, 1.0, 0, 0, 'PQ'],
            [3, 1.00, 0, 1.00, 2, 0  , 0  , 0, 0, 'slack']]

bus_cols = ['No', 'V_abs', 'V_angle', 'P_gen', 'Q_gen', 'P_load', 'Q_load', 'G_shunt', 'B_shunt', 'type']
bus_df = pd.DataFrame(data=bus_data, columns=bus_cols)


for i in range(len(bus_df)):
    bus_i = bus_df.loc[i]
    shunt = bus_i[['G_shunt', 'B_shunt']].values.tolist()
    if bus_i['type'] == 'slack':
        b = BusSlack(bus_i['V_abs'], bus_i['V_angle'], shunt)
        b.set_component(get_generator(i+1))
    elif bus_i['type'] == 'PV':
        b = BusPV(bus_i['P_load'], bus_i['V_abs'], shunt)
        b.set_component(get_generator(i+1))
    elif bus_i['type'] == 'PQ':
        P, Q = bus_i['P_load'], bus_i['Q_load']
        b = BusPQ(-P, -Q, shunt)
        if not (P == Q == 0):
            load = LoadCurrent()
            b.set_component(load)

    net.add_bus(b)

net.initialize()


