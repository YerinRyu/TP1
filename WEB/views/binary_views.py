from flask import Blueprint, render_template, request #,url_for
import pandas as pd
import numpy as np
import pickle
# from werkzeug.utils import redirect

model = None
# with open('../../model','binary') as pickle_file:
#    model = pickle.load(pickle_file)

bp = Blueprint('binary', __name__, url_prefix='/binary')

@bp.route('/')
def binary_main():
    return render_template('main/binary.html')

'''
col1: Mean of the integrated profile
col2: Standard deviation of the integrated profile
col3: Excess kurtosis of the integrated profile
col4: Skewness of the integrated profile
col5: Mean of the DM-SNR curve
col6: Standard deviation of the DM-SNR curve
col7: Excess kurtosis of the DM-SNR curve
col8: Skewness of the DM-SNR curve
'''

@bp.route('/result', methods=['GET'])
def result():
    
    data = np.array(np.array([request.form.get("col"+str(i+1)) for i in range(8)]))
    result = 'result'
    
    # result = model.predict(data) # = 모델 예측 결과
    
    return render_template('result/binary_result.html', result=result) # result를 html로 보냅니다.