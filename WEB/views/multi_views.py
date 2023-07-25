from flask import Blueprint, render_template, request #,url_for
import pickle
# from werkzeug.utils import redirect
import joblib
import os
import numpy as np

path = os.getcwd()

model_file_path = path+"/model/mlp_model_accuracy_0.78.joblib"
model = joblib.load(model_file_path)

with open(path+'/model/mlp_standard_scaler.pkl','rb') as pickle_file:
    scaler = pickle.load(pickle_file)

bp = Blueprint('multi', __name__, url_prefix='/multi')

@bp.route('/')
def multi_main():
    return render_template('main/multi.html')

@bp.route('/result', methods=['GET'])
def result():
    data = np.array([request.form.get("col"+str(i+1)) for i in range(27)])

    result = 'result' # = model 예측 결과
    return render_template('result/multi_result.html', result = result) # result를 html로 보냅니다.