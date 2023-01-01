import numpy as np
from math import sin, cos, atan, atan2, sqrt

from component import Component
from governor import Governor
from avr import Avr

class GeneratorBase(Component):
# モデル  ：同期発電機の一軸モデル
#         ・状態：３つ「回転子偏角"δ",周波数偏差"Δω",内部電圧"E"」
#               *PSSは付加されていない
#         ・入力：２ポート「AVRへ入力"u_avr", 機械入力"Pmech"」
#               *定常値からの偏差を指定
# 親クラス：componentクラス
# 実行方法：obj =　GeneratorBase(omega, parameter)
# 　引数　：・omega     : float値．系統周波数(50or60*2pi)
# 　　　　　・parameter : dict型．「'Xd', 'Xd_prime','Xq','T','M','D'」をkeyとして定義
# 　出力　：componentクラスのインスタンス

    def __init__(self, omega, parameter):
        # parameterは辞書タイプで収納
        self.x_equilibrium = None
        self.V_equilibrium = None
        self.I_equilibrium = None
        self.alpha_st = None
        self.avr = Avr()
        self.governor = Governor()
        self.omega0 = omega

        if type(parameter) != dict:
            raise TypeError('parameter must be dictionary')
        else:
            # 入力された辞書を受け取る
            # 該当の発電機のパラメータが辞書の値で数値のみ
            # OK {'Xd' : 0.1}
            # NG {'Xd' : [0.1]}
            self.parameter = parameter

    def get_x_name(self):
        gen_state = ['delta', 'omega', 'Ed']
        avr_state = self.avr.get_state_name()
        governor_state = self.governor.get_state_name()
        name_tag = gen_state + avr_state + governor_state
        return name_tag

    def get_port_name(self):
        return ['Vfd', 'Pm']

    def get_nx(self):
        out = 3 + self.avr.get_nx() + self.governor.get_nx()
        return out
    
    def get_nu(self):
        return 2

    # x、dx, uはndarrayの横ベクトル(１次元)であることを想定
    # conは縦ベクトル(2次元)
    def get_dx_constraint(self, t, x, V, I, u):
        omega0 = self.omega0
        Xd = self.parameter['Xd']
        Xdp = self.parameter['Xd_prime']
        Xq = self.parameter['Xq']
        Tdo = self.parameter['T']
        M = self.parameter['M']
        d = self.parameter['D']
        nx = 3
        nx_avr = self.avr.get_nx()
        nx_gov = self.governor.get_nx()

        x_gen = x[0:nx]
        x_avr = x[nx:nx+nx_avr]
        x_gov = x[nx+nx_avr:nx+nx_avr+nx_gov]

        Vabs = abs(V)
        Vangle = atan2(V.imag, V.real)

        delta = x_gen[0]
        omega = x_gen[1]
        E = x_gen[2]

        Vabscos = V.real*cos(delta) + V.imag*sin(delta)
        Vabssin = V.real*sin(delta) - V.imag*cos(delta)

        Ir =  (E-Vabscos)*sin(delta)/Xdp + Vabssin*cos(delta)/Xq
        Ii = -(E-Vabscos)*cos(delta)/Xdp + Vabssin*sin(delta)/Xq

        con = np.array([[I.real],[I.imag]]) - np.array([[Ir], [Ii]])

        Efd = Xd*E/Xdp - (Xd/Xdp - 1)*Vabscos

        [dx_avr, Vfd] = self.avr.get_Vfd(x_avr, Vabs, Efd, u[1])
        [dx_gov, P] = self.governor.get_P(x_gov, omega, u[2])

        dE = (-Efd + Vfd)/Tdo
        ddelta = omega0*omega
        domega = (P - d*omega - Vabs*E*sin(delta-Vangle)/Xdp + Vabs**2*(1/Xdp-1/Xq)*sin(2*(delta-Vangle))/2)/M

        dx = np.array([ddelta, domega, dE, dx_avr, dx_gov])

        return [dx, con]

    def set_avr(self, input_avr):
        if issubclass(input_avr, Avr):
            self.avr = input_avr()
        else:
            raise TypeError('input_avr must be subclass of Avr class')

    def set_governor(self, input_gov):
        if issubclass(input_gov, Governor):
            self.governor = input_gov()
        else:
            raise TypeError('input_gov must be subclass of Governor class')
    
    '''
    def initialize_net(self):
        # 怪しい
        if self.net != None:
            self.net.initialize(False)
    '''

    def set_equilibrium(self, V, I):
        Vabs = abs(V)
        Vangle = atan2(V.imag, V.real)
        Pow = I.conjugate() * V
        P = Pow.real
        Q = Pow.imag
        Xd = self.parameter['Xd']
        Xdp = self.parameter['Xd_prime']
        Xq = self.parameter['Xq']
        delta = Vangle + atan(P/(Q+Vabs**2/Xq))
        Enum = Vabs**4 + Q**2*Xdp*Xq + Q*Vabs**2*Xdp + Q*Vabs**2*Xq + P**2*Xdp*Xq
        Eden = Vabs*sqrt(P**2*Xq**2 + Q**2*Xq**2 + 2*Q*Vabs**2*Xq + Vabs**4)
        E = Enum/Eden
        Vfd = Xd*E/Xdp - (Xd/Xdp-1)*Vabs*cos(delta-Vangle)
        x_avr = self.avr.initialize(Vfd, Vabs)
        x_gov = self.governor.initialize(P)
        x_st = np.array([delta, 0, E, x_avr, x_gov])
        self.alpha_st = np.array([P, Vfd, Vabs])
        self.x_equilibrium = x_st
        self.V_equilibrium = V
        self.I_equilibrium = I
        return x_st
