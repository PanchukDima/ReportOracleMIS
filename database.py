import cx_Oracle
import os
os.environ['LD_LIBRARY_PATH'] = "/opt/oracle/product/18c/dbhomeXE/lib"
os.environ['ORACLE_HOME'] = "/opt/oracle/product/18c/dbhomeXE"
username = os.environ['ORACLE_USERNAME']
password = os.environ['ORACLE_PASSWORD']
database_name = os.environ['ORACLE_DATABASE']


class database():
    def __init__(self):
        self.connection = self.connectToDB()
    def connectToDB(self):
        with cx_Oracle.connect(username, password, database_name) as connection:
            return connection

    def loginSQLOnlyPass(self, sqlpass):
        with cx_Oracle.connect(username, password, database_name) as connection:
            cursor = connection.cursor()
            data = cursor.execute("select count(m.keyid) from man m WHERE m.pass = '%s' " % sqlpass)
            data = data.fetchone()
            if data[0] > 0:
                data = cursor.execute("select m.keyid, m.text from man m WHERE m.pass = '%s' " % sqlpass)
                data = data.fetchone()
                return True, data[0], data[1]
            else:
                return False
            return False
    def getListTasks(self, userid):
        with cx_Oracle.connect(username, password, database_name) as connection:
            cursor = connection.cursor()
            data = cursor.execute("select keyid, userid, taskid, nametask, ttl, datestart, datestop, status from gp54_admin.task WHERE userid = '%s' " % userid)
            data = data.fetchone()
            if data[0] > 0:
                return True
            else:
                return False
            return False
    def callSql(self, sqltext):
        with cx_Oracle.connect(username, password, database_name) as connection:
            cursor = connection.cursor()
            data = cursor.execute(sqltext)
            return True
