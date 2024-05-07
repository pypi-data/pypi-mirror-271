import numpy as np
import pandas as pd
from pprint import pprint


class LSA:
    """
    滞后序列分析，python版
    """

    def __init__(self, code_set,k=1):
        """
        :param seqs: 编码的序列
        :param code_set: 编码类别集合，都有哪些编码行为类别
        """
        self.seqs = None
        self.code_set = list(code_set)
        self.code_length = len(code_set)
        self.k=k#滞后间隔控制
        #通过传入的编码类别初始化一个对应的二维值皆为0的矩阵
        self.transform_array = np.zeros([self.code_length, self.code_length])
        self.Z = np.zeros([self.code_length, self.code_length])

      #利用前面建立的transform_array初始矩阵对传入的二维表格数据进行频次统计
    def _get_frequency_array(self,output=True):
        for seq in self.seqs:
            if len(seq)>self.k:#根据滞后间隔k的数值进行行为数据读取和统计
                for i in range(len(seq) - self.k):
                    last_code = seq[i]
                    next_code = seq[i + self.k]
                    idx1 = self.code_set.index(last_code)
                    idx2 = self.code_set.index(next_code)
                    self.transform_array[idx1][idx2] += 1
        if output:
            pprint(pd.DataFrame(self.transform_array, columns=self.code_set, index=self.code_set))

    #利用频次表和前面传入的行为类别进行残差表值的求解
    def _adjusted_residual_z(self, output):
        array = self.transform_array #实际频数
        length = self.code_length #行为编码类别长度
        i = array.sum(axis=1) #对列进行操作，对行进行求和，求某一行为i在行为序列中发生在前的总次数
        j = array.sum(axis=0) #对行进行操作，对列进行求和，求某一行为j在行为序列中发生在后的总次数
        N = array.sum() #对相邻行为出现的总次数进行统计=总行为样本数-1
        eij = np.dot(i.reshape(length, 1), j.reshape(1, length)) / N  #期望频数，i*j/N
        i_minus = 1 - i / N #残差调整做准备
        j_minus = 1 - j / N #残差调整做准备
      #np.dot(i_minus.reshape([length, 1]), j_minus.reshape([1, length]))---用来做残差调整的矩阵，与期望频数相乘，再开根号，得到c_ij
        c_ij = np.sqrt(np.dot(i_minus.reshape([length, 1]), j_minus.reshape([1, length])) * eij)
        z_ij = (array - eij) / c_ij #求调整过后的残差值表=（实际-期望）/调整因子
        self.Z = z_ij.round(3) #保留小数
        self.Z_frame = pd.DataFrame(self.Z, columns=self.code_set, index=self.code_set) #转换成df类型，并添加行属性值和列属性值
        if output: #默认为True，若为False，就不打印
            pprint(self.Z_frame)

    def fit(self, seqs, output=True):
        """
        :param seqs: 序列
        :param output: 是否print输出，默认为True，若为False，就不打印
        :return:
        """
        self.seqs = seqs
        self._get_frequency_array(output)
        self._adjusted_residual_z(output)

if __name__ == '__main__':
    # 调用对象及函数
    data = [['A', 'A', 'B', 'A', 'B']]
    # 默认滞后间隔k=1，可根据自己的需要进行修改
    lsa = LSA(['A', 'B'], 1)
    lsa.fit(data)