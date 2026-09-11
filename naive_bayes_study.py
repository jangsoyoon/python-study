from torch import t_copy
from math import log, exp, factorial
import matplotlib.pyplot as plt

data = [
    ("Chinese Beijing Chinese", "yes"),
    ("Chinese Chinese Shanghai", "yes"),
    ("Chinese Macao", "yes"),
    ("Tokyo Japan Chinese", "no"),
]

d = "Chinese Chinese Chinese Tokyo Japan"

data = [
    ("just plain boring", "negative"),
    ("entirely predictable and lacks energy", "negative"),
    ("no surprises and very few laughs", "negative"),
    ("very powerful", "positive"),
    ("the most fun film of the summer", "positive"),
]

d = "predictable no fun"


def training(C, D):
    # 1
    V = list(set([word for row in D for word in row[0].lower().split()]))
    # for row in D: for t in row[0] : Normalization ; word_tokenize

    # 2
    N = len(D)

    # 3
    prior = dict()
    condprob = dict()
    for c in C:
        # 4
        Nc = len([row for row in D if row[1] == c])
        # 5
        prior[c] = Nc / N
        # 6
        textc = " ".join([row[0] for row in D if row[1] == c])
        # 7
        Tct = dict()
        for t in V:
            # 8 => Counter
            Tct[t] = len([token for token in textc.lower().split() if token == t])
        # 9
        for t in V:
            # 10
            if t not in condprob:
                condprob[t] = dict()
            condprob[t][c] = (Tct[t] + 1) / sum([Tct[t_copy] + 1 for t_copy in Tct])
            # print(
            #     t,
            #     c,
            #     (Tct[t] + 1),
            #     sum([Tct[t_copy] + 1 for t_copy in Tct]),
            #     condprob[t][c],
            # )
            # Add-1 Smoothing
    return V, prior, condprob


V, prior, condprob = training(list(set([row[1] for row in data])), data)


def predict(d, C, V, prior, condprob):
    # 1
    W = [t for t in d.lower().split() if t in V]
    # 2
    score = dict()
    for c in C:
        # 3
        score[c] = log(prior[c])
        # 4
        for t in W:
            # 5
            score[c] += log(condprob[t][c])
    return score, max(score, key=score.get), {k: exp(v) for k, v in score.items()}


# print(predict(d, list(set([row[1] for row in data])), V, prior, condprob))


def taylor(x, N=3):
    a = 0
    value = 0.0
    for n in range(N):
        value += (exp(a) / factorial(n)) * (x - a) ** n
    return value


X = list(range(1, 5))
# plt.plot(X, [exp(x) for x in X], label="exp(x)", c="k")
# plt.plot(X, [taylor(x, 3) for x in X], label="taylor(x)", c="r")
# plt.plot(X, [taylor(x, 6) for x in X], label="taylor(x)", c="g")
# plt.plot(X, [taylor(x, 9) for x in X], label="taylor(x)", c="b")

# plt.show()


rosenbrock = lambda x1, x2: (1 - x1) ** 2 + 100 * (x2 - x1**2) ** 2
d_x1 = lambda x1, x2: -2 * (1 - x1) - 400 * (x2 - x1**2) * x1
d_x2 = lambda x1, x2: 200 * (x2 - x1**2)
norm = lambda x1, x2: (x1**2 + x2**2) ** (1 / 2)
X = [-1.3, 0.9]
history = []
h = 5e-5
epoch = 100000

X = [-1.3, 0.9]
history = []

for i in range(epoch):
    dX = [d_x1(*X), d_x2(*X)]

    X[0] = X[0] - h * dX[0] / norm(*dX)
    X[1] = X[1] - h * dX[1] / norm(*dX)

    if i % 100 == 0:  # Error
        history.append(rosenbrock(*X))


# print(X)
# plt.plot(history)
# plt.show()


