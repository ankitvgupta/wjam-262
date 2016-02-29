#!/usr/bin/python
import sys
from wirehandler import WireHandler
from resthandler import RestHandler

def print_cmd_line_usage():
    print "USAGE: ./client.py (rest|wire) [register] USERNAME PASSWORD"
    sys.exit()

def check_usage():
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print_cmd_line_usage()
    
    if sys.argv[1] != 'rest' and sys.argv[1] != 'wire':
        print_cmd_line_usage()
    
    # only scenario when there are 5 arguments is when we're registering a new account
    if len(sys.argv) == 5 and sys.argv[2] != 'register':
        print_cmd_line_usage()

if __name__ == '__main__':
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
    
