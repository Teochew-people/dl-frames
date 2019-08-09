import numpy as np
from sklearn import metrics
import os
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import torch


def reg_calculate(true, prediction):
    mse = metrics.mean_squared_error(true, prediction)
    rmse = np.sqrt(mse)
    mae = metrics.mean_absolute_error(true, prediction)
    r2 = metrics.r2_score(true, prediction)

    print("mse: {}, rmse: {}, mae: {}, r2: {}".format(mse, rmse, mae, r2))
    return mse, rmse, mae, r2


def clf_calculate(true, prediction):
    acc = metrics.accuracy_score(true, prediction)
    precision = metrics.precision_score(true, prediction, average='macro')
    recall = metrics.recall_score(true, prediction, average='macro')
    f1 = metrics.f1_score(true, prediction, average='macro')

    print('acc: {}, precision: {}, recall: {}, f1: {}'.format(acc, precision, recall, f1))
    return acc, precision, recall, f1


def confusion_matrix_result(true, prediction):
    cfm = confusion_matrix(true, prediction)
    return cfm


def create_dataset(dataset, look_back=7):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)


def train_test_split(X, y, test_size=0.2, random_state=19):
    np.random.seed(random_state)
    train_size = int(len(X) * (1 - test_size))
    p = np.random.permutation(X.shape[0])
    data = X[p]
    label = y[p]

    X_train, X_test = data[:train_size], data[train_size:]
    y_train, y_test = label[:train_size], label[train_size:]
    return X_train, X_test, y_train, y_test

# def create_dataset(dataset, test_size=0.2, look_back=7):
#
#     # 划分数据集
#     train_size = int(len(dataset) * (1-test_size))
#
#     if dataset.shape[1] == 1:
#         Train_dataset = dataset[:train_size]
#         Test_dataset = dataset[train_size:]
#
#         standard = StandardScaler()
#         standard.fit(Train_dataset)
#         Train_dataset = standard.transform(Train_dataset)
#         Test_dataset = standard.transform(Test_dataset)
#
#         # 构建数据集
#         Train_dataX, Train_dataY = [], []
#         Test_dataX, Test_dataY = [], []
#
#         for i in range(len(Train_dataset) - look_back):
#             a = Train_dataset[i:(i + look_back)]
#             Train_dataX.append(a)
#             Train_dataY.append(Train_dataset[i + look_back, -1:])
#
#         for i in range(len(Test_dataset) - look_back):
#             a = Test_dataset[i:(i + look_back)]
#             Test_dataX.append(a)
#             Test_dataY.append(Test_dataset[i + look_back, -1:])
#
#     else:
#         X_train = dataset[:train_size, :-1]
#         X_test = dataset[train_size:, :-1]
#
#         y_train = dataset[:train_size, -1:]
#         y_test = dataset[train_size:, -1:]
#
#         standard = StandardScaler()
#         standard.fit(X_train)
#         X_train_standard = standard.transform(X_train)
#         X_test_standard = standard.transform(X_test)
#
#         standard.fit(y_train)
#         y_train_standard = standard.transform(y_train)
#         y_test_satndard = standard.transform(y_test)
#
#         Train_dataset = np.c_[X_train_standard, y_train_standard, y_train]
#         Test_dataset = np.c_[X_test_standard, y_test_satndard, y_test]
#
#
#         # 构建数据集
#         Train_dataX, Train_dataY = [], []
#         Test_dataX, Test_dataY = [], []
#
#
#         for i in range(len(Train_dataset) - look_back):
#             a = Train_dataset[i:(i + look_back), :-1]
#             Train_dataX.append(a)
#             Train_dataY.append(Train_dataset[i + look_back, -1:])
#
#         for i in range(len(Test_dataset) - look_back):
#             a = Test_dataset[i:(i + look_back), :-1]
#             Test_dataX.append(a)
#             Test_dataY.append(Test_dataset[i + look_back, -1:])
#     return np.array(Train_dataX), np.array(Test_dataX), np.array(Train_dataY), np.array(Test_dataY)


def cross_entropy_erorr(y, t):
    delta = 1e-7
    return -torch.sum(t * torch.log(y + delta))


