from flask import Blueprint, render_template, request #,url_for
# from werkzeug.utils import redirect
import numpy as np

# with open('../../model','regression') as pickle_file:
#    model = pickle.load(pickle_file)

bp = Blueprint('regression', __name__, url_prefix='/regression')

@bp.route('/')
def regression_main():
    return render_template('main/regression.html')

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
    data = np.array(data_list)
    
    result = 'result' # = model 예측 결과
    
    # --- code for DB
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    init_regression_db()
    db_insert_data_regression(date, result, data_list)
    
    return render_template('result/regression_result.html', result = result) # result를 html로 보냅니다.

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
    
    results = get_regression_results()
    
    return render_template('DB/regression_log.html', results=results)
    