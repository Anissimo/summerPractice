from sqlite3 import connect
import pymysql
from config import host, user, password, db_name
# from uppy import _parameters_

# --- метод для генерации таблицы коэффициентов(восприимчивой для main.py)
def output_table_coeff(input_base_list):
    output_dictionary = {}
    for i in range(len(input_base_list)):
        output_dictionary[input_base_list[i]['unit']] = [input_base_list[i]['metre'], 
        input_base_list[i]['second'], input_base_list[i]['kilogram']]
    return output_dictionary

# --- метод для генерации таблицы единиц измерения(восприимчивой для main.py)
def output_table_unit(input_base_list):
    output_dictionary1 = {}
    for i in range(len(input_base_list)):
        output_dictionary1[input_base_list[i]['measurement']] = input_base_list[i]['unit']
    return output_dictionary1

try:
    
    connection = pymysql.connect(
    host = host,
    port = 3306,
    user = user,
    password = password,
    database = db_name,
    cursorclass = pymysql.cursors.DictCursor
    )
    # print("successfully connected...")

    try:
        with connection.cursor() as cursor:
            
            select_all_rows = f"SELECT * FROM table_init WHERE 1"
            cursor.execute(select_all_rows)
            # крч, тут выводим все строки, это уже метод sql
            # через цикл их надо крч вывести
            rows = cursor.fetchall()
            _table_coeff_ = output_table_coeff(rows)
            _table_unit_ = output_table_unit(rows)
            # print(_table_unit_)
    finally:
        connection.close()
except Exception as ex:
    print("Connection refused...")
    print(ex)

# print(_parameters_)






