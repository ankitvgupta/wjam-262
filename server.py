import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

if sys.argv[2] == 'rest':
    stub = RestAPIStub()
else:
    stub = WireProtocolStub()

# Initialize stub
# Initialize processor

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE'])
def catch_all(path):
    request_object = stub.decode(path, request)
    #if request_object["type"] == TYPEA
    #    request_processor.TYPEA()

# @app.route("/")
# def hello():
#     return render_template('index.html')

# @app.route('/todo/api/v1.0/tasks', methods=['POST'])
# def create_task():
#     print request
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': tasks}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
