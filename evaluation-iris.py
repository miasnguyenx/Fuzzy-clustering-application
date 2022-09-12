import sklearn
from fuzzyCmeans import FuzzyCmeans
from mcfcmPhase2 import MCFCMeansPhase2
from mcfcmPhase2_concen import MCFCMeansPhase2_2
from evaluationCriteria import EvaluationCriteria
import numpy as np
import pandas as pd

silhouette = list()
silhouette_c = list()
bouldin = list()
alpha = list()
randindex = list()
bouldin_c = list()
alpha_arr = np.arange(0.5, 5, 0.5)
# print(len(alpha_arr))
# exit()

for i in alpha_arr:
    X = MCFCMeansPhase2()
    X.read_file("Iris.csv")
    X.set_param(3, 1.1, 9.1, i)
    labels, centers, acc = X.MCFCM_phase2()
    df = X.df
    X1 = EvaluationCriteria(df, labels, centers)
    tmp, a = X1.ASWC()
    a = round(a, 3)
    b_real = X1.DB()
    b_real = round(b_real, 3)
    b = sklearn.metrics.davies_bouldin_score(X.df, labels)
    b = round(b, 3)
    r = sklearn.metrics.rand_score(labels, X.class_labels)
    r = round(r, 3)
    sc = X.SC()
    sc = round(sc, 3)
    
    bouldin_c.append(b_real)
    silhouette.append(a)
    silhouette_c.append(sc)
    bouldin.append(b)
    randindex.append(r)
    del X
    del X1
    print("------", i, "------")


print(silhouette)
print(silhouette_c)
print(bouldin)
# print(bouldin_c)
print(randindex)

