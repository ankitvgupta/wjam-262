import os
import sys
import pdb
import traceback
from flask import Flask, render_template, request, jsonify
from RestAPIStub import RestAPIStub
from WireProtocolStub import WireProtocolStub
from requestprocessor import RequestProcessor

app = Flask(__name__)
app.debug = True

if sys.argv[1] == 'rest':
    stub = RestAPIStub()
else:
    stub = WireProtocolStub()

request_processor = RequestProcessor()

def process_request(request_object):
    mapping = {
        "GetMessages"   : request_processor.get_messages,
        "SendMessage"   : request_processor.send_message,
        "ListAccounts"  : request_processor.list_accounts,
        "DeleteAccount" : request_processor.delete_account,
        "CreateUser"    : request_processor.register_user,
        "GetGroups"     : request_processor.list_groups,
        "CreateGroup"   : request_processor.create_group,
    }
    return mapping[request_object["task"]](request_object)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE'])
def catch_all(path):
    try:
        request_object = stub.decode(path, request)
        return_object  = process_request(request_object)
        return stub.encode(return_object), 200
    except Exception,e:
        traceback.print_exc()
        return "failure!" + str(e), 201

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
    port = int(os.environ.get("PORT", 30978))
    app.run(host='0.0.0.0', port=port)
