from BaseHandler import BaseHandler
import requests

REQUEST_URL = 'https://wjam-262.herokuapp.com'
# REQUEST_URL = 'http://0.0.0.0:8080'

def sendRequest(path, method):
    def wrap(f):
        def wrapped_f(*args):
            print REQUEST_URL + path
            print requests.request(method, REQUEST_URL + path, data=f(*args)).text
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
        print requests.get('/users/' + self.username + '/messages', data=self.req_dict()).text

    def send_user(self, username, message):
        return self.send_generic(username, message, False)
    
    def send_group(self, groupname, message):
        return self.send_generic(groupname, message, True)
    
    def send_generic(self, name, message, is_group):
        print requests.post('/users/' + name + '/messages', data=self.req_dict({ 'message': message })).text
    
    @sendRequest('/users', 'DELETE')
    def delete(self):
        return self.req_dict()
