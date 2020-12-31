import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def normalizing(matrix, k):
    for i in range(k):
        mean = np.mean(matrix[:, i])
        std = np.std(matrix[:, i])
        matrix[:, i] = (matrix[:, i] - mean) / std


def fit(learning_rate, trials):
    coefficients = np.zeros(number_of_features + 1)
    coefficients = np.reshape(coefficients, (14, 1))
    for i in range(trials):
        h = np.dot(x_train, coefficients)
        coefficients = coefficients - np.dot(np.transpose(x_train), (h - y_train)) * learning_rate * (1 / m)
    return coefficients


def regularization_fit(learning_rate, trials, landa):
    coefficients = np.zeros(number_of_features + 1)
    coefficients = np.reshape(coefficients, (14, 1))
    for i in range(trials):
        h = np.dot(x_train, coefficients)
        coefficients = coefficients * (1 - (learning_rate * landa / m)) - np.dot(np.transpose(x_train),
                                                                                 (h - y_train)) * learning_rate * (
                               1 / m)
    return coefficients


def regularization_fit_valid(learning_rate, trials, landa):
    coefficients = np.zeros(number_of_features + 1)
    coefficients = np.reshape(coefficients, (14, 1))
    k = len(new_x_train)
    for i in range(trials):
        h = np.dot(new_x_train, coefficients)
        coefficients = coefficients * (1 - (learning_rate * landa / k)) - np.dot(np.transpose(new_x_train),
                                                                                 (h - new_y_train)) * learning_rate * (
                               1 / k)
    return coefficients


def predict(coefficients):
    return np.dot(x_test, coefficients)


def find_hyper_parameter():
    lamdas = [500, 750, 1000]
    error = sys.maxsize
    landa = 0
    for l in lamdas:
        theta = regularization_fit_valid(0.01, 500, l)
        y_predicted = np.dot(x_valid, theta)
        er = np.sqrt(np.square(np.subtract(y_valid, y_predicted)).mean())
        if er < error:
            error = er
            landa = l
    return landa


def plot_errors_normal(learning_rate, k, j):
    errors = []
    iterations = []
    for i in range(100, 1100, 100):
        theta = fit(learning_rate, i)
        y_predicted = predict(theta)
        error = np.sqrt(np.square(np.subtract(y_test, y_predicted)).mean())
        errors.append(error)
        iterations.append(i)
    a[k][j].plot(iterations, errors)
    a[k][j].set_title(learning_rate)


def plot_errors_regularization(learning_rate, k, j):
    errors = []
    iterations = []
    for i in range(100, 1100, 100):
        theta = regularization_fit(learning_rate, i, landa)
        y_predicted = predict(theta)
        error = np.sqrt(np.square(np.subtract(y_test, y_predicted)).mean())
        errors.append(error)
        iterations.append(i)
    b[k][j].plot(iterations, errors)
    b[k][j].set_title(learning_rate)


def normal_gradient_descent():
    plot_errors_normal(0.1, 0, 0)
    plot_errors_normal(0.05, 0, 1)
    plot_errors_normal(0.01, 1, 0)
    plot_errors_normal(0.001, 1, 1)
    plt.suptitle("MSE Error/Number of Iteration")


def regularization_gradient_descent():
    plot_errors_regularization(0.1, 0, 0)
    plot_errors_regularization(0.05, 0, 1)
    plot_errors_regularization(0.01, 1, 0)
    plot_errors_regularization(0.001, 1, 1)
    plt.suptitle("With Regularization\nMSE Error/Number of Iteration")


housing = pd.read_csv("housing.csv")
# one-hot representation for the categorical data
housing['categorical'] = pd.Categorical(housing['ocean_proximity'])
categorical = pd.get_dummies(housing['ocean_proximity'], prefix='ocean_proximity')
housing = pd.concat([housing, categorical], axis=1)
housing = housing.drop(['categorical'], axis=1)
housing = housing.drop(['ocean_proximity'], axis=1)
# some cells were Nan type, we fill them with mean of other values
housing.dropna(subset=["total_bedrooms"], inplace=True)
# separating test and training sets
cut = int(7 * len(housing) / 10)
number_of_features = 13
housing = housing.to_numpy()
# normalizing the data in same scale
labels = housing[..., 8]
housing = np.delete(housing, 8, axis=1)
normalizing(housing, number_of_features)
# train set :
x_train = housing[0:cut]
m = len(x_train)
first_column_train = np.ones((m, 1))
x_train = np.hstack((first_column_train, x_train))
y_train = labels[0:cut]
y_train = np.reshape(y_train, (m, 1))
# test set :
x_test = housing[cut:len(housing)]
first_column_test = np.ones((len(x_test), 1))
x_test = np.hstack((first_column_test, x_test))
y_test = labels[cut:len(housing)]
y_test = np.reshape(y_test, (len(x_test), 1))
# validation set: for finding the best landa in regularization
cut_v = int(4 * len(x_train) / 5)
new_x_train = x_train[0:cut_v]
new_y_train = y_train[0:cut_v]
x_valid = x_train[cut_v:len(x_train)]
y_valid = y_train[cut_v:len(y_train)]
landa = 750
# **************
# WE CAN USE THE FOLLOWING COMMENTED LINE TO DETERMINE LAMBDA WITH VALIDATION SET
# landa = find_hyper_parameter()
# **************
# normal gradient descent :
fig1, a = plt.subplots(2, 2)
normal_gradient_descent()
# gradient descent with regularization :
fig2, b = plt.subplots(2, 2)
regularization_gradient_descent()
plt.show()
