from basehandler import BaseHandler
import requests
import json

# Base URL to request
REQUEST_URL = 'https://obscure-caverns-54504.herokuapp.com'
# Version number of the protocol, increment upon change
version = 0

def sendRequest(path, method):
    """ 
    A decorator to wrap requests sent to the server. Because not every URL
    is static in a Restful API (for instance sending a message to a new user 
    requires the username of the receiver to be in the URL), this method is
    NOT wrapping EVERY send.
    
    Used by the @sendRequest(path, method) construct in python
    
    :param path: the path of the url for the request (nouns)
    :param mathod: the method of the request (verb)
    
    :return: a high-level function that is used as a decoratar by the python API
    """
    def wrap(f):
        def wrapped_f(*args):
            data = f(*args)
            print requests.request(method, REQUEST_URL + path, data=json.dumps(data)).text
        return wrapped_f                            
    return wrap

class RestHandler(BaseHandler):
    """
    A client handler which converts input into a Restful API implementation. See
    design documentation for specific protocol definitions
    """

    def req_dict(self, append_dict={}):
        """
        Helper function to construct the request payload of the Rest API. Every valid
        REST API payload must have a username and a password to authenticate the user. 
        
        Functions should use req_dict(append_dict) rather than raw dictionaries in the payload.
        
        :param append_dict: the actual payload outside of authentication
        :return: a dictionary of username, password and the append_dict
        """
        ret = { 'username': self.username, 'password': self.password }
        for key in append_dict:
            ret[key] = append_dict[key]
        return ret

    def list_generic(self, text):
        extra_add = { 'matchstring': "" if text == None else text }
        return self.req_dict(extra_add)
        
    def send_generic(self, name, message, is_group):
        print requests.post(REQUEST_URL + '/users/' + name + '/messages', data=json.dumps(self.req_dict({ 'message': message }))).text

    # The following functions overwrite basehandler and make a request to the
    # server.
    @sendRequest('/users', 'POST')
    def register(self):
        return self.req_dict()
        
    @sendRequest('/users', 'GET')
    def list_users(self, text):
        return self.list_generic(text)

    @sendRequest('/groups', 'GET')
    def list_groups(self, text):
        return self.list_generic(text)
        
    @sendRequest('/groups', 'POST')        
    def group(self, groupname, usernames):
        return self.req_dict({
            'groupname': groupname,
            'groupusers': usernames })

    def get(self):
        print requests.get(REQUEST_URL + '/users/' + self.username + '/messages', data=json.dumps(self.req_dict())).text

    def send_user(self, username, message):
        return self.send_generic(username, message, False)
    
    def send_group(self, groupname, message):
        return self.send_generic(groupname, message, True)
    
    @sendRequest('/users', 'DELETE')
    def delete(self):
        return self.req_dict()
