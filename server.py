import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# userId -> user object
users    = {}
# groupId -> list of userIds
groups   = {}
# userId -> pending messages
messages = {}

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    print request
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': tasks}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
