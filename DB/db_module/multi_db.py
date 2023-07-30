import sqlite3
import os

path = os.getcwd()

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


def multi_delete_result(ids):
    
    conn = sqlite3.connect(path+'/DB/multi_result.db')
    c = conn.cursor()

    for id in ids:
        c.execute('DELETE FROM multi_result WHERE Id = ?', (int(id),))

    conn.commit()
    
    c.execute('SELECT * FROM multi_result')
    results = c.fetchall()
    
    conn.close()
    
    return results