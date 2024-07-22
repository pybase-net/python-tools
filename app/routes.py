from flask import current_app as app, jsonify
from .tasks import add, subtract

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!"})


@app.route('/add/<int:a>/<int:b>')
def add_numbers(a, b):
    result = add.delay(a, b)
    return jsonify({"task_id": result.id})


@app.route('/subtract/<int:a>/<int:b>')
def subtract_numbers(a, b):
    result = subtract.delay(a, b)
    return jsonify({"task_id": result.id})


@app.route('/result/<task_id>')
def get_result(task_id):
    result = app.extensions['celery'].AsyncResult(task_id)
    if result.state == 'SUCCESS':
        return jsonify({"result": result.result})
    else:
        return jsonify({"state": result.state})
