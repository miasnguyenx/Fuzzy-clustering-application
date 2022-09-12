from flask import Flask, request, redirect, render_template
import json
# import fuzzyCmeans
# from mcfcmPhase2 import MCFCMeansPhase2
from mcfcmPhase2_concen import MCFCMeansPhase2_2
from mcfcmPhase2_ASWC import MCFCMeansPhase2
import numpy as np
# from evaluationCriteria import EvaluationCriteria
from mcFuzzyCmeans import MCFuzzyCmeans

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/result', methods=['POST', 'GET'])
# def result():
#     # dataset = request.form['dataset']
#     input = request.form['inputData']
#     print(input)
#     print(type(input))

#     file = open("userData.csv", "w")
#     file.write(input)
#     file.close
#     mU = float(request.form['mU'])
#     mL = float(request.form['mL'])
#     k = int(request.form['k'])
#     alpha = float(request.form['alpha'])
#     X = MCFCMeansPhase2()
#     X.read_file("Iris.csv")
#     X.set_param(k, m, mL, mU, alpha)
#     X.MCFCM_phase2()
#     tmp, aswc = X.ASWC()
#     bouldin = X.Davies_Bouldin()
#     rand = X.Rand_score()
#     c = X.Calinski_harabasz()
#     matrix = X.membership_mat
#     cluster_center = np.array(X.cluster_centers)
#     cluster_label = X.cluster_labels
#     res = dict()
#     res['aswc'] = aswc
#     res['bouldin'] = bouldin
#     res['matrix'] = matrix
#     res['rand'] = rand
#     res['cluster_center'] = cluster_center
#     res['cluster_label'] = cluster_label
#     return render_template('result.html', res=res)


@app.route('/result_mcfcm', methods=['POST', 'GET'])
def result_mcfcm():
    # dataset = request.form['dataset']
    input = request.form['inputData']
    # m = float(request.form['fuzzyCoeff'])
    mU = float(request.form['mU'])
    mL = float(request.form['mL'])
    k = int(request.form['k'])
    alpha = float(request.form['alpha'])
    print(input)
    print(type(input))
    file = open("userData.csv", "w")
    file.write(input)
    file.close()
    X = MCFuzzyCmeans()
    X.read_file_from_user()
    X.set_param(k, mL, mU, alpha)
    X.MCFCM()
    tmp, aswc = X.ASWC()
    bouldin = X.Davies_Bouldin()
    matrix = X.membership_mat
    cluster_center = np.array(X.cluster_centers)
    cluster_label = X.cluster_labels
    res = dict()
    res['aswc'] = aswc
    res['bouldin'] = bouldin
    res['matrix'] = matrix
    res['cluster_center'] = cluster_center
    res['cluster_label'] = cluster_label
    res['num_elm'] = X.n
    res['elm_id'] = X.elm_id
    res['df'] = X.df.to_numpy()
    res['num_cluster'] = X.k
    return render_template('result.html', res=res)

@app.route('/result_mcfcm_1', methods=['POST', 'GET'])
def result_mcfcm1():
    # dataset = request.form['dataset']
    input = request.form['inputData']
    # m = float(request.form['fuzzyCoeff'])
    mU = float(request.form['mU'])
    mL = float(request.form['mL'])
    k = int(request.form['k'])
    alpha = float(request.form['alpha'])
    print(input)
    print(type(input))
    file = open("userData.csv", "w")
    file.write(input)
    file.close()
    X = MCFCMeansPhase2()
    X.read_file_from_user()
    X.set_param(k, mL, mU, alpha)
    X.MCFCM_phase2()
    tmp, aswc = X.ASWC()
    bouldin = X.Davies_Bouldin()
    matrix = X.membership_mat
    cluster_center = np.array(X.cluster_centers)
    cluster_label = X.cluster_labels
    res = dict()
    res['aswc'] = aswc
    res['bouldin'] = bouldin
    res['matrix'] = matrix
    res['cluster_center'] = cluster_center
    res['cluster_label'] = cluster_label
    res['num_elm'] = X.n
    res['elm_id'] = X.elm_id
    res['df'] = X.df.to_numpy()
    res['num_cluster'] = X.k
    return render_template('result.html', res=res)

@app.route('/result_mcfcm_2', methods=['POST', 'GET'])
def result_mcfcm2():
    # dataset = request.form['dataset']
    input = request.form['inputData']
    # m = float(request.form['fuzzyCoeff'])
    mU = float(request.form['mU'])
    mL = float(request.form['mL'])
    k = int(request.form['k'])
    alpha = float(request.form['alpha'])
    print(input)
    print(type(input))
    file = open("userData.csv", "w")
    file.write(input)
    file.close()
    X = MCFCMeansPhase2_2()
    X.read_file_from_user()
    X.set_param(k, mL, mU, alpha)
    X.MCFCM_phase2_2()
    tmp, aswc = X.ASWC()
    bouldin = X.Davies_Bouldin()
    matrix = X.membership_mat
    cluster_center = np.array(X.cluster_centers)
    cluster_label = X.cluster_labels
    res = dict()
    res['aswc'] = aswc
    res['bouldin'] = bouldin
    res['matrix'] = matrix
    res['cluster_center'] = cluster_center
    res['cluster_label'] = cluster_label
    res['num_elm'] = X.n
    res['elm_id'] = X.elm_id
    res['df'] = X.df.to_numpy()
    res['num_cluster'] = X.k
    return render_template('result.html', res=res)
if __name__ == '__main__':
    app.run(debug=True)