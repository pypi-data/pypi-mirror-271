import numpy as np
import math
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib as mpl

from desgld_alg import DeSGLD
from network import NetworkArchitecture

size_w=6; N=100; 
sigma=1; eta=0.0005; 
T=20; dim=3; b=32; 
lam=10; total_data=1000
hv=np.linspace(0.001,0.5,10)

nn=NetworkArchitecture(size_w)
w=np.array(nn.fully_connected()) 

x = []
np.random.seed(10)
for i in range(total_data):
    x.append([-20 + (20 + 20) * np.random.normal(), -10 + np.random.normal()])
np.random.seed(11)
y = [1 / (1 + np.exp(-item[0] * 1 - 1 * item[1] + 10)) for item in x]
for i in range(len(y)):
    temp = np.random.uniform(0, 1)
    if temp <= y[i]:
        y[i] = 1
    else:
        y[i] = 0

x_all = np.array(x)
y_all = np.array(y)
x_all = x
y_all = y
x_all = np.insert(x_all, 0, 1, axis=1)
x = x_all

'''
    Data splitting
'''

X_train1, x_trainRemain, y_train1, y_trainRemain = train_test_split(
    x, y, test_size=0.83333, random_state=42
)
X_train2, x_trainRemain, y_train2, y_trainRemain = train_test_split(
    x_trainRemain, y_trainRemain, test_size=0.8, random_state=42
)
X_train3, x_trainRemain, y_train3, y_trainRemain =train_test_split(
    x_trainRemain, y_trainRemain, test_size=0.75, random_state=42
)
X_train4, x_trainRemain, y_train4, y_trainRemain = train_test_split(
    x_trainRemain, y_trainRemain, test_size=0.66666666, random_state=42
)
X_train5, X_train6, y_train5, y_train6 = train_test_split(
    x_trainRemain, y_trainRemain,test_size=0.5, random_state=42
)
x = [X_train1, X_train2, X_train3, X_train4, X_train5, X_train6]
y = [y_train1, y_train2, y_train3, y_train4, y_train5, y_train6]

method=DeSGLD(size_w, N, sigma, eta, T, dim, b, lam, x, y, w, hv)
des=method.vanila_desgld_logreg()

des 