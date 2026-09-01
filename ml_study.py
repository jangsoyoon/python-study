from sklearn.datasets import load_wine
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt
import seaborn as sns

data = load_wine(as_frame=True)
# print(data.DESCR)
wine = data.frame
# print(wine.info())
# print(wine.describe())
win_no_class = wine.iloc[:, :-1]
# win_no_class.describe()
# win_no_class.boxplot(figsize=(14, 3))
# win_no_class.iloc[:, :-1].boxplot(figsize=(14, 3))
# plt.show()

# sns.pairplot(wine, hue="target")
# plt.show()

data = load_breast_cancer(as_frame=True)
# print(data.frame.info())
iris = sns.load_dataset("iris")
# print(iris.info()) # 5개의 column, 150 개의 데이터

#! EDA? -> 탐색적 데이터 분석 / 데이터를 본격적으로 모델링하거나 가설을 검정하기 전, 다양한 각도에서 관찰하고 이해하는 기초 분석 과정
#! learning curve?
sns.pairplot(iris, hue="species")
plt.show()
