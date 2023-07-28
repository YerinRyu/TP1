from flask import Blueprint, render_template, request, send_file
import os
import sqlite3
import model.regression.torch_AnnModel1_test as rg
from datetime import datetime
import pandas as pd

path = os.getcwd()

bp = Blueprint('regression', __name__, url_prefix='/regression')

@bp.route('/')
def regression_main():
    return render_template('main/regression.html')

@bp.route('/')
def csv_example():
    return send_file(path+'/dataset/test_dataset/regression_test.csv')

# ========================================================================= DB 함수
def init_regression_db():
    conn = sqlite3.connect(path+'/DB/regression_result.db')
    c = conn.cursor()
    
    # 테이블이 이미 존재하는지 확인하고, 없다면 새로 생성
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS regression_result(
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        DATE DATETIME,
                        result REAL,
                        Sex REAL,
                        Length REAL,
                        Diameter REAL,
                        Height REAL,
                        Whole_weight REAL,
                        Shucked_weight REAL,
                        Viscera_weight REAL,
                        Shell_weight REAL
                        )
    '''

    c.execute(create_table_query)

    conn.commit()
    conn.close()

def db_insert_data_regression(date, result, data_list):
    
    # Connect to the database
    conn = sqlite3.connect(path+'/DB/regression_result.db')
    c = conn.cursor()

    # Define the INSERT statement
    insert_query = '''
        INSERT INTO regression_result (DATE, result, Sex, Length, Diameter, Height, Whole_weight,
                                 Shucked_weight, Viscera_weight, Shell_weight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Prepend the date and result value to the data_list
    data_list = [date, result] + data_list

    # Execute the INSERT statement with the data
    c.execute(insert_query, data_list)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_regression_results():
    conn = sqlite3.connect(path+'/DB/regression_result.db')
    c = conn.cursor()

    # 데이터 조회
    c.execute('SELECT * FROM regression_result')

    results = c.fetchall()

    conn.close()

    return results
    
# ========================================================================= DB 함수

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
    
    init_regression_db()
    db_insert_data_regression(date, result, data_list)
    
    return render_template('result/regression_result.html', result = result) # result를 html로 보냅니다.

# =============== csv file
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

# ================ result log
@bp.route('/log')
def log():
    
    results = get_regression_results()
    
    return render_template('DB/regression_log.html', results=results)
    