# Input -> Model -> Output
#           AI
# 입력   (NB, LinearR, LogisticR, SoftmaxR, NN, MLP, DNN + CNN + RNN / LLM)    출력
#                                   X:LR => argminY-y{y|x1,x2,...,xn}    gradient descent => method(taylor)
#    -> tㅌV    -> vector(X:앞,뒤X -> X:LR => argmaxy=Y{y|x1,x2,...,xn})   gradient ascent
#       logP       -------          y > .5  (y=1;theta), else y=0
# X입력 * theta,a,w => 선형관계
import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(np.pi * 0, np.pi * 2, 100)
Y = np.sin(X)
Y[Y >= 0] = 1
Y[Y < 0] = 0
_X = np.c_[np.ones(len(X)), X]
_X.shape
theta = np.linalg.inv(_X.T @ _X) @ _X.T @ Y
print(theta)
# array([ 1.24257426, -0.23636873])
temp = 2 * np.pi * np.random.rand(1)
print(
    temp, theta @ np.r_[np.ones(1), temp], theta @ np.r_[np.ones(1), temp] > 0.5
)  # Classification
# (array([4.01500254]), 0.2935532176130371, False)
# plt.scatter(X, Y, s=1, c="k")
# plt.plot(
#     [X.min(), X.max()],
#     [theta @ np.array([1, X.min()]), theta @ np.array([1, X.max()])],
#     c="r",
# )
# plt.axhline(0.5, c="b")
# plt.axvline((0.5 - theta[0]) / theta[1], c="b")
#          X(제일작은값, 제일큰값)                   Y(작은값*theta, 큰값*theta)
# ax+b => bx_0 + ax_1 => b*1 + a*x => theta[0]*1 + theta[1]*x

# Gradient Descent
h = 1e-5
epoch = 10000
theta = np.random.rand(2)  # 초기점

J = lambda trueY, _x, _theta: np.sum((trueY - _x @ _theta) ** 2)
history = list()

_X = np.c_[np.ones(len(X)), X]

for i in range(epoch):
    dtheta0 = np.sum(2 * (Y - _X @ theta) * _X[:, 0])
    dtheta1 = np.sum(2 * (Y - _X @ theta) * _X[:, 1])
    theta = theta - h * (-np.array([dtheta0, dtheta1]))

    if i % 100 == 0:
        history.append(J(Y, _X, theta))

# plt.plot(history), theta

# plt.scatter(X, Y, s=1, c="k")
# plt.plot(
#     [X.min(), X.max()],
#     [theta @ np.array([1, X.min()]), theta @ np.array([1, X.max()])],
#     c="r",
# )
# plt.axhline(0.5, c="b")
# plt.axvline((0.5 - theta[0]) / theta[1], c="b")

# Gradient Descent
h = 1e-4
epoch = 100000
theta = np.random.rand(2)  # 초기점

J = lambda trueY, _x, _theta: np.sum((trueY - _x @ _theta) ** 2)
history = list()
thetalist = list()  # 여기################

_X = np.c_[np.ones(len(X)), X]

for i in range(epoch):
    theta = theta - h * (-_X.T @ (Y - _X @ theta)) / len(X)  # 평균
    #          (2,)<=(2,100)@(100,)-[(100,2)@(2,) => (100,)] = (100,) 각 행마다 X_i 정답이랑 얼마나 차이나는지
    #          [1, 1, 1, 1, ...   => theta0
    #           x1,x2,x3,x4,...]  => theta1
    if i % 100 == 0:
        history.append(J(Y, _X, theta))
        thetalist.append(theta)  # 여기################


# plt.scatter(X, Y, s=1, c="k")
# plt.plot(
#     [X.min(), X.max()],
#     [theta @ np.array([1, X.min()]), theta @ np.array([1, X.max()])],
#     c="r",
# )
# plt.axhline(0.5, c="b")
# plt.axvline((0.5 - theta[0]) / theta[1], c="b")

# plt.scatter(X, Y, s=1, c="k")
# plt.plot(
#     [X.min(), X.max()],
#     [theta @ np.array([1, X.min()]), theta @ np.array([1, X.max()])],
#     c="r",
# )
# for _theta in thetalist:
#     plt.plot(
#         [X.min(), X.max()],
#         [_theta @ np.array([1, X.min()]), _theta @ np.array([1, X.max()])],
#         c="r",
#         alpha=0.1,
#     )
# plt.axhline(0.5, c="b")
# plt.axvline((0.5 - theta[0]) / theta[1], c="b")
# plt.ylim(-0.1, 1.1)

