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
    data = np.array(data_list)
    result = 'result'
    
    # --- code for DB
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    init_multi_db()
    db_insert_data_multi(date, result, data_list)
    
    # result = model.predict(data) # = 모델 예측 결과
    
    return render_template('result/binary_result.html', result=result) # result를 html로 보냅니다.

@bp.route('/log')
def log():
    
    results = get_binary_results()
    
    return render_template('DB/binary_log.html', results=results)