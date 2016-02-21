#!/usr/bin/python
import sys
from WireHandler import WireHandler
from RestHandler import RestHandler

def print_cmd_line_usage():
    print "USAGE: ./client.py (REST|WIRE) [REGISTER] username password"
    sys.exit()

def check_usage():
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print_cmd_line_usage()
    
    if sys.argv[1] != 'REST' and sys.argv[1] != 'WIRE':
        print_cmd_line_usage()
    
    # only scenario when there are 5 arguments is when we're registering a new account
    if len(sys.argv) == 5 and sys.argv[2] != 'REGISTER':
        print_cmd_line_usage()

if __name__ == '__main__':
    check_usage()
    
    if len(sys.argv) == 5:
        username = sys.argv[3]
        password = sys.argv[4]
    else:
        username = sys.argv[2]
        password = sys.argv[3]
    
    if sys.argv[1] == 'REST':
        handler = RestHandler(username, password)
    elif sys.argv[1] == 'WIRE':
        handler = WireHandler(username, password)

    if len(sys.argv) == 5:
        handler.register()
    
    handler.get_command()
    