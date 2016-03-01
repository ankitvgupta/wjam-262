from basehandler import BaseHandler
import struct
import requests
import pdb

#REQUEST_URL = 'http://wjam-262.herokuapp.com'
#REQUEST_URL = 'http://0.0.0.0:5000'
REQUEST_URL = 'https://obscure-caverns-54504.herokuapp.com'
version = 0

def sendRequest(command_type):
    def wrap(f):
        def wrapped_f(*args):
            data = struct.pack("I", version) + bytearray([command_type]) + f(*args)
            print requests.post(REQUEST_URL, data=data).text
        return wrapped_f
    return wrap

# defined per the design https://docs.google.com/document/d/1gF_5esZ2cq-pECmQuPqit8FXHTf76Y9pqLyGkCfK5Rc/edit
class WireHandler(BaseHandler):

    # returns 4 + len(username) bytes: length of username; length bytes: username
    def username_bytes(self):
        return (struct.pack("I", len(self.username)) + bytearray(self.username) + struct.pack("I", len(self.password)) + bytearray(self.password))

    @sendRequest(0)
    def register(self):
        return self.username_bytes()
        
    @sendRequest(1)
    def list_users(self, text):
        text = "" if text is None else text
        return (self.username_bytes()
        + struct.pack("I", len(text))
        + bytearray(text))

    @sendRequest(3)
    def list_groups(self, text):
        text = "" if text is None else text
        return (self.username_bytes()
        + struct.pack("I", len(text))
        + bytearray(text))

    @sendRequest(2)
    def group(self, groupname, usernames):
        ret = (self.username_bytes() 
            + struct.pack("I", len(usernames))
            + struct.pack("I", len(groupname))
            + bytearray(groupname))
            
        for username in usernames:
            ret += struct.pack("I", len(username)) + bytearray(username)

        return ret

    @sendRequest(5)    
    def get(self):
        return self.username_bytes()

    @sendRequest(4)
    def send_user(self, username, message):
        return self.send_generic(username, message, False)
    
    @sendRequest(4)
    def send_group(self, groupname, message):
        return self.send_generic(groupname, message, True)
    
    def send_generic(self, name, message, is_group):
        return (self.username_bytes()
        + (bytearray([1]) if is_group else bytearray([0]))
        + struct.pack("I", len(name))
        + bytearray(name)
        + struct.pack("I", len(message))
        + bytearray(message))
    
    @sendRequest(6)
    def delete(self):
        return self.username_bytes()
