import cx_Oracle
import os
os.environ['LD_LIBRARY_PATH'] = "/opt/oracle/product/18c/dbhomeXE/lib"
os.environ['ORACLE_HOME'] = "/opt/oracle/product/18c/dbhomeXE"
username = os.environ['ORACLE_USERNAME']
password = os.environ['ORACLE_PASSWORD']
database_name = os.environ['ORACLE_DATABASE']


class database():
    def __init__(self):
        self.connection = self.connect()
    def connect(self):
        with cx_Oracle.connect(username, password, database_name) as connection:
            return connection

    def loginSQLOnlyPass(self, sqlpass):
        cursor = self.connection.cursor()
        data = cursor.execute('select count(m.keyid) from man m WHERE m.password = %s' % sqlpass)
        if data[0] > 0:
            return True
        else:
            return False
        return False
