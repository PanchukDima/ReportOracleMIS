import requests
import cx_Oracle
import json
import os
os.environ['LD_LIBRARY_PATH'] = "/opt/oracle/product/18c/dbhomeXE/lib"
os.environ['ORACLE_HOME'] = "/opt/oracle/product/18c/dbhomeXE"
username = os.environ['ORACLE_USERNAME']
password = os.environ['ORACLE_PASSWORD']
database = os.environ['ORACLE_DATABASE']

def count_words_at_url():

    return "adasdadsasd"



def load_patients():
    data = {"data":[]}
    with cx_Oracle.connect(username, password, database) as connection:
        cursor = connection.cursor()
        for result in cursor.execute('select p.keyid, p.firstname, p.lastname, p.secondname from patient p'):
            data["data"].append(
                {
                 "keyid": result[0],
                 "firstname": result[1],
                 "lastname": result[2],
                 "secondname": result[3]
                 })
        return json.dumps(data)

def migrate_asov_to_ariadna():
    with cx_Oracle.connect(username, password, database) as connection:
        cursor = connection.cursor()
    return "OK"