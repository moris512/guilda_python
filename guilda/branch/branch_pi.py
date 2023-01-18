from guilda.branch.branch import Branch
import numpy as np


class BranchPi(Branch):
    '''モデル ：対地静電容量をもつ送電線のπ型回路モデル
    '''


    # restrictions: SetAccess = public

    def __init__(self, from_: int, to: int, x, y: float):
        """モデル ：対地静電容量をもつ送電線のπ型回路モデル

        Args:
            from_ (_type_): 接続する母線番号
            to (_type_): 接続する母線番号
            x (_type_): [1*2 double]の配列。インピーダンスの実部、虚部を並べた配列。
            y (_type_): double値。対地静電容量の値
        """ 
        super().__init__(from_, to)

        if type(x) == list:
            x = complex(x[0], x[1])
        self.x = x
        self.y = y

    def get_admittance_matrix(self):
        x = self.x
        y = self.y
        Y = np.array(([complex(1/x,y), -1/x          ],
                      [-1/x          , complex(1/x,y)]))
        return Y
