import json
import pdb
import flask

"""
This class implements the RestAPI encoder and decoder. 

The encoder is used to transfer information from the server
back to the user in a consistent format. Since we are displaying information
to the user in a simple JSON-like notation, this requires a simple jsonify call
on the server's return object.

The decoder is the more critical piece here, as it allows us to convert the request
object that is specific to REST into a custom internal request object. The format of this
internal request object is shared between the various transfer protocol implementations
(REST/WireProtocol), and thus we can add more such protocols in the future by adding 
another stub implementation, like this one.
"""
class RestAPIStub:
	def __init__(self):
		pass

	""" 
	An encoder for requests from the server that are going to the user.
	Since requests are being receives as dictionaries, we can encode them for
	sending back to the user as a JSON string. Thus, we simply call
	jsonify.

	:param ret: The information to be returned to the user.
	Ret must be a Python dictionary that can be jsonified into a string.
	No assumptions otherwise.

	:return A jsonified dictionary with the information needed to return to the user. 
	"""
	def encode(self, ret):
		return flask.jsonify(ret)
    """ 
    A decoder for requests from the user. This function converts the 
    request that the user makes from the REST format to a consistent 
    internal dictionary. This is critical, because the internal format
    is shared between the RestAPI and the WireProtocolAPI, and so after that
    object is made, the backend does not need to have behavior specific
    to a particular protocol.
        
    :param path: the path of the url for the request (nouns)
    :param request: the JSON request object
    
    Valid values for the path argument are:
    	For GET, they were allowed to request
			../users, to get a list of all of the users
			../users/<USERNAME>/messages, to get all of the messages for <USERNAME>
			../groups/, to get a list of all groups
		For POST, they were allowed to request
			../users, to create a new user
			../users/<USERNAME>/messages, to send a message to <USERNAME>
			../groups, to create a group
		For DELETE, they were allowed to request
			../users, to delete a user
		Anything else will return INVALID.
	The request argument must have the following fields:
		method [POST/GET/DELETE]
		data:
			username
			password
			matchstring (for getting users and groups only)
			groupname (for making group)
			groupusers [list of user IDS in group] (for making group only)
			message (for sending a message)
    :return: a request dictionary which has the same format as the one returned by WireProtocolStub.py
    """
	def decode(self, path, request):
		path_values = path.split("/")
		target = path_values[0]
		return_object = {}
		request_json = json.loads(request.data)
		return_object["username"] = request_json['username']
		return_object["password"] = request_json['password']
		assert(request_json)
		if path_values[0] == "users" and request.method == "GET" and len(path_values) == 1:
			return_object["task"] = "ListAccounts"
			return_object["matchstring"] = request_json["matchstring"]
			return return_object
		elif path_values[0] == "users" and request.method == "DELETE" and len(path_values) == 1:
			return_object["task"] = "DeleteAccount"
			return return_object
		elif path_values[0] == "users" and request.method == "POST" and len(path_values) == 1:
			return_object["task"] = "CreateUser"
			return return_object
		elif path_values[0] == "groups" and request.method == "GET" and len(path_values) == 1:
			return_object["task"] = "GetGroups"
			return_object["matchstring"] = request_json["matchstring"]
			return return_object
		elif path_values[0] == "groups" and request.method == "POST" and len(path_values) == 1:
			return_object["name"] = request_json["groupname"]
			return_object["users"] = request_json["groupusers"]
			return_object["task"] = "CreateGroup"
			return return_object
		elif path_values[0] == "users" and path_values[2] == "messages" and request.method == "GET":
			return_object["task"] = "GetMessages"
			return return_object
		elif path_values[0] == "users" and path_values[2] == "messages" and request.method == "POST":
			return_object["message"] = request_json["message"]
			return_object["groupname"] = path_values[1]
			return_object["task"] = "SendMessage"
			return return_object
		else:
			return_object["task"] = "INVALID"
		return return_object
