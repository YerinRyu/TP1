from flask import Blueprint, render_template, request, send_file
# from werkzeug.utils import redirect
import os
import sqlite3
from datetime import datetime
import model.multi.MDNN_Multi_test as mt
import pandas as pd

path = os.getcwd()
model, scaler, label_mapping = mt.load_model() # model 불러오기

bp = Blueprint('multi', __name__, url_prefix='/multi')

@bp.route('/')
def multi_main():
    return render_template('main/multi.html')

@bp.route('/')
def csv_example():
    return send_file(path+'/dataset/test_dataset/multi_test.csv')

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
    result = mt.predict(data_list, model, scaler, label_mapping)
    
    # --- code for DB
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    init_multi_db()
    db_insert_data_multi(date, result, data_list)

    # send result to html
    return render_template('result/multi_result.html', result = result)



# =============== csv file
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

# ================ result log
@bp.route('/log')
def log():
    
    results = get_multi_results()
    
    return render_template('DB/multi_log.html', results=results)
    

