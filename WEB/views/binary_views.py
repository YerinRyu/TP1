from flask import Blueprint, render_template, request, send_file
from datetime import datetime
import sqlite3
import os
import model.binary.binary as bn
import pandas as pd

path = os.getcwd()

bp = Blueprint('binary', __name__, url_prefix='/binary')

@bp.route('/')
def binary_main():
    return render_template('main/binary.html')

@bp.route('/')
def csv_example():
    return send_file(path+'/dataset/test_dataset/binary_test.csv')


# ========================================================================= DB 함수
def init_binary_db():
    conn = sqlite3.connect(path+'/DB/binary_result.db')
    c = conn.cursor()
    
    # 테이블이 이미 존재하는지 확인하고, 없다면 새로 생성
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS binary_result(
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        DATE DATETIME,
                        result REAL,
                        Mean_of_the_integrated_profile REAL,
                        Standard_deviation_of_the_integrated_profile REAL,
                        Excess_kurtosis_of_the_integrated_profile REAL,
                        Skewness_of_the_integrated_profile REAL,
                        Mean_of_the_DM_SNR_curve REAL,
                        Standard_deviation_of_the_DM_SNR_curve REAL,
                        Excess_kurtosis_of_the_DM_SNR_curve REAL,
                        Skewness_of_the_DM_SNR_curve REAL
                        )
    '''

    c.execute(create_table_query)

    conn.commit()
    conn.close()
    
def db_insert_data_binary(date, result, data_list):
    # Connect to the database
    conn = sqlite3.connect(path+'/DB/binary_result.db')
    c = conn.cursor()

    # Define the INSERT statement
    insert_query = '''
        INSERT INTO binary_result (DATE, result, Mean_of_the_integrated_profile, 
                                 Standard_deviation_of_the_integrated_profile,
                                 Excess_kurtosis_of_the_integrated_profile,
                                 Skewness_of_the_integrated_profile, Mean_of_the_DM_SNR_curve,
                                 Standard_deviation_of_the_DM_SNR_curve,
                                 Excess_kurtosis_of_the_DM_SNR_curve,
                                 Skewness_of_the_DM_SNR_curve)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # Prepend the date and result value to the data_list
    data_list = [date, result] + data_list

    # Execute the INSERT statement with the data
    c.execute(insert_query, data_list)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_binary_results():
    conn = sqlite3.connect(path+'/DB/binary_result.db')
    c = conn.cursor()

    # 데이터 조회
    c.execute('SELECT * FROM binary_result')

    results = c.fetchall()

    conn.close()

    return results
# ========================================================================= DB 함수

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
    
    init_binary_db()
    db_insert_data_binary(date, result, data_list)
    
    return render_template('result/binary_result.html', result=result) # result를 html로 보냅니다.

# =============== csv file
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

# ================ result log
@bp.route('/log')
def log():
    
    results = get_binary_results()
    
    return render_template('DB/binary_log.html', results=results)