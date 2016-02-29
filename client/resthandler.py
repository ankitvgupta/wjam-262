from basehandler import BaseHandler
import requests
import json

# import logging

# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig() 
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# REQUEST_URL = 'https://wjam-262.herokuapp.com'
REQUEST_URL = 'http://0.0.0.0:5000'

def sendRequest(path, method):
    def wrap(f):
        def wrapped_f(*args):
            data = f(*args)
            print requests.request(method, REQUEST_URL + path, data=json.dumps(data)).text
        return wrapped_f                            
    return wrap

class RestHandler(BaseHandler):

    def req_dict(self, append_dict={}):
        ret = { 'username': self.username, 'password': self.password }
        for key in append_dict:
            ret[key] = append_dict[key]
        return ret

    @sendRequest('/users', 'POST')
    def register(self):
        return self.req_dict()
        
    @sendRequest('/users', 'GET')
    def list_users(self, text):
        return self.req_dict()

    @sendRequest('/groups', 'GET')
    def list_groups(self, text):
        return self.req_dict()

    @sendRequest('/groups', 'POST')        
    def group(self, groupname, usernames):
        return self.req_dict({
            'groupname': groupname,
            'groupusers': usernames })

    def get(self):
        print requests.get(REQUEST_URL + '/users/' + self.username + '/messages', data=self.req_dict()).text

    def send_user(self, username, message):
        return self.send_generic(username, message, False)
    
    def send_group(self, groupname, message):
        return self.send_generic(groupname, message, True)
    
    def send_generic(self, name, message, is_group):
        print requests.post(REQUEST_URL + '/users/' + name + '/messages', data=self.req_dict({ 'message': message })).text
    
    @sendRequest('/users', 'DELETE')
    def delete(self):
        return self.req_dict()
