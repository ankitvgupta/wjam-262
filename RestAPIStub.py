
class RestAPIStub:
	def __init__(self):
		pass

	def decode(self, path, request):
		path_values = path.split("/")
		target = path_values[0]
		return_object = {}
		assert(request.json)
		if path_values[0] == "users" and path_values[1] == "create":
			return_object["username"] = request.json['username']
			return_object["password"] = request.json['password']
			return_object["task"] = "CreateUser"
			return return_object
		elif path_values[0] == "users" and path_values[1] == "list":
			return_object["username"] = request.json['username']
			return_object["password"] = request.json['password']
			return_object["task"] = "ListAccounts"
			return return_object
		elif path_values[0] == "users" and path_values[1] == "delete":
			return_object["username"] = request.json['username']
			return_object["password"] = request.json['password']
			return_object["task"] = "DeleteAccount"
			return return_object
		elif path_values[0] == "users" and path_values[2] == "messages" and request.method == "GET":
			return_object["username"] = path_values[1]
			return_object["password"] = request.json["password"]
			return_object["task"] = "GetMessages"
			return return_object
		elif path_values[0] == "users" and path_values[2] == "messages" and request.method == "POST":
			return_object["username"] = path_values[1]
			return_object["password"] = request.json["password"]
			return_object["message"] = request.json["message"]
			return_object["targetgroup"] = request.json["targetgroup"]
			return_object["task"] = "SendMessage"
			return return_object
		elif path_values[0] == "groups" and path_values[1] == "list":
			return_object["username"] = request.json["username"]
			return_object["password"] = request.json["password"]
			return_object["task"] = "GetGroups"
			return return_object
		elif path_values[0] == "groups" and path_values[1] == "create":
			return_object["username"] = request.json["username"]
			return_object["password"] = request.json["password"]
			return_object["groupname"] = request.json["groupname"]
			return_object["groupusers"] = request.json["groupusers"]
			return_object["task"] = "CreateGroup"
			return return_object
		else:
			return_object["task"] = "INVALID"
		return return_object
