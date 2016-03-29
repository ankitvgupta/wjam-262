import io
import binascii
import struct
import pdb

"""
WireProtocolStub

This class represents the processor which will take in binary data over
the wire (from a binary http field) and parse it out into a dictionary,
with the appropritate fields filled in. The relevant fields are
-username: the username of the user
-password: their password (everyone must have these two fields for requests
 		to be authenticated)
-task: what operation is to be performed by the server
-matchstring: a string to be matched, e.g. for listing groups
-message: the message to be sent to another user
-groupname: the name of a group to create or send a message to
"""
class WireProtocolStub:
    def __init__(self):
        pass

    # Takes in a string representation of http binary field, and the path
    # it came from.
    def decode(self, path, request):
        bytes = request.data
        
        """
        Byte layouts for the below functions:
		Every single request includes a four byte version number as the
		first four bytes (as we are currently on version 0, the version numbers
		are currently always 0). The fifth byte is a command number: 0
		corresponds to registering a new user, 1 to listing accounts, 2 to
		creating a group, 3 to listing a group, 4 to sending a message, 5 to
		getting all of the messages that have been sent to a particular user, 6
		to deleting an account. Every single request is authenticated — that is,
		after the command number, every request then incorporates four bytes for
		the length of the username of the user sending the request, the username
		of that user, the length of that user’s password, and the password
		itself. The unique data in each request, which immediately follows the
		data described above, is organized as follows:
		Register
			No extra information is needed beyond the username and password.
		List accounts
			The next four bytes are the length of the string to be matched,
			followed by this string itself.
		Create group
			The next four bytes are the number of users to be added to the
			group. The next four bytes are the length of the name of the group
			to be created, followed by that name itself. This is followed by the
			length of the first username to be added to the group, that
			username, the length of the second username, that username, etc.
		List groups
			This is simply going to list the groups to which the current user
			belongs, so we do not need any more information.
		Send message
			The next four bytes are the length of the name of the user or group
			for the message to be sent to, that name, four bytes representing
			the length of the message, and finally the message itself.
		Get messages
			Again, we are just getting the messages which have been sent to a
			particular user, so we do not need any extra information.
		Delete account
			Again, no extra information needed.
		"""
        version = struct.unpack("<i",bytes[0:4])[0]
        command_type = struct.unpack("<B", bytes[4])[0]

        ret_obj = {}        

        def get_user_pwd(bytes, ret_obj):
            vtype_start = 4
            usernamelen = struct.unpack("<i", bytes[vtype_start + 1:vtype_start + 5])[0]
            username = bytes[vtype_start + 5:(vtype_start + 5 + usernamelen)]
            passwordlen = struct.unpack("<i", bytes[vtype_start + 5 + usernamelen : vtype_start + 5 + usernamelen + 4])[0]
            password = bytes[vtype_start + 5 + usernamelen + 4 : vtype_start + 5 + usernamelen + 4 + passwordlen]
            start = vtype_start + 5 + usernamelen + 4 + passwordlen
            ret_obj["username"] = username
            ret_obj["password"] = password
            return username, password, start

        if command_type == 0:
            # Register command
            user, pwd, st = get_user_pwd(bytes, ret_obj)
            ret_obj["task"] = "CreateUser"
            return ret_obj

        elif command_type == 1:
            # List accounts command
            user, pwd, st = get_user_pwd(bytes, ret_obj)
            matchstringlen = struct.unpack("<i", bytes[st:st+4])[0]

            matchstring = bytes[4 + st:4 + matchstringlen + st]
            ret_obj["task"] = "ListAccounts"
            ret_obj["matchstring"] = matchstring
            return ret_obj

        elif command_type == 2:
            # Create group command
            user, pwd, st = get_user_pwd(bytes, ret_obj)
            num_users = struct.unpack("<i", bytes[st: st + 4])[0]
            groupnamelen = struct.unpack("<i", bytes[st + 4: st + 8])[0]
            groupname = bytes[st + 8:st + 8 + groupnamelen]
            ret_obj["name"] = groupname
            init = st + 4 + 4 + groupnamelen
            for i in range(num_users):
                tmpuserlen = struct.unpack("<i", bytes[init:init+4])[0]
                tmpusern = bytes[init+4:init+4+tmpuserlen]
                init += 4 + tmpuserlen
                if i == 0:
                    ret_obj["users"] = [tmpusern]
                else:
                    ret_obj["users"].append(tmpusern)
            ret_obj["task"] = "CreateGroup"
            return ret_obj

        elif command_type == 3:
            # List groups command
            user, pwd, st = get_user_pwd(bytes,ret_obj)
            matchstringlen = struct.unpack("<i", bytes[st:st+4])[0]

            matchstring = bytes[4 + st:4 + matchstringlen + st]
            ret_obj["task"] = "GetGroups"
            ret_obj["matchstring"] = matchstring
            return ret_obj

        elif command_type == 4:
            # Send_message command
            user, pwd, st = get_user_pwd(bytes,ret_obj)   
            namelen = struct.unpack("<i", bytes[st+1:st+5])[0]
            name = bytes[st+5:st+ 5 + namelen]
            name_end = st + 5 + namelen
            msglen = struct.unpack("<i", bytes[name_end:name_end + 4])[0]
            msg = bytes[name_end + 4:name_end + msglen + 4]
            ret_obj["message"] = msg
            ret_obj["groupname"] = name
            ret_obj["task"] = "SendMessage"
            return ret_obj

        elif command_type == 5:
            # Get messages command
            user, pwd, st = get_user_pwd(bytes,ret_obj)
            ret_obj["task"] = "GetMessages"
            return ret_obj

        elif command_type == 6:
            # Delete account command
            user, pwd, st = get_user_pwd(bytes,ret_obj)
            ret_obj["task"] = "DeleteAccount"
            return ret_obj

        else:
        	# The data was not recognized as one of our types,
        	# return an error.
            ret_obj["task"] = "INVALID"
            return ret_obj

    # Encode the response, which is always just the response field, as:
    # 4 bytes for 0 or 1, 0 if success, 1 if failure, the length of the
    # response as a 4 byte integer, and then the bytes of the response itself.
    def encode(self, response):
        s = response["success"]
        resp = str(response["response"])
        # 0 if operation success, 1 if failure.
        i = 0 if s else 1
        resplen = len(resp)
        output = ""
        output += struct.pack("<i", s)
        output += struct.pack("<i", resplen)
        output += resp
        return output
