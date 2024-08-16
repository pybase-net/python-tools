from flask import current_app as app, jsonify
from .tasks import add, subtract
from .firebase import FirebaseConnector

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!"})


@app.post('/test-notification/<int:user_id>/<int:n>')
def test_notification(user_id, n):
    FirebaseConnector().update_user_notifications(user_id, n)
    return jsonify({"message": "success"})

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


@app.post('/custom-token/<user_id>')
def get_custom_token(user_id):
    # User ID for which to create a custom token
    additional_claims = {
    }  # Optional: Add custom claims as needed
    connector = FirebaseConnector()
    custom_token = connector.create_custom_token(user_id, additional_claims)
    return jsonify({
        "custom_token": custom_token
    })
