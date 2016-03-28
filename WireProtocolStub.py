import io
import binascii
import struct
import pdb

# This class represents the processor which will take in binary data over
# the wire (from a binary http field) and parse it out into a dictionary,
# with the appropritate fields filled in. The relevant fields are
class WireProtocolStub:
    def __init__(self):
        pass

    # Takes in a string representation of http binary field
    def decode(self, path, request):
        bytes = request.data
        
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
            # register
            user, pwd, st = get_user_pwd(bytes, ret_obj)
            ret_obj["task"] = "CreateUser"
            return ret_obj

        elif command_type == 1:
            # list accounts
            user, pwd, st = get_user_pwd(bytes, ret_obj)
            matchstringlen = struct.unpack("<i", bytes[st:st+4])[0]

            matchstring = bytes[4 + st:4 + matchstringlen + st]
            ret_obj["task"] = "ListAccounts"
            ret_obj["matchstring"] = matchstring
            return ret_obj

        elif command_type == 2:
            # create group
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
            # list groups
            user, pwd, st = get_user_pwd(bytes,ret_obj)
            matchstringlen = struct.unpack("<i", bytes[st:st+4])[0]

            matchstring = bytes[4 + st:4 + matchstringlen + st]
            # that's all the info we need
            ret_obj["task"] = "GetGroups"
            ret_obj["matchstring"] = matchstring
            return ret_obj

        elif command_type == 4:
            # send_message
            user, pwd, st = get_user_pwd(bytes,ret_obj)   
            #usr_or_group = struct.unpack("<i", bytes[st : st + 1])
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
            #get messages
            user, pwd, st = get_user_pwd(bytes,ret_obj)
            # that's all we need
            ret_obj["task"] = "GetMessages"
            return ret_obj

        elif command_type == 6:
            # delete account
            user, pwd, st = get_user_pwd(bytes,ret_obj)
            # that's all we need
            ret_obj["task"] = "DeleteAccount"
            return ret_obj

        else:
            ret_obj["task"] = "INVALID"
            return ret_obj

    def encode(self, response):
        s = response["success"]
        resp = str(response["response"])
        # 0 if success, 1 if failure
        i = 0 if s else 1
        resplen = len(resp)
        output = ""
        output += struct.pack("<i", s)
        output += struct.pack("<i", resplen)
        output += resp
        return output


# Run on the output of check.c
# def test():
#     f = open("output")
#     s = f.read()
#     bytestream_to_request(s)
