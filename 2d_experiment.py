from collections import Counter
import math
from scipy.spatial import distance
import numpy as np
from sklearn import cluster

rows, cols = (5, 2)
x = [[0 for i in range(cols)] for j in range(rows)]

x[0]=[46,42]
x[1]=[45,46]
x[2]=[44,49]
x[3]=[48,45]
x[4]=[47,40]

rows, cols = (5, 2)
y = [[0 for i in range(cols)] for j in range(rows)]
y[0]=[20,21]
y[1]=[28,23]
y[2]=[27,28]
y[3]=[29,29]
y[4]=[26,29]

rows, cols = (10, 1)
Sx = [[0 for i in range(cols)] for j in range(rows)]
numerator = list()
denominator = list()
for i in range(5):
    tmp=0
    for k in range(5):
        if k != i:
            tmp += distance.euclidean(x[i], x[k])
            denominator.append(tmp)

for i in range(5):
    tmp=0
    for k in range(5):
        if k != i:
            tmp += distance.euclidean(y[i], y[k])
            denominator.append(tmp)
     
print(numerator)
for i in range(10):
    Sx[i]=denominator[i]
    Sx[i] = round(Sx[i],2)
print(Sx)
min = min(Sx)
max = max(Sx)
m=[0]*10
mL = 1
mU = 9
for i in range(10):

    frac = float((Sx[i] - min) / (max - min))
    m[i] = mL + (mU - mL) * ( math.pow(frac, 1))
    m[i] = round(m[i],2)
print(m)

