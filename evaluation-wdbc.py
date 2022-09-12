import sklearn
from mcfcmPhase2 import MCFCMeansPhase2
from mcfcmPhase2_concen import MCFCMeansPhase2_2
from evaluationCriteria import EvaluationCriteria
import numpy as np

silhouette = list()
bouldin = list()
alpha = list()
randindex = list()
calin = list()
alpha_arr = np.arange(0.5, 5, 0.5)
# print(len(alpha_arr))
# exit()

for i in alpha_arr:
    X = MCFCMeansPhase2_2()
    X.read_file("WDBC.csv")
    X.set_param(2, 2, 3.1, 9.1, i)
    labels, centers, acc = X.MCFCM_phase2_2()
    df = X.df
    X1 = EvaluationCriteria(df, labels, centers)
    tmp, a = X1.ASWC()
    a = round(a, 3)
    b = sklearn.metrics.davies_bouldin_score(X.df, labels)
    b = round(b, 3)
    r = sklearn.metrics.rand_score(labels, X.class_labels)
    r = round(r, 3)
    c = X.Calinski_harabasz()
    calin.append(c)
    silhouette.append(a)
    bouldin.append(b)
    randindex.append(r)
    del X
    del X1
    print("------", i, "------")


print(silhouette)
print(bouldin)
print(randindex)