def save_ann_results(epoch, batch_size, lr, dropout, layer_numbers, hidden_layers, activate_function, value1, value2,
                     value3, value4, is_standrad, is_PCA, save_file, train_type):

    if train_type == 'regression':
        if not os.path.exists(save_file):
            content = 'epoch' + ',' + 'batch_size' + ',' + 'lr' + ',' + 'dropout' + ',' + 'hidden_layer_number' + ',' + 'hidden_neurons' + ',' \
                      + 'activate function' + ',' + 'mse' + ',' + 'rmse' + ',' + 'mae' + ',' + 'r2' + ',' + 'is_standard' + ',' + 'is_PCA'
            with open(save_file, 'a') as f:
                f.write(content)
                f.write('\n')
        content = str(epoch) + ',' + str(batch_size) + ',' + str(lr) + "," + str(dropout) + ',' + str(layer_numbers) +\
                  ',' + str(hidden_layers) + ',' + str(activate_function) + ',' + str(value1) + ',' + str(value2) + ',' \
                  + str(value3) + ',' + str(value4) + ',' + str(is_standrad) + ',' + str(is_PCA)
    if train_type == 'classification':
        if not os.path.exists(save_file):
            content = 'epoch' + ',' + 'batch_size' + ',' + 'lr' + ',' + 'dropout' + ',' + 'hidden_layer_number' + ',' + 'hidden_neurons' + ',' \
                      + 'activate function' + ',' + 'acc' + ',' + 'precision' + ',' + 'recall' + ',' + 'f1' + ',' + 'is_standard' + ',' + 'is_PCA'
            with open(save_file, 'a') as f:
                f.write(content)
                f.write('\n')
        content = str(epoch) + ',' + str(batch_size) + ',' + str(lr) + "," + str(dropout) + ',' + str(
            layer_numbers) + ',' \
                  + str(hidden_layers) + ',' + str(activate_function) + ',' + str(value1) + ',' + str(value2) + ',' + str(
            value3) + ',' + str(value4) + ',' + str(is_standrad) + ',' + str(is_PCA)
    with open(save_file, 'a') as f:
        f.write(content)
        f.write('\n')


def save_cnn_results(epoch, batch_size, lr, dropout, conv_layers, channle_numbers, conv_kernel_size, conv_stride, pooling_size, pooling_stride,
                 flatten, activate_function, mse, rmse, mae, r2, is_standrad, is_PCA, save_file):

    save_file = save_file
    if not os.path.exists(save_file):
        content = 'epoch' + ',' + 'batch_size' + ',' + 'lr' + ',' + 'dropout' + ',' + 'conv_layers' + ',' + \
                  'channle_numbers' + ',' + 'conv_kernel_size' + ',' + 'conv_stride' + ',' + 'pooling_kernel_size' + \
                  ',' + 'pooling_stride' + ',' + 'flatten' + ',' + 'activate function' + ',' + 'mse' + ',' + 'rmse' + \
                  ',' + 'mae' + ',' + 'r2' + ',' + 'is_standard' + ',' + 'is_PCA'
        with open(save_file, 'a') as f:
            f.write(content)
            f.write('\n')
    content = str(epoch) + ',' + str(batch_size) + ',' + str(lr) + "," + str(dropout) + ',' + str(conv_layers) + ',' + str(channle_numbers) + ',' \
              + str(conv_kernel_size) + ',' + str(conv_stride) + ',' + str(pooling_size) + ',' + str(pooling_stride) + ',' \
              + str(flatten) + ',' + str(activate_function) + ',' + str(mse) + ',' + str(rmse) + ',' + str(mae) + ',' + \
              str(r2) + ',' + str(is_standrad) + ',' + str(is_PCA)
    with open(save_file, 'a') as f:
        f.write(content)
        f.write('\n')


def save_lstm_results(epoch, batch_size, lr, dropout, num_layers, hidden_size, activate_function, mse, rmse, mae, r2, is_standrad, is_PCA, save_file):

    save_file = save_file
    if not os.path.exists(save_file):
        content = 'epoch' + ',' + 'batch_size' + ',' + 'lr' + ',' + 'dropout' + ',' + 'hidden_size' + ',' + 'hidden_size' + ','\
                  + 'activate function' + ',' + 'mse' + ',' + 'rmse' + ',' + 'mae' + ',' + 'r2' + ',' + 'is_standard' + ',' + 'is_PCA'
        with open(save_file, 'a') as f:
            f.write(content)
            f.write('\n')
    content = str(epoch) + ',' + str(batch_size) + ',' + str(lr) + "," + str(dropout) + ',' + str(num_layers) + ','  \
              + str(hidden_size) + ',' + str(activate_function) + ',' + str(mse) + ',' + str(rmse) + ',' + str(mae) + ',' + str(r2) + ',' + str(is_standrad) + ',' + str(is_PCA)
    with open(save_file, 'a') as f:
        f.write(content)
        f.write('\n')