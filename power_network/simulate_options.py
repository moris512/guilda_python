
from dataclasses import dataclass
from typing import *
import numpy as np

from power_network.power_network import PowerNetwork

@dataclass
class SimulateOptions:
    
    linear: bool = False
    fault: List[Tuple[Tuple[float, float], List[int]]] = []
    
    x0_sys: complex = 0
    V0: complex = 0
    I0: complex = 0
    
    x0_con_local = []
    x0_con_global = []
    
    method: Union[Literal['zoh'], Literal['foh']] = 'zoh'
    AbsTol: float = 1e-8
    RelTol: float = 1e-8
    
    do_report: bool = False
    do_retry: bool = True
    reset_time: float = np.inf
    OutputFcn = []
    tools: bool = False
    
    def set_parameter_from_pn(self, pn: PowerNetwork):
        
        self.x0_sys = pn.x_equilibrium or 0
        self.V0 = pn.V_equilibrium or 0
        self.I0 = pn.I_equilibrium or 0
        
        self.x0_con_local = [c.get_x0() for c in pn.a_controller_local]
        self.x0_con_global = [c.get_x0() for c in pn.a_controller_global]
        
        # TODO controller
        
        
        
        