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
        self.layers.append(DenseLayer(223, 120, dropout=0.1, activation=ReLu()))
        self.layers.append(DenseLayer(120, 50, activation=ReLu()))
        self.layers.append(DenseLayer(50, 120, activation=ReLu()))
        self.layers.append(DenseLayer(120, 223, activation=Sigmoid()))

        # # for test_bp()
        # self.layers.append(DenseLayer(2, 5, activation=ReLu()))
        # self.layers.append(DenseLayer(5, 2, activation=Sigmoid()))

    def forward(self, x):
        input_data = x
        for layer in self.layers:
            input_data = layer.forward(input_data)
        return input_data

    def backward(self, learning_rate, loss):
        for layer in reversed(self.layers):
            loss = layer.backward(learning_rate, loss)

    def get_loss(self, prediction, y, m, loss_function=None):
        if loss_function is None:
            loss_function = self.loss_function
        return loss_function(prediction, y, m)

    def epoch(self, X, y, flag_valid, flag_real):
        loss_list = []
        for i in range(len(y)):
            prediction = self.forward(X[i:i + 1])
            m = np.count_nonzero(flag_valid[i:i + 1])
            derivative_ce, loss_ce = self.get_loss(prediction, y[i:i + 1], m, self.loss_function_prob)
            derivative_mse, loss_mse = self.get_loss(prediction, y[i:i + 1], m, self.loss_function_real)

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

    def predict(self, x):
        input_data = x
        for layer in self.layers:
            input_data = layer.predict(input_data)
        return input_data

    def test(self, X, y, flag_valid, flag_real):
        loss_list = []
        for i in range(len(y)):
            prediction = self.forward(X[i:i + 1])
            m = np.count_nonzero(flag_valid[i:i + 1])
            _, loss_ce = self.get_loss(prediction, y[i:i + 1], m, self.loss_function_prob)
            _, loss_mse = self.get_loss(prediction, y[i:i + 1], m, self.loss_function_real)

            loss_ce *= flag_valid[i:i + 1]
            loss_ce *= 1 - flag_real[i:i + 1]

            loss_mse *= flag_valid[i:i + 1]
            loss_mse *= flag_real[i:i + 1]

            loss = loss_mse + loss_ce
            loss_list.append(np.sum(loss))
        return loss_list


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


def load_data_from_file(filename = 'splitedData.pkl'):
    filename = path_data + filename
    ret = None
    with open(filename, 'rb') as f:
        ret = pickle.load(f)
    return ret


def load_data(filename = 'splitedData.pkl'):
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


def shuffle_data(a, b, c):
    assert len(a) == len(b) == len(c)
    d = np.c_[a.reshape(len(a), -1), b.reshape(len(b), -1), c.reshape(len(c), -1)]
    np.random.shuffle(d)
    end_a = a.size // len(a)
    end_b = end_a + (b.size // len(b))
    a2 = d[:, :end_a].reshape(a.shape)
    b2 = d[:, end_a:end_b].reshape(b.shape)
    c2 = d[:, end_b:].reshape(c.shape)
    return a2, b2, c2


def save_model(nn, filename):
    filename = path_model + filename
    if not os.path.isdir(path_model):
        os.mkdir(path_model)
    with open(filename, 'wb') as f:
        pickle.dump(nn, f)


def load_model(filename):
    filename = path_model + filename
    with open(filename, 'rb') as f:
        return pickle.load(f)


def restore_data(x):
    deSortMap = preprocess.loadVar(path_data, 'deSortMap.pkl')
    minDataMatrix = preprocess.loadVar(path_data, 'minDataMatrix.pkl')
    difDataMatrix = preprocess.loadVar(path_data, 'difDataMatrix.pkl')
    formatFun = preprocess.loadVar(path_data, 'formatFun.pkl')
    restored = preprocess.restoreData(x.reshape(x.size), deSortMap, minDataMatrix, difDataMatrix)
    return restored, preprocess.decodeData(restored, formatFun)


def test_restore(pre_trained_model):
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


def train():
    np.random.seed(random_seed)

    # preprocess data
    flag_valid_train_raw, X_train_raw, flag_real_train_raw, flag_valid_dev_raw, X_dev_raw, flag_real_dev_raw, \
        flag_valid_test_raw, X_test_raw, flag_real_test_raw = load_data()
    flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
        flag_real_test = flag_valid_train_raw[:, :-38],  X_train_raw[:, :-38],  flag_real_train_raw[:, :-38],  \
                         flag_valid_dev_raw[:, :-38],  X_dev_raw[:, :-38],  flag_real_dev_raw[:, :-38], \
                         flag_valid_test_raw[:, :-38],  X_test_raw[:, :-38],  flag_real_test_raw[:, :-38]
    # flag_valid_train[164:170] = False
    # flag_valid_dev[164:170] = False
    # flag_valid_test[164:170] = False
    # X_train[164:170] = 0
    # X_dev[164:170] = 0
    # X_test[164:170] = 0

    # build model
    nn = NN(learning_rate=0.001, loss_function_prob=CrossEntropy(), loss_function_real=RMSE())

    # load pre-trained model
    # nn = load_model('model-epoch70-trainloss29-devloss32.pkl')

    # train
    start_epoch = max(nn.epoch_trained, 1)
    max_epoch = 100
    min_test_loss = np.inf
    min_test_loss_epoch = None
    for epoch in range(start_epoch, start_epoch + max_epoch):
        try:

            X, flag_valid, flag_real = shuffle_data(X_train, flag_valid_train, flag_real_train)
            loss_train_list = nn.epoch(X, X, flag_valid, flag_real)
            loss_train = np.average(loss_train_list)
            print('Training epoch {}, training loss = {}'.format(epoch, loss_train))
            # print((loss_train_list))
            if epoch % 10 == 0:
                loss_dev_list = nn.test(X_dev, X_dev, flag_valid_dev, flag_real_dev)
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
    # test_restore('model-epoch30-trainloss32-devloss33.pkl')
    train()
