from BaseHandler import BaseHandler
import struct
import requests

REQUEST_URL = 'https://wjam-262.herokuapp.com'
def sendRequest(command_type):
    def wrap(f):
        def wrapped_f(*args):
            data = bytearray([command_type]) + f(*args)
            print requests.post(REQUEST_URL, data=data).text
        return wrapped_f
    return wrap

# defined per the design https://docs.google.com/document/d/1gF_5esZ2cq-pECmQuPqit8FXHTf76Y9pqLyGkCfK5Rc/edit
class WireHandler(BaseHandler):

    # returns 4 bytes: length of username; length bytes: username
    def username_bytes(self):
        return struct.pack("I", len(self.username)) + bytearray(self.username)

    @sendRequest(0)
    def register(self):
        return self.username_bytes()
        + struct.pack("I", len(self.password))
        + bytearray(password)
        
    @sendRequest(1)
    def list_users(self, text):
        return struct.pack("I", len(text))
        + bytearray(text)

    def list_groups(self, text):
        # TODO
        pass
    def group(self, usernames):
        # TODO
        pass

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
        return bytearray([1]) if is_group else bytearray([0])
        + struct.pack("I", len(name))
        + bytearray(name)
        + struct.pack("I", len(message))
        + bytearray(message)
    
    @sendRequest(6)
    def delete(self):
        return self.username_bytes()
