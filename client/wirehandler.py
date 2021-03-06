from basehandler import BaseHandler
import struct
import requests

# Base URL to request - this should match the location where the server is deployed.
REQUEST_URL = 'https://obscure-caverns-54504.herokuapp.com'
version = 0

def sendRequest(command_type):
    """ 
    A decorator to wrap requests sent to the server. Used by the @sendRequest(command_type) construct in python
    
    :param command_type: the command type (0-6) as defined in the design documentation
        0 corresponds to registering a new user, 
        1 to listing accounts, 
        2 to creating a group, 
        3 to listing a group, 
        4 to sending a message, 
        5 to getting all messages, 
        6 to deleting an account
    :return: a high-level function that is used as a decoratar by the python API
    """
    def wrap(f):
        def wrapped_f(*args):
            data = struct.pack("I", version) + bytearray([command_type]) + f(*args)
            print requests.post(REQUEST_URL, data=data).text
        return wrapped_f
    return wrap

class WireHandler(BaseHandler):
    """
    A client handler which converts input into a Wire API implementation. See
    design documentation for specific protocol definitions
    """
    
    def username_bytes(self):
        """
        Helper function for authentication. This should be appended to any
        set of bytes in the request that requires a username / password pair
        
        :return: ByteArray of [username length, username, password length, password]
        """
        return (struct.pack("I", len(self.username)) 
            + bytearray(self.username) 
            + struct.pack("I", len(self.password)) 
            + bytearray(self.password))

    def send_generic(self, name, message, is_group):
        """
        Helper function for sending messages. This can be used to send a message to
        either a group or user.
        :param name, the name of the user/group sending to
        :param message, the message being sent
        :param is_group, a boolean indicating whether it's a user or group being sent to.
        
        """
        return (self.username_bytes()
        + (bytearray([1]) if is_group else bytearray([0]))
        + struct.pack("I", len(name))
        + bytearray(name)
        + struct.pack("I", len(message))
        + bytearray(message))

    # The following functions overwrite the abstract functions in BaseHandler. See
    # basehandler for detailed function documentation.
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
    
    @sendRequest(6)
    def delete(self):
        return self.username_bytes()
