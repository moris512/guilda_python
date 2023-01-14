from controller import Controller
import numpy as np

class ControllerBroadcastPIAGC(Controller):
# モデル  ：AGCコントローラ
# 親クラス：Controllerクラス
# 実行方法：obj =　ControllerBroadcastPIAGC(net, y_idx, u_idx, Kp, Ki)
# 　引数　：・ net  : power_networkクラスのインスタンス。付加する対象の系統モデル
# 　　　　　・y_idx : float配列。観測元の機器の番号
# 　　　　　・u_idx : float配列。入力先の機器の番号
# 　　　　　・　Kp  ： float値。Pゲイン(ネガティブフィードバックの場合負の値に)
# 　　　　　・　Ki  ： float値。Iゲイン(ネガティブフィードバックの場合負の値に)
# 　出力　：controllerクラスのインスタンス
    def __init__(self, net, y_idx, u_idx, Kp, Ki):
        super().__init__(u_idx, y_idx)
        self.Ki = Ki
        self.Kp = Kp
        self.K_input = np.ones([len(self.index_input), 1])/len(self.index_input)
        self.K_observe = np.ones([len(self.index_observe), 1])/len(self.index_observe)
        self.net = net
    
    def get_nx(self):
        return 1

    # xは縦ベクトル
    # Xはlistを想定
    # Xの要素は、ある時刻における各バスの発電機の状態（縦ベクトル）
    def get_dx_u(self, x, X, t=None, V=None, I=None, u_global=None):
        # 各発電機の角周波数偏差を格納する縦ベクトル
        omega = np.zeros([len(X), 1])
        for i in range(len(X)):
            omega[i] = X[i][0][1,0]
        
        omega_mean = sum(omega*self.K_observe[:]).reshape(-1, 1)
        dx = omega_mean
        # 2×(K_inputの要素数)
        u = np.kron(np.array([0,1]), self.K_input[:]*(self.Ki*(x.reshape(-1,1)) + self.Kp*omega_mean)).T
        # 列ベクトルに整形
        u = np.vstack((u[:,[i]] for i in range(u.shape[1])))
        return [dx, u]

    def get_dx_u_linear(self, x, X, t=None, V=None, I=None, u_global=None):
        return self.get_dx_u(x, X, t, V, I, u_global)

    def get_linear_matrix(self):
        A = np.zeros([1,1])

    def get_signals(self, X=None, V=None):
        return []

    def set_Kp(self, Kp):
        if type(Kp)==int or type(Kp)==float:
            self.Kp = Kp
        else:
            raise TypeError('Kp must be int or float')

    def set_Ki(self, Ki):
        if type(Ki)==int or type(Ki)==float:
            self.Ki = Ki
        else:
            raise TypeError('Ki must be int or float')

    def set_K_input(self, K_input):
        if len(K_input) == len(self.index_input):
            self.K_input = K_input
        else:
            raise TypeError('The number of elements in K_input must match the number of elements in index_input.')

    def set_K_observe(self, K_observe):
        if len(K_observe) == len(self.index_observe):
            self.K_observe = K_observe
        else:
            raise TypeError('The number of elements in K_observe must match the number of elements in index_observe.')