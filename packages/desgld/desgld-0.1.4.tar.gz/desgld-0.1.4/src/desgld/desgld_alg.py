import math

import numpy as np


class DeSGLD:
    """Decentralized Stochastic Gradient Langevin Dynamics

    Args:
        size_w (int): the size of the network
        N (int): the size of the array in each it
        sigma (float): the variation of the noise
        eta (float): the learning rate
        T (int): the iteration numbers
        dim (int): the dimension of the input data
        b (int): the batch size
        lam (float): the regularization parameter
        x (float): the input data
        y (float): the output data
        w (float): the weight matrix from the network structure
        hv (float): the tuning parameter for the extra algorithm
        reg_type (str): the type of regressor used

    Returns:
        vanila_desgld()
        extra_desgld()
    """

    def __init__(
        self, size_w, N, sigma, eta, T, dim, b, lam, x, y, w, hv, reg_type
    ):
        self.size_w = size_w
        self.N = N
        self.sigma = sigma
        self.eta = eta
        self.dim = dim
        self.b = b
        self.lam = lam
        self.x = x
        self.y = y
        self.w = w
        self.hv = hv
        self.T = T
        self.reg_type = reg_type

    def gradient_logreg(self, beta, x, y, dim, lam, b):
        """Gradient function for the logistic regression

        Args:
            beta: approximation at each node
            x: the input data
            y: the output data
            dim: the dimension of the input data
            lam: the regularization parameter
            b: the batch size
        Returns:
            gradient for the the logistic regression
        """
        f = np.zeros(dim)
        randomList = np.random.randint(0, len(y) - 1, size=int(b))
        for item in randomList:
            h = 1 / (1 + np.exp(-np.dot(beta, x[item])))
            f -= np.dot((y[item] - h), x[item])
        f += (2 / lam) * beta
        return f

    def gradient_linreg(self, beta, x, y, dim, lam, b):
        """Gradient function for the linear regression

        Args:
            beta: approximation at each node
            x: the input data
            y: the output data
            dim: the dimension of the input data
            lam: the regularization parameter
            b: the batch size
        Returns:
            gradient for the the logistic regression
        """
        f = np.zeros(dim)
        randomList = np.random.randint(0, len(y) - 1, size=int(b))
        for i in randomList:
            f = f - np.dot((y[i] - np.dot(beta, x[i])), x[i])
        f += (2 / lam) * beta
        return f

    def vanila_desgld(self):
        """Vanila DeSGLD algorithm

        Returns:
            history_all: contains the approximation from all the nodes
            beta_mean_all: contains the mean of the approximation from
            all the nodes
        """
        # Initialization
        if self.reg_type == "logistic":
            beta = np.random.normal(
                0, self.sigma, size=(self.N, self.size_w, self.dim)
            )
        else:
            beta = np.random.multivariate_normal(
                mean=np.zeros(self.dim),
                cov=np.eye(self.dim),
                size=(self.N, self.size_w),
            )
        history_all = []
        beta_mean_all = []
        for t in range(1):
            history = np.empty((self.size_w, self.dim, self.N))
            beta_mean = np.empty((self.dim, self.N))
            for i in range(self.N):
                history[:, :, i] = beta[i, :, :]
            for j in range(self.dim):
                beta_mean[j, :] = np.mean(history[:, j, :], axis=0)
            history_all.append(history)
            beta_mean_all.append(beta_mean)

        # Update
        step = self.eta
        for t in range(self.T):
            for n in range(self.N):
                for i in range(self.size_w):
                    if self.reg_type == "logistic":
                        g = self.gradient_logreg(
                            beta[n, i],
                            self.x[i],
                            self.y[i],
                            self.dim,
                            self.lam,
                            self.b,
                        )
                        temp = np.zeros(self.dim)
                        for j in range(len(beta[n])):
                            temp = temp + self.w[i, j] * beta[n, j]
                        noise = np.random.normal(0, self.sigma, self.dim)
                        beta[n, i] = (
                            temp - step * g + math.sqrt(2 * step) * noise
                        )
                    else:
                        g = self.gradient_linreg(
                            beta[n, i],
                            self.x[i],
                            self.y[i],
                            self.dim,
                            self.lam,
                            self.b,
                        )
                        temp = np.zeros(self.dim)
                        for j in range(len(beta[n])):
                            temp = temp + self.w[i, j] * beta[n, j]
                        noise = np.random.multivariate_normal(
                            mean=np.zeros(self.dim), cov=np.eye(self.dim)
                        )
                        beta[n, i] = (
                            temp - step * g + math.sqrt(2 * step) * noise
                        )

            history = np.empty((self.size_w, self.dim, self.N))
            beta_mean = np.empty((self.dim, self.N))
            for i in range(self.N):
                history[:, :, i] = beta[i, :, :]
            for j in range(self.dim):
                beta_mean[j, :] = np.mean(history[:, j, :], axis=0)
            history_all.append(history)
            beta_mean_all.append(beta_mean)
        return np.array(history_all), np.array(beta_mean_all)

    def extra_desgld(self):
        """EXTRA DeSGLD algorithm

        Returns:
            history_all: contains the approximation from all the nodes
            beta_mean_all: contains the mean of the approximation from
            all the nodes
        """
        # I_n is the identity matrix of the same size as the weight matrix
        I_n = np.eye(self.size_w)
        h_values = self.hv

        history_all = []
        beta_mean_all = []
        for h in h_values:
            # w1 is the weight matrix with the hyperparameter h
            w1 = h * I_n + (1 - h) * self.w

            # Initialization
            if self.reg_type == "logistic":
                beta = np.random.normal(
                    0, self.sigma, size=(self.N, self.size_w, self.dim)
                )
            else:
                beta = np.random.multivariate_normal(
                    mean=np.zeros(self.dim),
                    cov=np.eye(self.dim),
                    size=(self.N, self.size_w),
                )
            history_all_h = []
            beta_mean_all_h = []
            for t in range(1):
                history = np.empty((self.size_w, self.dim, self.N))
                beta_mean = np.empty((self.dim, self.N))
                for i in range(self.N):
                    history[:, :, i] = beta[i, :, :]
                for j in range(self.dim):
                    beta_mean[j, :] = np.mean(history[:, j, :], axis=0)
                history_all_h.append(history)
                beta_mean_all_h.append(beta_mean)

            # Update
            step = self.eta
            for t in range(self.T):
                for n in range(self.N):
                    for i in range(self.size_w):
                        if self.reg_type == "logistic":
                            # Vanila Part
                            g = self.gradient_logreg(
                                beta[n, i],
                                self.x[i],
                                self.y[i],
                                self.dim,
                                self.lam,
                                self.b,
                            )
                            temp = np.zeros(self.dim)
                            for j in range(len(beta[n])):
                                temp = temp + w1[i, j] * beta[n, j]
                            noise = np.random.normal(0, self.sigma, self.dim)
                            beta[n, i] = (
                                temp - step * g + math.sqrt(2 * step) * noise
                            )
                            # Extra Part
                            g = self.gradient_logreg(
                                beta[n, i],
                                self.x[i],
                                self.y[i],
                                self.dim,
                                self.lam,
                                self.b,
                            )
                            temp = np.zeros(self.dim)
                            for j in range(len(beta[n])):
                                temp = temp + self.w[i, j] * beta[n, j]
                            noise = np.random.normal(0, self.sigma, self.dim)
                            beta[n, i] = (
                                temp - step * g + math.sqrt(2 * step) * noise
                            )
                        else:
                            # Vanila Part
                            g = self.gradient_linreg(
                                beta[n, i],
                                self.x[i],
                                self.y[i],
                                self.dim,
                                self.lam,
                                self.b,
                            )
                            temp = np.zeros(self.dim)
                            for j in range(len(beta[n])):
                                temp = temp + w1[i, j] * beta[n, j]
                            noise = np.random.multivariate_normal(
                                mean=np.zeros(self.dim), cov=np.eye(self.dim)
                            )
                            beta[n, i] = (
                                temp - step * g + math.sqrt(2 * step) * noise
                            )
                            # Extra Part
                            g = self.gradient_linreg(
                                beta[n, i],
                                self.x[i],
                                self.y[i],
                                self.dim,
                                self.lam,
                                self.b,
                            )
                            temp = np.zeros(self.dim)
                            for j in range(len(beta[n])):
                                temp = temp + self.w[i, j] * beta[n, j]
                            noise = np.random.multivariate_normal(
                                mean=np.zeros(self.dim), cov=np.eye(self.dim)
                            )
                            beta[n, i] = (
                                temp - step * g + math.sqrt(2 * step) * noise
                            )

                history = np.empty((self.size_w, self.dim, self.N))
                beta_mean = np.empty((self.dim, self.N))
                for i in range(self.N):
                    history[:, :, i] = beta[i, :, :]
                for j in range(self.dim):
                    beta_mean[j, :] = np.mean(history[:, j, :], axis=0)
                history_all_h.append(history)
                beta_mean_all_h.append(beta_mean)
            history_all.append(history_all_h)
            beta_mean_all.append(beta_mean_all_h)
        return np.array(history_all), np.array(beta_mean_all)