logistic = lambda x: 1 / (1 + np.exp(-x))
# plt.scatter(np.linspace(-10, 10, 100), logistic(np.linspace(-10, 10, 100)))
# plt.axhline(0.5)
# plt.axvline(0)

# 베르누이시행 => J
# P(D|theta)   = theta^Y*(1-theta)^(1-Y)
#  (Y|X;theta) = P(X)^Y*(1-P(X))^(1-Y)
#    argmax    = Y=P(X), 정답=정답 => 1
#                        오답=오답 => 1
#  (Y=1, 정답)

# log J => 0, argmax / gradient +
# 구간: [0,1]

# negative log J => argmin / grandient - => NLL / BinaryCrossEntropy
logistic2 = lambda x: np.exp(x) / (1 + np.exp(x))
# plt.scatter(np.linspace(-10, 10, 100), logistic2(np.linspace(-10, 10, 100)))
# # plt.scatter(np.linspace(-10,10,100), logistic(np.linspace(-10,10,100)))
# plt.axhline(0.5)
# plt.axvline(0)

np.random.seed(0)
theta = np.random.rand(2)

J = lambda trueY, predY: predY**trueY * (1 - predY) ** (1 - trueY)  # 베르누이
d_logistic = lambda y, x: y - logistic(x)

h = 1e-4
epoch = 30000
history = list()

_X = np.c_[np.ones(len(X)), X]

for i in range(epoch):
    theta = theta + h * _X.T @ d_logistic(Y, _X @ theta)
    if i % 100 == 0:
        history.append(np.mean(J(Y, logistic(_X @ theta))))

# plt.plot(history)

# for x, y in zip(X, Y):
#     plt.scatter(x, y, c=("r" if logistic(np.array([1, x]) @ theta) > 0.5 else "b"), s=3)
# # plt.scatter(X,Y,c='k',s=3)
# plt.scatter(X, logistic(_X @ theta), c="g", s=3)

data = [
    ("Chinese Beijing Chinese", "yes"),
    ("Chinese Chinese Shanghai", "yes"),
    ("Chinese Macao", "yes"),
    ("Tokyo Japan Chinese", "no"),
]

d = "Chinese Chinese Chinese Tokyo Japan"
# Tokens = Tokenizer(data)
# V = {tㅌTokens} => Dims
# Vectorize
# Tokenizing
V = list()
for x, y in data:
    # Normalizing + Tokenizing
    V.extend(x.lower().split())
V = list(set(V))
X = np.zeros((len(data), len(V)))
Y = np.zeros(len(data))

i2t = lambda i: V[i]
t2i = lambda t: V.index(t)

# Boolean Vectorize
for i, (x, y) in enumerate(data):
    for t in x.lower().split():
        if t in V:
            j = t2i(t)
            X[i, j] = (
                1  # 벡터차원(Token=어휘)에서의 중요도/가중치, [0,1], [0,1,2,3], [0~실수]
            )
    Y[i] = 1 if y == "yes" else 0


idx = 0
# for x, y in zip(X, Y):
#     plt.scatter(x[idx], y, c="r" if y == 1 else "b")

test = np.zeros(X.shape[-1])
for t in d.lower().split():
    if t in V:
        test[t2i(t)] = 1  # Boolean
test = np.r_[np.ones(1), test]

# Gradient Descent
np.random.seed(0)

h = 1e-4
epoch = 100000
theta = np.random.rand(X.shape[-1] + 1)

J = lambda trueY, _x, _theta: np.sum((trueY - _x @ _theta) ** 2)
history = list()

_X = np.c_[np.ones(len(X)), X]

for i in range(epoch):
    theta = theta - h * (-_X.T @ (Y - _X @ theta)) / len(X)  # 평균
    if i % 100 == 0:
        history.append(J(Y, _X, theta))

# plt.plot(history), _X @ theta > 0.5, test @ theta > 0.5

# plt.show()

np.random.seed(0)
theta = np.random.rand(X.shape[-1] + 1)

J = lambda trueY, predY: predY**trueY * (1 - predY) ** (1 - trueY)  # 베르누이
d_logistic = lambda y, x: y - logistic(x)

h = 5e-4
epoch = 30000
history = list()

_X = np.c_[np.ones(len(X)), X]

