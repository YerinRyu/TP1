import sqlite3
import os
import pandas as pd

path = os.getcwd()

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

def regression_delete_result(ids):
    
    conn = sqlite3.connect(path+'/DB/regression_result.db')
    c = conn.cursor()
    
    for id in ids:
        c.execute('DELETE FROM regression_result WHERE Id = ?', (int(id),))
    
    conn.commit()
    
    c.execute('SELECT * FROM regression_result')
    results = c.fetchall()
    
    conn.close()
    
    return results


def log_to_csv():
    
    csv_file_path = path + '/dataset/log.csv'
    conn = sqlite3.connect(path + '/DB/regression_result.db')
    
    df = pd.read_sql_query('SELECT * FROM regression_result', conn)
    conn.close()

    df.to_csv(csv_file_path, index=False)  # CSV 파일로 저장

    return csv_file_path


        