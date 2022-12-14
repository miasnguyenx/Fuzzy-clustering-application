from collections import Counter
from sklearn import metrics
from sklearn.metrics import accuracy_score
import sklearn
from sklearn.metrics import davies_bouldin_score
import pandas as pd  # reading all required header files
import numpy as np
import random
import operator
import math
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.stats import multivariate_normal  # for generating pdf
from evaluationCriteria import EvaluationCriteria
import csv

# 50,52,77,101,106,113,119,121,123,126,127,133,138,142,146,149
class FuzzyCmeans:
    def __init__(self):
        self.maxIter = 100
        self.eps = math.pow(10, -6)
        self.e = 0.01

    def read_file(self, name):

        df_full = pd.read_csv(name)  # iris data
        # df_full.head()

        # Drop a column
        df_full = df_full.drop(["Id"], axis=1)
        df_full.shape

        columns = list(df_full.columns)  # column now is an array variable

        # features is column without species attribute
        features = columns[: len(columns) - 1]
        # print(features)
        self.class_labels = list(df_full[columns[-1]])
        # print(class_labels)
        self.df = df_full[features]
        self.n = len(self.df)

    def set_param(self, k, m):
        self.k = k
        self.m = m

    def accuracy(self, cluster_labels, class_labels):
        df = self.df
        correct_pred = 0
        # find max of a set base on key value as the element has the most occurences
        seto = max(set(cluster_labels[0:50]), key=cluster_labels[0:50].count)
        vers = max(set(cluster_labels[50:100]), key=cluster_labels[50:100].count)
        virg = max(set(cluster_labels[100:]), key=cluster_labels[100:].count)

        for i in range(len(df)):
            if cluster_labels[i] == seto and class_labels[i] == "Iris-setosa":
                correct_pred = correct_pred + 1
            if (
                cluster_labels[i] == vers
                and class_labels[i] == "Iris-versicolor"
                and vers != seto
            ):
                correct_pred = correct_pred + 1
            if (
                cluster_labels[i] == virg
                and class_labels[i] == "Iris-virginica"
                and virg != seto
                and virg != vers
            ):
                correct_pred = correct_pred + 1

        accuracy = correct_pred / len(df) * 100
        return accuracy

    def initializeMembershipMatrix(self):  # initializing the membership matrix
        n = self.n
        k = self.k
        membership_mat = []
        # initialize the membership maxtrix for each objects
        for i in range(n):
            random_num_list = [
                random.random() for i in range(k)
            ]  # random a k-values array

            summation = sum(random_num_list)  # sum of all values in array
            temp_list = [x / summation for x in random_num_list]

            # attach the object to a cluster (0,1,2) - respectively to three iris categories
            flag = temp_list.index(max(temp_list))
            for j in range(0, len(temp_list)):
                if j == flag:
                    temp_list[j] = 1
                else:
                    temp_list[j] = 0

            membership_mat.append(temp_list)
        return membership_mat

    # calculating the cluster center
    def calculateClusterCenter(self, membership_mat):
        n = self.n
        k = self.k
        df = self.df
        m = self.m
        cluster_mem_val = list(zip(*membership_mat))
        cluster_centers = []
        for j in range(k):
            x = list(cluster_mem_val[j])  # Uik
            xraised = [p ** m for p in x]  # Uik power by m
            denominator = sum(xraised)
            temp_num = []
            for i in range(n):
                data_point = list(df.iloc[i])
                prod = [xraised[i] * val for val in data_point]  # Uik^m * Xi
                temp_num.append(prod)
            # sum of list(zip(*temp_num)) is numerator of v[k]
            numerator = map(sum, list(zip(*temp_num)))
            center = [z / denominator for z in numerator]
            cluster_centers.append(center)

        return cluster_centers

    def updateMembershipValue(self, membership_mat, cluster_centers):
        m = self.m
        n = self.n
        df = self.df
        k = self.k
        p = float(2 / (m - 1))
        for i in range(n):
            x = list(df.iloc[i])
            distances = [
                np.linalg.norm(np.array(list(map(operator.sub, x, cluster_centers[j]))))
                for j in range(k)
            ]
            for j in range(k):
                den = sum(
                    [math.pow(float(distances[j] / distances[c]), p) for c in range(k)]
                )
                membership_mat[i][j] = float(1 / den)
        return membership_mat

    def getClusters(self, membership_mat):  # getting the clusters
        n = self.n
        cluster_labels = list()
        for i in range(n):
            # index of x - val is the value of enumerate list
            max_val, idx = max(
                (val, idx) for (idx, val) in enumerate(membership_mat[i])
            )
            cluster_labels.append(idx)
        return cluster_labels

    def FCM(self):  # Third iteration Random vectors from data
        # Membership Matrix
        membership_mat = self.initializeMembershipMatrix()
        curr = 0
        acc = []
        while curr < self.maxIter:
            cluster_centers = self.calculateClusterCenter(membership_mat)
            membership_mat = self.updateMembershipValue(membership_mat, cluster_centers)
            cluster_labels = self.getClusters(membership_mat)

            acc.append(cluster_labels)

            # if curr == 0:
            #     print("Cluster Centers:")
            #     print(np.array(cluster_centers))
            curr += 1
        # self.labels = cluster_labels
        # print("---------------------------")
        # print("Partition matrix:")
        # for i in range(0, 149):
        #     print(np.max(membership_mat[i]), np.array(
        #         membership_mat)[i], cluster_labels[i])
        # print(np.array(list(enumerate(cluster_labels))))
        # print(np.array(cluster_labels).shape)

        # a = self.accuracy(cluster_labels, self.class_labels)
        # print("Accuracy = ", a)
        self.cluster_labels = cluster_labels
        self.cluster_centers = cluster_centers
        self.acc = acc
        return cluster_labels, cluster_centers, acc

    def ASWC(self):
        array, result = EvaluationCriteria(self.df, self.cluster_labels,self.cluster_centers).ASWC()
        # X1 = EvaluationCriteria(self.df, self.cluster_labels)
        # array, result = X1.ASWC()
        return array, result
    def Davies_Bouldin_c(self):
        result = EvaluationCriteria(self.df, self.cluster_labels,self.cluster_centers).DB()
        # X1 = EvaluationCriteria(self.df, self.cluster_labels)
        # array, result = X1.ASWC()
        return result
    def Davies_Bouldin(self):
        b = sklearn.metrics.davies_bouldin_score(self.df, self.cluster_labels)
        b = round(b, 3)
        return b
    def SC(self):
        sc = sklearn.metrics.silhouette_score(self.df, self.cluster_labels)
        sc = round(sc, 3)
        return sc
    def Rand_score(self):
        r = sklearn.metrics.rand_score(self.cluster_labels, self.class_labels)
        r = round(r, 3)
        return r

    def Calinski_harabasz(self):
        c = metrics.calinski_harabasz_score(self.df, self.cluster_labels)
        c = round(c, 3)
        return c

X = FuzzyCmeans()
X.read_file("Iris.csv")
X.set_param(3, 10)
X.FCM()
print(X.Davies_Bouldin())
print(X.Rand_score())
print(X.Davies_Bouldin_c())
array, result = X.ASWC()
print(result)
