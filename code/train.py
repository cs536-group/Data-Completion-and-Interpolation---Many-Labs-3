import os
import pickle
import preprocess
import numpy as np
from layers import DenseLayer
from funcs import MSE, ReLu, CrossEntropy, Sigmoid, RMSE

path_data = '../data/'
path_model = '../model/'
random_seed = 1145141919

class NN:

    def __init__(self, learning_rate, loss_function_prob=CrossEntropy(), loss_function_real=RMSE()):
        self.layers = []
        self._init_layers()
        self.loss_function_prob = loss_function_prob
        self.loss_function_real = loss_function_real
        self.learning_rate = learning_rate
        self.epoch_trained = 0

    def _init_layers(self):
        self.layers.append(DenseLayer(223, 180, dropout=0.1, activation=ReLu()))
        self.layers.append(DenseLayer(180, 100, activation=ReLu()))
        self.layers.append(DenseLayer(100, 180, activation=ReLu()))
        self.layers.append(DenseLayer(180, 223, activation=Sigmoid()))

        # # for test_bp()
        # self.layers.append(DenseLayer(2, 5, activation=ReLu()))
        # self.layers.append(DenseLayer(5, 2, activation=Sigmoid()))

    #compute next output
    def forward(self, x, dropout=True):
        #in:
        #x: data point
        #dropout: bool, indicator of using dropout
        input_data = x
        for layer in self.layers:
            input_data = layer.forward(input_data, dropout)
        return input_data

    #compute previous derivative of loss
    def backward(self, learning_rate, loss):
        #in:
        #learning_rate:
        #loss: derivative of loss
        for layer in reversed(self.layers):
            loss = layer.backward(learning_rate, loss)

    def get_loss(self, prediction, y, loss_function=None):
        #in:
        #prediction: output of nn
        #y: object
        #loss_function:
        #out: (a, b)
        #a: derivative of loss
        #b: loss
        if loss_function is None:
            loss_function = self.loss_function
        return loss_function(prediction, y)

    def epoch(self, X, y, flag_valid, flag_real):
        loss_list = []
        for i in range(len(y)):
            prediction = self.forward(X[i:i + 1])
            derivative_ce, loss_ce = self.get_loss(prediction, y[i:i + 1], self.loss_function_prob)
            derivative_mse, loss_mse = self.get_loss(prediction, y[i:i + 1], self.loss_function_real)

            derivative_ce *= flag_valid[i:i + 1]
            derivative_ce *= 1 - flag_real[i:i + 1]
            loss_ce *= flag_valid[i:i + 1]
            loss_ce *= 1 - flag_real[i:i + 1]

            derivative_mse *= flag_valid[i:i + 1]
            derivative_mse *= flag_real[i:i + 1]
            loss_mse *= flag_valid[i:i + 1]
            loss_mse *= flag_real[i:i + 1]

            derivative = derivative_mse + derivative_ce
            loss = loss_mse + loss_ce

            self.backward(self.learning_rate, derivative)
            loss_list.append(np.sum(loss))
        self.epoch_trained += 1
        return loss_list

    def epoch1(self, X, y):
        loss_list = []
        for i in range(len(y)):
            prediction = self.forward(X[i:i+1])
            derivative, loss = self.get_loss(prediction, y[i:i+1])
            self.backward(self.learning_rate, derivative)
            loss_list.append(np.sum(loss))
        return loss_list

    #forward(dropout = False)
    def predict(self, x):
        input_data = x
        for layer in self.layers:
            input_data = layer.predict(input_data)
        return input_data

    def test(self, X, y, flag_valid, flag_real, dropout=False):
        #in:
        #X: data matrix
        #y: object
        #flag_valid: NA mask
        #flag_real: real/prob mask
        #dropout: bool, decide whether to use dropout
        #out:
        #loss_list: list, len = len(y), overall loss
        #loss_list_axised: list of list, shape = (len(y), 223), loss on each feature
        loss_list = []
        loss_list_axised = [] #store loss by axis
        for i in range(len(y)):
            prediction = self.forward(X[i:i + 1], dropout=dropout)
            _, loss_ce = self.get_loss(prediction, y[i:i + 1], self.loss_function_prob)
            _, loss_mse = self.get_loss(prediction, y[i:i + 1], self.loss_function_real)

            loss_ce *= flag_valid[i:i + 1]
            loss_ce *= 1 - flag_real[i:i + 1]

            loss_mse *= flag_valid[i:i + 1]
            loss_mse *= flag_real[i:i + 1]

            loss = loss_mse + loss_ce
            loss_list.append(np.sum(loss))
            loss_list_axised.append(loss[0]) #store loss by axis, shpe = (len(y), 223)
        return loss_list, loss_list_axised


