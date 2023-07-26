from flask import Blueprint, render_template, request #,url_for
import pickle
# from werkzeug.utils import redirect
import joblib
import os
import numpy as np

path = os.getcwd()

model_file_path = path+"/model/mlp_model_accuracy_0.78.joblib"
model = joblib.load(model_file_path)

scaler_file_path = path+"/model/mlp_standard_scaler.joblib"
scaler = joblib.load(scaler_file_path)

bp = Blueprint('multi', __name__, url_prefix='/multi')

@bp.route('/')
def multi_main():
    return render_template('main/multi.html')


@bp.route('/result', methods=['GET','POST'])
def result():
    
    data = np.array([request.form.get("col"+str(i+1)) for i in range(27)]).reshape(1, -1)
    scaled_data = scaler.transform(data)

    result = model.predict(scaled_data)[0] # = model 예측 결과

    return render_template('result/multi_result.html', result = result) # result를 html로 보냅니다.

@bp.route('/result_csv', methods=['GET', 'POST'])
def csv():
    
    data = request.form.get("csv")
    
    result = None
    # scaled_data = scaler.transform(data)
    # result = model.predict(scaled_data)[0] # = model 예측 결과

    return render_template('result/multi_csv_result.html', result = result) # result를 html로 보냅니다.