for i in range(epoch):
    theta = theta + h * _X.T @ d_logistic(Y, _X @ theta)
    if i % 100 == 0:
        history.append(np.mean(J(Y, logistic(_X @ theta))))

# plt.plot(history), logistic(_X @ theta) > 0.5, logistic(test @ theta) > 0.5
# plt.show()


import numpy as np

#                       1 2 3 4
#
X = [[0, 0, 1, 1], [0, 1, 0, 1]]
X = np.array(X)
Y = np.array(
    [0, 0, 0, 1]
)  # 두 값이 1일 때만 1, 나머지는 0  -> 열로 바꾼다면 [0,0] [0,1], [1,0], [1,1] 이니까

lr = h = 1e-5
ephoch = 10000
history = list()
W = np.random.rand(X.shape[0])  # 2개
B = np.random.rand(1)  # 1개  bias 갯수는 아웃풋의 개수만큼 필요
for it in range(ephoch):
    for i in range(X.shape[-1]):  # Stochastic Gradient Descent => Batch = 1
        # 전체 데이터 => full batch 합 / 평균 => GD/GA
        predY = X[:, i].T @ W + B
        # Backward - BackPropagation
        loss = (Y[i] - predY) ** 2
        dLoss = -2 * (Y[i] - predY)  # 1/2

        # 노드 단위로 편미분을 수행
        dW = X[:, i] * 1 * dLoss
        # [Gradient방향 -] lr*(체인룰 편미분)
        W = W - lr * dW

        dB = 1 * dLoss  # f'(x)/|f'(x)|
        B = B - lr * dB
    # 모든 데이터 셋에 대해서 1번 다 돈이후 => 1-iteration

    if it % 100 == 0:
        history.append(np.sum((Y - (X.T @ W + B)) ** 2))

plt.plot(history), (X.T @ W + B) > 0.5

lr = h = 1e-5
ephoch = 10000

# [[0, 0, 1, 1], [0, 1, 0, 1]] => [[1,1,1,1], [0,0,1,1], [0,1,0,1]] => [[1,0,0], [1,0,1], [1,1,0], [1,1,1]] => [[0,0], [0,1], [1,0], [1,1]]
_X = np.vstack((np.ones(X.shape[-1]), X))  # bias를 포함한 입력값
W = np.random.rand(X.shape[0] + 1)  # 2개
history = list()
for it in range(epoch):
    # FeedFoward
    predY = _X.T @ W

    # Backward - BackPropagation
    loss = (Y - predY) ** 2
    dLoss = -2 * (Y - predY)

    MSE = np.mean(dLoss)
    SSE = np.sum(dLoss)

    # 노드 단위로 편미분을 수행
    dW = _X @ dLoss  # (3,4) * (4,) => (3,)  ====> WeightedSum(SSE)
    # [Gradient방향 -] lr*(체인룰 편미분)
    W = W - lr * dW

    if it % 100 == 0:
        history.append(MSE)

plt.plot(history), (_X.T @ W) > 0.5

logistic = lambda x: 1 / (1 + np.exp(-x))
dlogistic = lambda x: logistic(x) * (1 - logistic(x))
D = np.linspace(-5, 5, 100)
plt.plot(D, logistic(D), c="b")
plt.plot(D, dlogistic(D), c="r")
plt.axvline(0)
plt.axhline(0.5)

lr = h = 1e-3
epoch = 40000

W = np.random.rand(X.shape[0] + 1)

history = list()

_X = np.vstack((np.ones(X.shape[-1]), X))

# Loss = Error = 0; => Gradient Descent
BCE = NLL = lambda Y, _Y: -(Y * np.log(_Y) + (1 - Y) * np.log(1 - _Y))

for it in range(epoch):
    # Optimaizer = GD
    # SGD 바꿔보세요 X => x_i
    # FeedFoward
    Z = _X.T @ W  # Bias => W0 => X0=1
    predY = logistic(Z)

    # Backward - BackPropagation
    loss = BCE(Y, predY)
    dLoss = -(Y - predY)

    dZ = dlogistic(Z) * dLoss
    dW = _X @ dZ
    W = W - lr * dW

    if it % 100 == 0:
        history.append(np.sum(loss))

plt.plot(history), logistic(_X.T @ W) > 0.5
