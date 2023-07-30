from flask import Blueprint, render_template, request, send_file

import os
from datetime import datetime
import pandas as pd

import model.regression.torch_AnnModel1_test as rg
from DB.db_module import regression_db as DB

path = os.getcwd()

bp = Blueprint('regression', __name__, url_prefix='/regression')

@bp.route('/')
def regression_main():
    return render_template('main/regression.html')

@bp.route('/csv_example_download', methods=['GET'])
def csv_example():
    return send_file(path+'/dataset/test_dataset/regression_test.csv')

'''
col1: Sex
col2: Length
col3: Diameter
col4: Height
col5: Whole weight
col6: Shucked weight
col7: Viscera weight
col8: Shell weight
'''

@bp.route('/result', methods=['GET','POST'])
def result():
    
    data_list = [request.form.get("col"+str(i+1)) for i in range(8)]
    result = rg.load_predict(data_list)
    
    # --- code for DB
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    DB.init_regression_db()
    DB.db_insert_data_regression(date, result, data_list)
    
    return render_template('result/regression_result.html', result = result) # result를 html로 보냅니다.

# csv file
@bp.route('/result_csv', methods=['GET', 'POST'])
def csv():
    
    try:
        csv_file = request.files['csv']
        file_path = path+'/dataset/user.csv'
        csv_file.save(file_path)
        
        results = rg.load_predict_csv(file_path)
        
        df = pd.read_csv(file_path)
        df['result'] = results
        df.to_csv(file_path)

        return render_template('result/csv/regression_csv_result.html', results = results) # result를 html로 보냅니다.
    
    except:
        return "파일 형식을 정확히하여 다시 시도하시기 바랍니다."

@bp.route('/result_csv/download')
def download_csv():
    file_path = path+'/dataset/user.csv'
    return send_file(file_path, as_attachment=True)

# log
@bp.route('/log')
def log():
    
    results = DB.get_regression_results()
    
    return render_template('DB/regression_log.html', results=results)

@bp.route('/log', methods=['GET', 'POST'])
def delete():
    
    ids = request.form.getlist('ids')
    results = DB.regression_delete_result(ids)
    
    return render_template('DB/regression_log.html', results=results)