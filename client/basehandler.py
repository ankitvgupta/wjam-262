import sys

class BaseHandler:
    """
    Abstract client input handler that all communications protocols should extend. 
    A client handler is responsible for converting standardized user input into a specified 
    communications protocol. It will loop waiting for user input in the command line.
    
    To debug this file, use:
        import logging
        try:
            import http.client as http_client
        except ImportError:
            # Python 2
            import httplib as http_client
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig() 
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
    """
    
    def __init__(self, username, password):
        """
        Initialize the handler, stores the username and password in plain-text in ram
        
        :param username: the username of the chatter
        :param password: the password of the chatter
        """
        self.username = username
        self.password = password
    
    def print_usage(self):
        """
        Prints the usage for the user; used on error
        
        :return: None
        """
        print """Commands:
                    list (users|groups) [SEARCH_TEXT]
                    send GROUPNAME MESSAGE
                    get
                    group GROUPNAME USERNAME1 USERNAME2 ...
                    delete
                    exit"""

    def get_command(self):
        """
        Loops on the command line for user input, checks validity of user input,
        and calls the relevant function commanded in the 
        communications protocol (implemented by sub-classes).
        
        Possible commands are listed above in print_usage function
        
        :return: None
        """
        while True:
            command = raw_input("Enter command: ")
            args = command.split(' ')
            
            if args[0] == 'register':
                self.register()
                
            elif args[0] == 'list':
                
                # checks for the variable length user-inputs as search-text
                if len(args) == 2:
                    search_text = None
                elif len(args) == 3:
                    search_text = args[2]
                else:
                    self.print_usage()
                    continue

                # kick-off to sub-class implementation
                if args[1] == 'users':
                    self.list_users(search_text)
                elif args[1] == 'groups':
                    self.list_groups(search_text)
                else:
                    self.print_usage()
                    
            elif args[0] == 'get':
                self.get()
                
            elif args[0] == 'send':
                if len(args) < 3:
                    self.print_usage()
                    continue
                self.send_group(args[1], " ".join(args[2:]))
                
            elif args[0] == 'group':
                if len(args) < 3:
                    self.print_usage()
                    continue
                self.group(args[1], args[2:])
                
            elif args[0] == 'delete':
                self.delete()
                print "Thanks for messaging!"
                sys.exit()
                
            elif args[0] == 'exit':
                print "Thanks for messaging!"
                sys.exit()
                
            else:
                # error
                self.print_usage()
    
    # The following functions should be overwritten by sub-classes. To see what
    # each function is meant to do, read the Design Documentation for the meaning
    # of each action.
    """ Register a user """
    def register(self):
        pass
    """ List users that match the wildcard "text" """
    def list_users(self, text):
        pass
    """ List groups that match the wildcard "text" """
    def list_groups(self, text):
        pass
    """ Get all messages to the current user """
    def get(self):
        pass
    """ Send "message" to "username" - 'username' can be a groupname or username"""
    def send_group(self, username, message):
        pass
    """ Create a group called "groupanme" with "usernames" in it """
    def group(self, groupname, usernames):
        pass
    """ Delete the current user (and log out). """
    def delete(self):
        pass
