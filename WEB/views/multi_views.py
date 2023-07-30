from flask import Blueprint, render_template, request, send_file
import os
import pandas as pd
from datetime import datetime

# module
import model.multi.MDNN_Multi_test as mt # model
from DB.db_module import multi_db as DB # DB

path = os.getcwd()
model, scaler, label_mapping = mt.load_model() # model 불러오기

bp = Blueprint('multi', __name__, url_prefix='/multi')

@bp.route('/')
def multi_main():
    return render_template('main/multi.html')

@bp.route('/csv_example_download', methods=['GET'])
def csv_example():
    return send_file(path+'/dataset/test_dataset/multi_test.csv')

# Model Predict
@bp.route('/result', methods=['GET','POST'])
def result():
    
    data_list = [request.form.get("col"+str(i+1)) for i in range(27)]
    result = mt.predict(data_list, model, scaler, label_mapping)
    
    # --- code for DB
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    DB.init_multi_db()
    DB.db_insert_data_multi(date, result, data_list)

    # send result to html
    return render_template('result/multi_result.html', result = result)


# csv file
@bp.route('/result_csv', methods=['GET', 'POST'])
def csv():
    try:
        csv_file = request.files['csv']
        file_path = path+'/dataset/user.csv'
        csv_file.save(file_path)
        
        results = mt.predict_csv(file_path, model, scaler, label_mapping)
        
        df = pd.read_csv(file_path)
        df['result'] = results
        df.to_csv(file_path)

        return render_template('result/csv/multi_csv_result.html', results = results) # result를 html로 보냅니다.

    except:
            return "파일 형식을 정확히하여 다시 시도하시기 바랍니다."

@bp.route('/result_csv/download')
def download_csv():
    file_path = path+'/dataset/user.csv'
    return send_file(file_path, as_attachment=True)

# result log
@bp.route('/log')
def log():
    
    results = DB.get_multi_results()
    
    return render_template('DB/multi_log.html', results=results)

@bp.route('/log', methods=['GET', 'POST'])
def delete():
    
    ids = request.form.getlist('ids')
    results = DB.multi_delete_result(ids)
    
    return render_template('DB/multi_log.html', results=results)

