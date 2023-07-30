from flask import Blueprint, render_template, request, send_file

from datetime import datetime
import os
import pandas as pd

import model.binary.binary as bn
from DB.db_module import binary_db as DB

path = os.getcwd()

bp = Blueprint('binary', __name__, url_prefix='/binary')

@bp.route('/')
def binary_main():
    return render_template('main/binary.html')

@bp.route('/csv_example_download', methods=['GET'])
def csv_example():
    return send_file(path+'/dataset/test_dataset/binary_test.csv')

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

@bp.route('/result', methods=['GET','POST'])
def result():
    
    data_list = [request.form.get("col"+str(i+1)) for i in range(8)]
    scaled_data = bn.scaler(data_list)
    result = bn.load_model_and_predict(scaled_data)
    
    # --- code for DB
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    DB.init_binary_db()
    DB.db_insert_data_binary(date, result, data_list)
    
    return render_template('result/binary_result.html', result=result) # result를 html로 보냅니다.

# csv file
@bp.route('/result_csv', methods=['GET', 'POST'])
def csv():
    
    try:
        csv_file = request.files['csv']
        file_path = path+'/dataset/user.csv'
        csv_file.save(file_path)
        
        results = bn.predict_csv(file_path)
        
        df = pd.read_csv(file_path)
        df['result'] = results
        df.to_csv(file_path)
        
        return render_template('result/csv/binary_csv_result.html', results = results)
    
    except:
        return "파일 형식을 정확히하여 다시 시도하시기 바랍니다."

@bp.route('/result_csv/download')
def download_csv():
    file_path = path+'/dataset/user.csv'
    return send_file(file_path, as_attachment=True)

# result log
@bp.route('/log')
def log():
    
    results = DB.get_binary_results()
    
    return render_template('DB/binary_log.html', results=results)

@bp.route('/log', methods=['GET', 'POST'])
def delete():
    
    ids = request.form.getlist('ids')
    results = DB.binary_delete_result(ids)
    
    return render_template('DB/binary_log.html', results=results)