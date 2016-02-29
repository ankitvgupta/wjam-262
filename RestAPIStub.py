import json
import pdb

class RestAPIStub:
	def __init__(self):
		pass

	def encode(self, ret):
		return ret
	
	def decode(self, path, request):
		path_values = path.split("/")
		target = path_values[0]
		return_object = {}
		request_json = json.loads(request.data)
		assert(request_json)
		if path_values[0] == "users" and request.method == "GET" and len(path_values) == 1:
			return_object["username"] = request_json['username']
			return_object["password"] = request_json['password']
			return_object["task"] = "ListAccounts"
			return return_object
		elif path_values[0] == "users" and request.method == "DELETE" and len(path_values) == 1:
			return_object["username"] = request_json['username']
			return_object["password"] = request_json['password']
			return_object["task"] = "DeleteAccount"
			return return_object
		elif path_values[0] == "users" and request.method == "POST" and len(path_values) == 1:
			return_object["username"] = request_json['username']
			return_object["password"] = request_json['password']
			return_object["task"] = "CreateUser"
			return return_object
		elif path_values[0] == "groups" and request.method == "GET" and len(path_values) == 1:
			return_object["username"] = request_json["username"]
			return_object["password"] = request_json["password"]
			return_object["task"] = "GetGroups"
			return return_object
		elif path_values[0] == "groups" and request.method == "POST" and len(path_values) == 1:
			return_object["username"] = request_json["username"]
			return_object["password"] = request_json["password"]
			return_object["groupname"] = request_json["groupname"]
			return_object["groupusers"] = request_json["groupusers"]
			return_object["task"] = "CreateGroup"
			return return_object
		elif path_values[0] == "users" and path_values[2] == "messages" and request.method == "GET":
			return_object["username"] = path_values[1]
			return_object["password"] = request_json["password"]
			return_object["task"] = "GetMessages"
			return return_object
		elif path_values[0] == "users" and path_values[2] == "messages" and request.method == "POST":
			return_object["username"] = path_values[1]
			return_object["password"] = request_json["password"]
			return_object["message"] = request_json["message"]
			return_object["groupname"] = path_values[1]
			return_object["task"] = "SendMessage"
			return return_object
		else:
			return_object["task"] = "INVALID"
		return return_object
