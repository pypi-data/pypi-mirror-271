import sys
import os
lib_path = (os.path.split(os.path.realpath(__file__))[0])
sys.path.append(lib_path)
import numpy as np
from My_machine_learning import *
##########混淆图##############
def hxt():
    # classes表示不同类别的名称，比如这有6个类别
    classes = ['hlj','jl','ln']
    cm =np.array([[18,1,3]
          ,[1,19,0]
          ,[1,0,17]])
    print(type(cm))
    plot_confusion_matrix(cm, classes,dpi=300,savename='confusion_matrix.png',title='')
##########pls——test##############
def pls_test(X,y, cv=11, split_flag = 0,test_size=0.2):
    ##split_flag为0，使用KS方法，为1使用SPXY方法
    if split_flag == 0:
        X_train, X_test, y_train, y_test = KS(X, y, test_size)
    elif split_flag == 1:
        X_train, X_test, y_train, y_test = SPXY(X, y, test_size)
    ##########################################################
    plt.figure(figsize=(8, 6), tight_layout=True)
    # with plt.style.context(('ggplot')):
    #     plt.plot(X_train.T)
    #     plt.xticks(range(0, X.shape[1], 30, ), rotation=45, weight='bold')
    #     plt.xlabel('Wavelength (nm)')
    #     plt.ylabel('D2 Absorbance')
    #     plt.show()
    pls_opt = optimise_pls_cv(X_train, y_train,40,cv,plot_components=True)
    print('model:', pls_opt)
    ####测试集############
    # Fir to the entire dataset
    y_test_pre = pls_opt.predict(X_test)
    # Cross-validation
    # Calculate scores for calibration and cross-validation
    score_pre1 = r2_score(y_test, y_test_pre)
    # Calculate mean squared error for calibration and cross validation
    mse_pre1 = mean_squared_error(y_test, y_test_pre)
    rmse_pre1 = np.sqrt(mse_pre1)
    print('R2 score_pre: %5.4f' % (score_pre1))
    print('MSE score_pre: %5.4f' % (mse_pre1))
    print('RMSE score_pre: %5.4f' % (rmse_pre1))

#将要转换的txt文件放到地址位path的文件夹中
def changeTo_utf8(path):
    change_to_utf8('path')

def KS(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = ks(X, y, test_size)
    return X_train, X_test, y_train, y_test
def SPXY(X, y, test_size=0.2):
    X_train, X_test, y_train, y_test = spxy(X, y, test_size)
    return X_train, X_test, y_train, y_test


##############数据预处理################################
def plotSpectrum(spec, title='原始光谱', x=0, m=5):
    """
    :param spec: shape (n_samples, n_features)
    :return: plt
    """
    p = Pretreatment()
    plt = p.PlotSpectrum(spec, title, x, m)
    return plt

def mean_Centralization(sdata):
    """
    均值中心化
    """
    p = Pretreatment()
    new_data = p.mean_centralization(sdata)
    return new_data

def standardLize(sdata):
    """
    标准化
    """
    p = Pretreatment()
    new_data = p.standardlize(sdata)
    return new_data

def msC(sdata):
    p = Pretreatment()
    new_data = p.msc(sdata)
    return new_data

def De1(sdata):
    """
    一阶差分
    """
    p = Pretreatment()
    new_data = p.D1(sdata)
    return new_data
#
def De2(sdata):
    """
    二阶差分
    """
    p = Pretreatment()
    new_data = p.D2(sdata)
    return new_data
#
def snV(sdata):
    """
    标准正态变量变换
    """
    p = Pretreatment()
    new_data = p.snv(sdata)
    return new_data
#
def max_min_Normalization(sdata):
    """
    最大最小归一化
    """
    p = Pretreatment()
    new_data = p.max_min_normalization(sdata)
    return new_data
#
def vector_Normalization(sdata):
    """
    矢量归一化
    """
    p = Pretreatment()
    new_data = p.vector_normalization(sdata)
    return new_data
#
def sG(sdata):
    # eg:sg = p.sG(x, 4*5+1,2*3,2)
    """
    SG平滑
    待处理
    """
    p = Pretreatment()
    new_data = p.SG(sdata)
    return new_data

def wAVE(data_x):  # 小波变换
    p = Pretreatment()
    new_data = p.wave(data_x)
    return new_data

def move_Avg(data_x, n=15, mode="valid"):
    # 滑动平均滤波
    p = Pretreatment()
    new_data = p.move_avg(data_x,n,mode)
    return new_data
##############数据预处理################################

# if __name__ == '__main__':
    # # X = np.ones((10,10))
    # # y = np.zeros((10,1))
    # # X_train, X_test, y_train, y_test = KS(X,y)
    #
    # x = np.random.random((100,1000))
    # # p = Pretreatment()
    # # sg = p.SG(x, 4*5+1,2*3,2)
    # # d1 = p.D1(x)
    # plotSpectrum(x)
    # x1 = sG(x)
    # x2 = sG(x)
    # plotSpectrum(x1,'1')
    # plotSpectrum(x2,'2')
    # plt.show()
    # print("ok")
if __name__ == '__main__':
    hxt()
    # data = pd.read_excel(
    #     r"D:\qiaozhiqi\project\基于多维度的人参分选系统开发项目\20220729\data\rg_data.xlsx"
#     #     , sheet_name='all104',index_col='Primary ID')
#     data = pd.read_excel(
#         r"./rg_data.xlsx"
#         , sheet_name='HSI104', index_col='Primary ID')
#     #######################spxy划分样本家######################
#     # print(data.shape)
#     X = data.values[:, 2:]
#
#     # X = ml.snV(X)
#     # print(X.shape)
#     y = data['Rg1+Re'].values
#     y = data.values[:, 0:2]
#
#     # print(y.shape)
#     # print(type(X))
#     # print(type(y))
#     #######################pls######################
#     pls_test(X,y,11,0)
#     print()
#     pls_test(X,y,11,1)
# #