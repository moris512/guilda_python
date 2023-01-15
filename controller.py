from abc import ABCMeta, abstractmethod
import numpy as np

class Controller(metaclass=ABCMeta):
    # 引数は入力、観測するバスの番号
    # 0スタートを想定
    # [0, 3, 8]のようにリストで横ベクトル形式（1次元）で記述
    def __init__(self, index_input, index_observe):
        self.__index_all = None
        self._get_dx_u_func = None

        if type(index_input) == np.ndarray:
            index_input = index_input.flatten().tolist()
        if type(index_observe) == np.ndarray:
            index_observe = index_observe.flatten().tolist()
        self.index_input = index_input
        self.index_observe = index_observe
        

    def get_x0(self):
        return np.zeros([self.get_nx(), 1])

    # t : 時刻
    # x : コントローラの状態（列ベクトル）
    # X : 各バスに接続された機器の状態(arrayを要素とするlist)
    # V : 各バスの電圧
    # I : 各バスの電流
    # U : グローバルコントローラによって各バスに印加される入力信号
    # X,Uは縦に収納されたリスト
    # V,Iは横に収納(1次元配列)されたリストと想定

    # out.Xやout.V等はバスの数だけ要素を持つlistで、１つ１つの要素は対応するバスの時刻変遷(array)
    # この関数の引数のX,Vは、上のlistのうち観測や入力を行う要素のarrayを集めたlist
    def get_input_vectorized(self, t, x, X, V, I, U):
        # ある時刻iにおける値(状態等)を列ベクトル(array)にして返す関数オブジェクト
        # XiとUiは各バスの列ベクトルを縦に並べたリスト
        # ViとIiは各バスの列ベクトルを横に並べたリスト
        Xi = lambda i: list(map(lambda x: [x[0][i, :].reshape(-1, 1)], X))
        Vi = lambda i: np.hstack(tuple(map(lambda v: v[i, :].reshape(-1, 1), V)))
        Ii = lambda j: np.hstack(tuple(map(lambda i: i[j, :].reshape(-1, 1), I)))
        Ui = lambda i: list(map(lambda u: [u[0][i, :].reshape(-1, 1)], U))

        [_, u] = self.get_dx_u_func(t[0, 0], x[0, :].reshape(-1, 1), Xi(0), Vi(0), Ii(0), Ui(0))

        # t,uは2次元配列で列ベクトルであることを想定
        uout = np.zeros([len(t), len(u)])
        uout[0,:] = u.reshape(1, -1)

        for i in range(1,len(t)):
            [_, u] = self.get_dx_u_func(t[i, 0], x[i, :].reshape(-1, 1), Xi(i), Vi(i), Ii(i), Ui(i))
            uout[i,:] = u.reshape(1, -1)

        return uout
        

    # listで状態の名前を返す
    # 列ベクトルに相当するlistであることに注意(nx×1)
    def get_state_name(self):
        x_name = [['x' + str(i+1)] for i in range(self.get_nx())]
        return x_name

    # index_allは横のリストで返していることに注意
    @property
    def index_all(self):
        self.__index_all = list(set(self.index_observe + self.index_input))
        return self.__index_all

    @property
    def get_dx_u_func(self):
        return self._get_dx_u_func
    
    @get_dx_u_func.setter
    def get_dx_u_func(self, func):
        if not callable(func):
            raise TypeError('given funcition must be callable')
        self._get_dx_u_func = func


    @abstractmethod
    def get_dx_u(self, t, x, X, V, I, U_global):
        pass

    @abstractmethod
    def get_nx(self):
        pass