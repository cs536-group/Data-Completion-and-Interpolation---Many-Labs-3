import numpy as np
from layers import DenseLayer
from funcs import MSE, ReLu, CrossEntropy, Sigmoid
import pickle

class NN:

    def __init__(self, learning_rate=0.0001, loss_function=CrossEntropy()):
        self.layers = []
        self._init_layers()
        self.loss_function = loss_function
        self.learning_rate = learning_rate

    def _init_layers(self):
        self.layers.append(DenseLayer(261, 150, dropout=0.1, activation=ReLu()))
        self.layers.append(DenseLayer(150, 50, activation=ReLu()))
        self.layers.append(DenseLayer(50, 150, activation=ReLu()))
        self.layers.append(DenseLayer(150, 261, activation=Sigmoid()))

        # # for test()
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

    def get_loss(self, prediction, y, loss_function=None):
        if loss_function is None:
            loss_function = self.loss_function
        return loss_function(prediction, y)

    def epoch(self, X, y, flag_valid, flag_real):
        loss_list = []
        for i in range(len(y)):
            prediction = self.forward(X[i:i+1])
            derivative_ce, loss_ce = self.get_loss(prediction, y[i:i+1], CrossEntropy())
            derivative_mse, loss_mse = self.get_loss(prediction, y[i:i+1], MSE())
            derivative_ce *= flag_valid[i:i + 1]
            loss_ce *= flag_valid[i:i + 1]

            derivative_mse *= flag_valid[i:i + 1]
            derivative_mse *= flag_real[i:i + 1]
            loss_mse *= flag_valid[i:i + 1]
            loss_mse *= flag_real[i:i + 1]

            derivative = derivative_mse + derivative_ce
            loss = loss_mse + loss_ce

            self.backward(self.learning_rate, derivative)
            loss_list.append(np.sum(loss))
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

    def test(self, X, y, flag_valid):
        loss_list = []
        for i in range(len(y)):
            prediction = self.predict(X[i:i+1])
            derivative, loss = self.get_loss(prediction, y[i:i+1])
            derivative *= flag_valid[i:i + 1]
            loss *= flag_valid[i:i + 1]
            loss_list.append(np.sum(loss))
        return loss_list


def test():
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


def load_data_from_file(filename = '../data/splitedData.pkl'):
    ret = None
    with open(filename, 'rb') as f:
        ret = pickle.load(f)
    return ret


def load_data(filename = '../data/splitedData.pkl'):
    data = load_data_from_file(filename)

    flag_valid_train = np.array(data[0])
    X_train = np.array(data[1], dtype=np.float)
    flag_real_train = np.array(data[2])

    flag_valid_dev = np.array(data[3])
    X_dev = np.array(data[4])
    flag_real_dev = np.array(data[5])

    flag_valid_test = np.array(data[6])
    X_test = np.array(data[7])
    flag_real_test = np.array(data[8])

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


if __name__ == '__main__':
    np.random.seed(1145141919)

    # preprocess data
    flag_valid_train, X_train, flag_real_train, flag_valid_dev, X_dev, flag_real_dev, flag_valid_test, X_test, \
        flag_real_test = load_data()
    flag_valid_train[:, -38:] = False
    flag_valid_dev[:, -38:] = False
    flag_valid_test[:, -38:] = False
    X_train *= flag_valid_train
    X_dev *= flag_valid_dev
    X_test *= flag_valid_test

    # build model
    nn = NN(learning_rate=0.01, loss_function=CrossEntropy())

    # train
    max_epoch = 100
    min_test_loss = np.inf
    for epoch in range(max_epoch):
        X, flag_valid, flag_real = shuffle_data(X_train, flag_valid_train, flag_real_train)
        loss_train_list = nn.epoch(X, X, flag_valid, flag_real)
        print('Training epoch {}, training loss = {}'.format(epoch, np.average(loss_train_list)))
        # print((loss_train_list))
        if epoch % 10 == 0:
            loss_dev_list = nn.test(X_dev, X_dev, flag_valid_dev)
            loss_test = np.average(loss_dev_list)
            min_test_loss = np.minimum(min_test_loss, loss_test)
            print('Testing loss = {}'.format(loss_test))
    print(min_test_loss)
