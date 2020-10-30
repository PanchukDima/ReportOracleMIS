from flask import Flask
import time
from rq import Queue
from redis import Redis
from flask import Flask, render_template, request
from tasks import load_patients, valid_login
import json
functions = {"load_patients": load_patients}
app = Flask(__name__)
queue = Queue(connection=Redis(), default_timeout=3600)

@app.route('/')
def hello_world():
    List_commands = ["load_patients"]
    return render_template('index.html', my_string="Список доступных комманд", List_commands=List_commands)

@app.route('/task/<func>')
def create_task(func):
    job = queue.enqueue(functions["load_patients"], result_ttl=86400)
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
@app.route('/queue')
def get_list_queue():
    queued_job_ids = queue.job_ids
    print(queued_job_ids)
    return "queued"
@app.route('/queue/clear')
def clear_queue():
    queue.empty()
    return "Clear"
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':


if __name__ == '__main__':
    app.run()
