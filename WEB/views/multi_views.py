from flask import Blueprint, render_template, request #,url_for
import pickle
# from werkzeug.utils import redirect
import joblib
import os
import numpy as np
import sqlite3
from datetime import datetime

path = os.getcwd()

model_file_path = path+"/model/mlp_model_accuracy_0.78.joblib"
model = joblib.load(model_file_path)

scaler_file_path = path+"/model/mlp_standard_scaler.joblib"
scaler = joblib.load(scaler_file_path)

bp = Blueprint('multi', __name__, url_prefix='/multi')

@bp.route('/')
def multi_main():
    return render_template('main/multi.html')

# ========================================================================= DB 함수
def init_multi_db():
    conn = sqlite3.connect(path+'/DB/multi_result.db')
    c = conn.cursor()
    
    # 테이블이 이미 존재하는지 확인하고, 없다면 새로 생성
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS multi_result(
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        DATE DATETIME,
                        RESULT CHAR,
                        X_Minimum REAL,
                        X_Maximum REAL,
                        Y_Minimum REAL,
                        Y_Maximum REAL,
                        Pixels_Areas REAL,
                        X_Perimeter REAL,
                        Y_Perimeter REAL,
                        Sum_of_Luminosity REAL,
                        Minimum_of_Luminosity REAL,
                        Maximum_of_Luminosity REAL,
                        Length_of_Conveyer REAL,
                        TypeOfSteel_A300 REAL,
                        TypeOfSteel_A400 REAL,
                        Steel_Plate_Thickness REAL,
                        Edges_Index REAL,
                        Empty_Index REAL,
                        Square_Index REAL,
                        Outside_X_Index REAL,
                        Edges_X_Index REAL,
                        Edges_Y_Index REAL,
                        Outside_Global_Index REAL,
                        LogOfAreas REAL,
                        Log_X_Index REAL,
                        Log_Y_Index REAL,
                        Orientation_Index REAL,
                        Luminosity_Index REAL,
                        SigmoidOfAreas REAL)'''

    c.execute(create_table_query)

    conn.commit()
    conn.close()
    

def db_insert_data_multi(date, result, data_list):

    # Connect to the database
    conn = sqlite3.connect(path+'/DB/multi_result.db')
    c = conn.cursor()

    # Define the INSERT statement
    insert_query = '''
        INSERT INTO multi_result (DATE, result, X_Minimum, X_Maximum, Y_Minimum, Y_Maximum, Pixels_Areas,
                                X_Perimeter, Y_Perimeter, Sum_of_Luminosity, Minimum_of_Luminosity, Maximum_of_Luminosity,
                                Length_of_Conveyer, TypeOfSteel_A300, TypeOfSteel_A400, Steel_Plate_Thickness, Edges_Index,
                                Empty_Index, Square_Index, Outside_X_Index, Edges_X_Index, Edges_Y_Index,
                                Outside_Global_Index, LogOfAreas, Log_X_Index, Log_Y_Index, Orientation_Index,
                                Luminosity_Index, SigmoidOfAreas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # DATA
    data_list = [date, result] + data_list

    # Execute the INSERT statement with the data
    c.execute(insert_query, data_list)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_multi_results():
    conn = sqlite3.connect(path+'/DB/multi_result.db')
    c = conn.cursor()

    # 데이터 조회
    c.execute('SELECT * FROM multi_result')

    results = c.fetchall()

    conn.close()

    return results
# ========================================================================= DB 함수


# ========================================================================= Model Predict
@bp.route('/result', methods=['GET','POST'])
def result():
    
    data_list = [request.form.get("col"+str(i+1)) for i in range(27)]
    data = np.array(data_list).reshape(1, -1)
    scaled_data = scaler.transform(data)
    
    # result = result of model predicted
    result = model.predict(scaled_data)[0]
    
    # --- code for DB
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    init_multi_db()
    db_insert_data_multi(date, result, data_list)

    # send result to html
    return render_template('result/multi_result.html', result = result)


# =============== csv file
@bp.route('/result_csv', methods=['GET', 'POST'])
def csv():
    
    data = request.form.get("csv")
    
    result = None
    # scaled_data = scaler.transform(data)
    # result = model.predict(scaled_data)[0] # = model 예측 결과

    return render_template('result/multi_csv_result.html', result = result) # result를 html로 보냅니다.

# ================ result log
@bp.route('/log')
def log():
    
    results = get_multi_results()
    
    return render_template('DB/multi_log.html', results=results)
    