def test_bp():
    nn = NN()

    X = np.array(([[2.5, 1.5], [7.5, 1.5], [2.5, 2.5], [7.5, 2.5], [2.5, 3.5], [7.5, 3.5], [2.5, 4.5], [7.5, 4.5], [1.5, 2.5], [6.5, 2.5], [1.5, 3.5], [6.5, 3.5], [3.5, 2.5], [8.5, 2.5], [3.5, 3.5], [8.5, 3.5]]
), dtype=float)
    y = np.array(([[1, 0], [0, 1], [1, 0], [0, 1], [1, 0], [0, 1], [1, 0], [0, 1], [1, 0], [0, 1], [1, 0], [0, 1], [1, 0], [0, 1], [1, 0], [0, 1]]), dtype=float)


    max_epoch = 500
    min_test_loss = np.inf
    for epoch in range(max_epoch):
        loss_train_list = nn.epoch1(X, y)
        loss_test = np.average(loss_train_list)
        print('Training epoch {}, training loss = {}'.format(epoch, loss_test))
        # print((loss_train_list))
        min_test_loss = np.minimum(min_test_loss, loss_test)
    print(min_test_loss)
    x = np.array([7.5, -2])
    print(nn.predict(x))


#from /data/filename load data
def load_data_from_file(filename = 'splitedData.pkl'):
    filename = path_data + filename
    ret = None
    with open(filename, 'rb') as f:
        ret = pickle.load(f)
    return ret


#load splited dataset
def load_data(filename = 'splitedData.pkl'):
    #out:
    #valid: bool mask for each feature, indicate not NA
    #_: actual data, NA is replaced with 0
    #real: bool mask for each feature, indicate real value (True) / prob value (False)
    filename = path_data + filename
    data = load_data_from_file(filename)

    flag_valid_train = np.array(data[0], dtype=np.bool_)
    X_train = np.array(data[1], dtype=np.float)
    flag_real_train = np.array(data[2], dtype=np.bool_)

    flag_valid_dev = np.array(data[3], dtype=np.bool_)
    X_dev = np.array(data[4], dtype=np.float)
    flag_real_dev = np.array(data[5], dtype=np.bool_)

    flag_valid_test = np.array(data[6], dtype=np.bool_)
    X_test = np.array(data[7], dtype=np.float)
    flag_real_test = np.array(data[8], dtype=np.bool_)

    # flag_valid_train[:, -38:] = False
    # flag_valid_dev[:, -38:] = False
    # flag_valid_test[:, -38:] = False
    # X_train *= flag_valid_train
    # X_dev *= flag_valid_dev
    # X_test *= flag_valid_test

    # print(flag_valid_train.shape,  X_train.shape,  flag_real_train.shape,  flag_valid_dev.shape,  X_dev.shape,
    #       flag_real_dev.shape,  flag_valid_test.shape,  X_test.shape, flag_real_test.shape)
    return flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
           flag_real_test


