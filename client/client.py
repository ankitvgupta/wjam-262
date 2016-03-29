"""
client.py
This is the main driver program for the client. To instantiate the client, the user
should indicate whether the REST protocol or WireProtocol is desired, along with the
username and password. If this is a new user, adding the word "register" will create the 
new user. See the below usage for the format.

Here is the correct usage:
USAGE: ./client.py (rest|wire) [register] USERNAME PASSWORD


This file connects the appropriate handler (RestHandler or WireHandler) in order to 
do the appropriate information transfer to the server. Prior to running this client,
the server should be running already.
"""
#!/usr/bin/python

import sys
from wirehandler import WireHandler
from resthandler import RestHandler

def print_cmd_line_usage():
    """
    Prints usage error. activated when the user inputs a bad command line argument. Exits program upon completion.
    
    :return: None
    """
    print "USAGE: ./client.py (rest|wire) [register] USERNAME PASSWORD"
    sys.exit()

def check_usage():
    """
    Checks for usage errors
    
    :return: None
    """
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print_cmd_line_usage()
    
    if sys.argv[1] != 'rest' and sys.argv[1] != 'wire':
        print_cmd_line_usage()
    
    # only case when there are 5 arguments is when we're registering a new account
    if len(sys.argv) == 5 and sys.argv[2] != 'register':
        print_cmd_line_usage()

if __name__ == '__main__':
    """
    The driver, checks that the user input is valid, then instantiates a client handler 
    with the specified communication protocol.
    """
    check_usage()
    
    # if registering a new user
    if len(sys.argv) == 5:
        username = sys.argv[3]
        password = sys.argv[4]
    else:
        username = sys.argv[2]
        password = sys.argv[3]
    
    if sys.argv[1] == 'rest':
        handler = RestHandler(username, password)
    elif sys.argv[1] == 'wire':
        handler = WireHandler(username, password)

    # if registering a new user, we must call for it here
    if len(sys.argv) == 5:
        handler.register()

    # ready to receive instructions
    handler.get_command()
    
