from collections import Counter
import math
from scipy.spatial import distance
import numpy as np
from sklearn import cluster

class EvaluationCriteria:
    def __init__(self, df, labels, centers):
        self.df = df
        self.n = len(df)
        self.k = len(set(labels))
        self.labels = labels
        self.centers = centers

    def initDistancesMatrix(self):
        n = self.n
        df = self.df
        rows, cols = (n, n)
        dst = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(n):
            x = list(df.iloc[i])
            for j in range(n):
                y = list(df.iloc[j])
                dst[i][j] = distance.euclidean(x, y)
        return dst

    def DB(self):
        n = self.n
        k = self.k
        labels = self.labels
        df = self.df
        centers = self.centers
        dst = self.initDistancesMatrix()
        DB = 0
        occ = Counter(labels)
        djk = np.zeros((k, k))
        rows, cols = (k, 1)
        cluster_couples = [[0 for i in range(cols)] for j in range(rows)]
        
        # print(np.array(centers))
        for i in range(k):
            for j in range(k):
                djk[i][j] = distance.euclidean(centers[i], centers[j])
        # print(djk)
        dj = [0]*k
        for i in range(k):
            center = centers[i]
            label = labels[i]
            for j in range(n):
                if labels[j] == label:
                    x = df.iloc[j]
                    dj[i] += distance.euclidean(x, center)
            dj[i] /= occ[i]
        # print(dj)
        
        for i in range(k):
            Dj_max = 0
            for j in range(k):
                if i != j:
                    x = (dj[i] + dj[j]) / djk[i][j]
                    if x > Dj_max:
                        Dj_max = x
                        cluster_couples[i].clear()
                        cluster_couples[i].append(i)
                        cluster_couples[i].append(j)
            DB += Dj_max
            print(DB)
        
        print(cluster_couples)
        DB /= k
        # print("DB_index: ", DB)
        return DB
        
    def ASWC(self):
        n = self.n
        k = self.k
        labels = self.labels
        df = self.df
        eps = math.pow(10, -6)
        dst = self.initDistancesMatrix()
        rows, cols = (n, k)
        InterAVGdist = [[0 for i in range(cols)] for j in range(rows)]
        IntraAVGdist = [0]*n
        minInterAVG = [0]*n
        occ = Counter(labels)

        rows, cols = (k, n+1)
        cluster = [[0 for i in range(cols)] for j in range(rows)]
        count = 0

        for i in range(n):
            label = labels[i]
            for j in range(n):
                if labels[j] == label:
                    IntraAVGdist[i] += dst[i][j]
                    count += 1
            IntraAVGdist[i] /= count
            count = 0

        # for i in range(n):
        #     x = list(df.iloc[i])
        #     y = labels[i]
        #     cluster[y].append(x)

        for i in range(n):
            for j in range(n):
                if labels[j] != labels[i]:
                    t = labels[j]
                    InterAVGdist[i][t] += dst[i][j]

        # print(np.array(InterAVGdist))
        ASWC_matrix = [0]*n
        for i in range(n):
            for j in range(k):
                if InterAVGdist[i][j] != 0:
                    InterAVGdist[i][j] /= occ[j]

            InterAVGdist[i].sort()
            minInterAVG[i] = InterAVGdist[i][1]
            ASWC_matrix[i] = minInterAVG[i] / (IntraAVGdist[i] + eps)
        print(np.array(InterAVGdist))
        print(np.array(IntraAVGdist))

        ASWC = sum((minInterAVG[i] / (IntraAVGdist[i] + eps))
                   for i in range(n))
        ASWC /= n
        # print(np.array(ASWC_matrix))
        # print("ASWC_index: ", ASWC)
        return ASWC_matrix, ASWC
