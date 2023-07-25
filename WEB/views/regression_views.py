from flask import Blueprint, render_template, request #,url_for
# from werkzeug.utils import redirect
import numpy as np

# with open('../../model','regression') as pickle_file:
#    model = pickle.load(pickle_file)

bp = Blueprint('regression', __name__, url_prefix='/regression')

@bp.route('/')
def regression_main():
    return render_template('main/regression.html')

@bp.route('/result', methods=['GET'])
def result():
    
    data = np.array([request.form.get("col"+str(i+1)) for i in range(8)])
    result = 'result' # = model 예측 결과
    return render_template('result/regression_result.html', result = result) # result를 html로 보냅니다.