#shuffle 4 array using the same index order
def shuffle_data(a, b, c, d):
    assert len(a) == len(b) == len(c) == len(d)
    _ = np.c_[a.reshape(len(a), -1), b.reshape(len(b), -1), c.reshape(len(c), -1), d.reshape(len(d), -1)]
    np.random.shuffle(_)
    end_a = a.size // len(a)
    end_b = end_a + (b.size // len(b))
    end_c = end_b + (c.size // len(c))
    a2 = _[:, :end_a].reshape(a.shape)
    b2 = _[:, end_a:end_b].reshape(b.shape)
    c2 = _[:, end_b:end_c].reshape(c.shape)
    d2 = _[:, end_c:].reshape(d.shape)
    return a2, b2, c2, d2


#dump nn to /model/
def save_model(nn, filename):
    filename = path_model + filename
    if not os.path.isdir(path_model):
        os.mkdir(path_model)
    with open(filename, 'wb') as f:
        pickle.dump(nn, f)


#load nn from /model/
def load_model(filename):
    filename = path_model + filename
    with open(filename, 'rb') as f:
        return pickle.load(f)


#given the predicted vector, reconstuct data point with the same format in ML3AllSites
def restore_data(x):
    #in: 
    #x: nn output
    #out: (a, b)
    #a: data point with the same format as encoded dataset
    #b: data point with the same format as ML3AllSites
    deSortMap = preprocess.loadVar(path_data, 'deSortMap.pkl')
    minDataMatrix = preprocess.loadVar(path_data, 'minDataMatrix.pkl')
    difDataMatrix = preprocess.loadVar(path_data, 'difDataMatrix.pkl')
    formatFun = preprocess.loadVar(path_data, 'formatFun.pkl')
    restored = preprocess.restoreData(x.reshape(x.size), deSortMap, minDataMatrix, difDataMatrix)
    return restored, preprocess.decodeData(restored, formatFun)


#print original data point and predicted data point
def test_restore(pre_trained_model):
    #in:
    #pre_trained_model: str, model file name
    np.random.seed(random_seed)

    # preprocess data
    flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
        flag_real_test = load_data()

    # load pre-trained model
    nn = load_model(pre_trained_model)
    x = X_train[0:1]
    predict = nn.predict(x[:, :-38])
    predict_with_38 = np.concatenate((predict, X_train[0:1, -38:]), axis=1)
    r_x = restore_data(x)
    r_predict, prediction_formatted = restore_data(predict_with_38)
    print(r_x)
    print(r_predict)
    print(prediction_formatted)
    return


#trace loss to the original feature space
def restore_loss(loss_axised, deSortMap, flag_real, best_name = 'best', worst_name = 'worst'):
    #in:
    #loss_axised: np.array, shape = (1, len(data point))
    #deSortMap: dict, sCol: (eCol, oriCol)
    #flag_real: real / prob mask, shape = (1, len(data point))
    #best_name: str
    #worst_name: str
    loss_real_axised, loss_prob_axised = preprocess.restoreLoss(loss_axised, deSortMap, flag_real)
    loss_real_axised = np.asarray(loss_real_axised, dtype = np.float64)
    loss_prob_axised = np.asarray(loss_prob_axised, dtype = np.float64)
    
    loss_real_nan_index = np.isnan(loss_real_axised)
    loss_prob_nan_index = np.isnan(loss_prob_axised)
    loss_real_axised[loss_real_nan_index] = -np.inf
    loss_real_max_index = np.argsort(loss_real_axised)
    loss_real_axised[loss_real_nan_index] = np.inf
    loss_real_min_index = np.argsort(loss_real_axised)
    loss_prob_axised[loss_prob_nan_index] = -np.inf
    loss_prob_max_index = np.argsort(loss_prob_axised)
    loss_prob_axised[loss_prob_nan_index] = np.inf
    loss_prob_min_index = np.argsort(loss_prob_axised)


    print(best_name + ' real values:')
    for i in range(10):
        print('column %d: loss %f' %(loss_real_min_index[i], loss_real_axised[loss_real_min_index[i]]))
    print(worst_name + ' real values:')
    for i in range(10):
        print('column %d: loss %f' %(loss_real_max_index[-(i+1)], loss_real_axised[loss_real_max_index[-(i+1)]]))
    print(best_name + ' prob values:')
    for i in range(10):
        print('column %d: loss %f' %(loss_prob_min_index[i], loss_prob_axised[loss_prob_min_index[i]]))
    print(worst_name + ' prob values:')
    for i in range(10):
        print('column %d: loss %f' %(loss_prob_max_index[-(i+1)], loss_prob_axised[loss_prob_max_index[-(i+1)]]))
    return 


#given the model, check how much loss each feature contributes
def test_restore_loss_axised(pre_trained_model):
    flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
        flag_real_test = load_data()
    deSortMap = preprocess.loadVar(path_data, 'deSortMap.pkl')

    nn = load_model(pre_trained_model)
    x = X_dev[:, :-38]
    loss_dev_list, loss_dev_list_axised = nn.test(x, x, flag_valid_dev[:, :-38], flag_real_dev[:, :-38])
    loss_axised = np.average(loss_dev_list_axised, axis = 0)
    restore_loss(loss_axised, deSortMap, flag_real_dev[0])
    return


#given the model, dropout each feature, check the new loss
def test_col_importance(pre_trained_model):
    flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
        flag_real_test = load_data()
    deSortMap = preprocess.loadVar(path_data, 'deSortMap.pkl')

    nn = load_model(pre_trained_model)
    x = X_dev[:, :-38]

    loss_dev_list, loss_dev_list_axised = nn.test(x, x, flag_valid_dev[:, :-38], flag_real_dev[:, :-38])
    ori_loss = np.average(loss_dev_list) #baseline loss

    loss_list_axised = []
    for index in range(x.shape[1]):
        temp_x = np.copy(x)
        temp_valid = np.copy(flag_valid_dev[:, :-38])
        temp_valid[:, index] = False #avoid the situation that this data itself is hard to predict
        temp_x[:, index] = 0
        loss_dev_list, loss_dev_list_axised = nn.test(temp_x, x, temp_valid, flag_real_dev[:, :-38])
        loss_list_axised.append(np.average(loss_dev_list))
    loss_list_axised = np.asarray(loss_list_axised, dtype = np.float64)
    restore_loss(loss_list_axised - ori_loss, deSortMap, flag_real_dev[0], 'least important', 'most important') #minus baseline
    return


#given the model, compare the prediction in hottest and coldest lab
def test_temperature(pre_trained_model):
    flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
        flag_real_test = load_data()
    deSortMap = preprocess.loadVar(path_data, 'deSortMap.pkl')

    nn = load_model(pre_trained_model)
    x = X_dev[:, :-38]

    lo_x = np.copy(x)
    x[:, 188] = 0.01 #coldest

    hi_x = np.copy(x)
    x[:, 188] = 0.99 #hottest

    flag_valid_dev[:, 182: 189] = False #avoid test 7 itself
    lo_predict = []
    for i in range(len(lo_x)):
        lo_predict.append(nn.forward(lo_x[i:i + 1], dropout=False)[0])
    lo_predict = np.asarray(lo_predict, dtype = np.float64) #prediction in coldest

    loss_dev_list, loss_dev_list_axised = nn.test(hi_x, lo_predict, flag_valid_dev[:, :-38], flag_real_dev[:, :-38]) #use coldest as object, computing hottest loss
    loss_axised = np.average(loss_dev_list_axised, axis = 0)
    restore_loss(loss_axised, deSortMap, flag_real_dev[0], 'least different', 'most different')
    return


def test_num_of_features():
    """
    for question: Does it need a certain amount of features in order to interpolate well?
    :return:
    """
    np.random.seed(random_seed)
    # preprocess data
    flag_valid_train_raw, X_train_raw, flag_real_train_raw, flag_valid_dev_raw, X_dev_raw, flag_real_dev_raw, \
        flag_valid_test_raw, X_test_raw, flag_real_test_raw = load_data()
    flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
    flag_real_test = np.copy(flag_valid_train_raw[:, :-38]), np.copy(X_train_raw[:, :-38]), \
                     np.copy(flag_real_train_raw[:, :-38]), np.copy(flag_valid_dev_raw[:, :-38]), \
                     np.copy(X_dev_raw[:, :-38]), np.copy(flag_real_dev_raw[:, :-38]), \
                     np.copy(flag_valid_test_raw[:, :-38]), np.copy(X_test_raw[:, :-38]), \
                     np.copy(flag_real_test_raw[:, :-38])

    # load pre-trained model
    nn = load_model('model-epoch30-trainloss22-devloss20.pkl')

    # evaluate
    dropout_rates = np.arange(0, 1, 0.05, dtype=np.float)
    for dropout in dropout_rates:
        nn.layers[0].dropout = dropout
        loss_list, _ = nn.test(X_test, X_test_raw[:, :-38], flag_valid_test, flag_real_test, dropout=True)
        print('dropout={}, \tloss={}'.format(dropout, np.average(loss_list)))
    return


def train():
    deSortMap = preprocess.loadVar(path_data, 'deSortMap.pkl')
    np.random.seed(random_seed)

    # preprocess data
    flag_valid_train_raw, X_train_raw, flag_real_train_raw, flag_valid_dev_raw, X_dev_raw, flag_real_dev_raw, \
        flag_valid_test_raw, X_test_raw, flag_real_test_raw = load_data()
    flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
        flag_real_test = np.copy(flag_valid_train_raw[:, :-38]),  np.copy(X_train_raw[:, :-38]),  np.copy(flag_real_train_raw[:, :-38]),  \
                         np.copy(flag_valid_dev_raw[:, :-38]),  np.copy(X_dev_raw[:, :-38]),  np.copy(flag_real_dev_raw[:, :-38]), \
                         np.copy(flag_valid_test_raw[:, :-38]),  np.copy(X_test_raw[:, :-38]),  np.copy(flag_real_test_raw[:, :-38])
    # flag_valid_train[164:170] = False
    # flag_valid_dev[164:170] = False
    # flag_valid_test[164:170] = False
    # X_train[:, 120:170] = 0
    # X_dev[:, 120:170] = 0
    # X_test[164:170] = 0

    # build model
    nn = NN(learning_rate=0.001, loss_function_prob=CrossEntropy(), loss_function_real=RMSE())

    # load pre-trained model
    # nn = load_model('model-epoch126-trainloss27-devloss32.pkl')

    # train
    start_epoch = max(nn.epoch_trained, 1)
    max_epoch = 100
    min_test_loss = np.inf
    min_test_loss_epoch = None
    for epoch in range(start_epoch, start_epoch + max_epoch):
        try:

            X, X_raw, flag_valid, flag_real = shuffle_data(X_train, X_train_raw[:, :-38], flag_valid_train, flag_real_train)
            loss_train_list = nn.epoch(X, X_raw, flag_valid, flag_real)
            loss_train = np.average(loss_train_list)
            print('Training epoch {}, training loss = {}'.format(epoch, loss_train))
            # print((loss_train_list))
            if epoch % 10 == 0:
                loss_dev_list, loss_dev_list_axised = nn.test(X_dev, X_dev_raw[:, :-38], flag_valid_dev, flag_real_dev)
                loss_test = np.average(loss_dev_list)
                if loss_test < min_test_loss:
                    min_test_loss = loss_test
                    min_test_loss_epoch = epoch
                print('Testing loss = {}'.format(loss_test))
                save_model(nn, 'model-epoch{}-trainloss{}-devloss{}.pkl'.format(epoch, int(loss_train), int(min_test_loss)))

        except KeyboardInterrupt:
            if input('\n Do you want to save current model? (y / n) ') == 'y':
                save_model(nn, 'model-epoch{}-trainloss{}-devloss{}.pkl'.format(epoch, int(loss_train), int(min_test_loss)))
            exit()

    print('Minimum test loss: {} in epoch {}'.format(min_test_loss, min_test_loss_epoch))
    return


if __name__ == '__main__':
    # test_temperature('model-epoch30-trainloss22-devloss20.pkl')
    test_num_of_features()
    # train()
