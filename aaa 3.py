import pandas as pd
import pandas as pd
from numpy import pi

from power_network import PowerNetwork
from branch import BranchPi, BranchPiTransformer
from bus import BusPQ, BusPV, BusSlack
from generator import GeneratorBase
from avr import Avr


omega0 = 60*2*pi

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
    mac_i =  macs_df[macs_df['No_bus'] == i]
    if mac_i.empty:
        return
    gen = GeneratorBase(omega0, mac_i)
#    exc_i = excs_df[excs_df['No_bus'] == i]
    gen.set_avr(Avr())  # まだ exc 考慮していない
    return gen

