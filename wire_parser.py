import io
import binascii
import struct

# Takes in a string representation of http binary field
def bytestream_to_request(b):
    type = struct.unpack("<B", b[0])[0]
    if type == 0:
        usernamelen = struct.unpack("<i", b[1:5])
        username = b[5:5 + usernamelen]
        passwordlen = struct.unpack("<i", b[5 + usernamelen : 5 + usernamelen + 4])
        password = b[5 + usernamelen + 4 : 5 + usernamelen + 4 + passwordlen]
    elif type == 1:
        print "here"
        matchstringlen = struct.unpack("<i", b[1:5])[0]
        matchstring = b[5:5 + matchstringlen]
        print matchstringlen, matchstring
    elif type == 2:
        pass
    elif type == 3:
        pass
    elif type == 4:
        pass
    elif type == 5:
        pass
    elif type == 6:
        pass

f = open("output")

s = f.read()
bytestream_to_request(s)
