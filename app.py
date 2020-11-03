from flask import Flask
import time
from rq import Queue
from redis import Redis
from flask import Flask, render_template, request, session, redirect, url_for
from tasks import load_patients
from database import database
import json
functions = {"load_patients": load_patients}
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'db35c5ed2e96475086bc44599b7f54e1'
queue = Queue(connection=Redis(), default_timeout=3600)

@app.route('/')
def hello_world():
    if 'userauth' in session:
        List_commands = ["load_patients"]
        return render_template('index.html', List_commands=List_commands)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        db = database()
        status, userid, username = db.loginSQLOnlyPass(request.form['password'])
        if status:
            session['userauth'] = 1
            session['userid'] = userid
            session['username'] = username
            return redirect('/')
        else:
            return "Bye"
    return "Bue"
@app.route('/logout')
def logout():
    session.pop('userauth', None)
    session.pop('userid', None)
    session.pop('username', None)
    return redirect('/')

@app.route('/listtask')
def showListTasks():
    list_dep = ["0","1","2","3","4","5","6"]
    return render_template('listtasks.html')

@app.route('/createTask', methods=['GET', 'POST'])
def createTask():
    if request.method == 'POST':
        if request.form['typedata'] == 'exportoms':


        return "Ok"

@app.route('/task/<func>')
def create_task(func):
    job = queue.enqueue(functions[func], result_ttl=86400)
    return job.id

@app.route('/result/<id>')
def result_task(id):
    try:
        job = queue.fetch_job(id)
        print(job.get_status())
        if job.is_finished:
            return json.dumps(job.result, ensure_ascii=False)
        else:
            return 'Not ready', 202
    except:
        return "Not found", 404
@app.route('/tasks')
def get_list_queue():
    db = database()
    return db.getListTasks(session['userid'])

@app.route('/queue/clear')
def clear_queue():
    queue.empty()
    return "Clear"

@app.route('/exportoms')
def show_export():
    db = database()
    db_eis = db.getEISBD()
    type_visit = db.getTypeVisit()
    visit_purpose = db.getVisitPurpose()
    list_dep = db.getDepList()
    return render_template("exportOMS.html",
                           list_dep=list_dep,
                           db_eis=db_eis,
                           type_visit=type_visit,
                           visit_purpose=visit_purpose)


if __name__ == '__main__':
    app.run()
