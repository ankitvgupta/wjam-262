import sys

class BaseHandler:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def print_usage(self):
        print """Commands:
                    list (users|groups) [search_text]
                    send (user|group) (username|groupname) message
                    get
                    group username1 username2 ...
                    delete
                    exit"""

    def get_command(self):
        while True:
            command = raw_input("Enter command: ")
            args = command.split(' ')
            
            if args[0] == 'list':
                if len(args) == 2:
                    search_text = None
                elif len(args) == 3:
                    search_text = args[2]
                else:
                    self.print_usage()
                    continue

                if args[1] == 'users':
                    self.list_users(search_text)
                elif args[1] == 'groups':
                    self.list_groups(search_text)
                else:
                    self.print_usage()
                    
            elif args[0] == 'get':
                self.get()
                
            elif args[0] == 'send':
                if len(args) < 4:
                    self.print_usage()
                    continue
                if args[1] == 'user':
                    self.send_user(args[2], " ".join(args[3:]))
                elif args[1] == 'group':
                    self.send_group(args[2], " ".join(args[3:]))
                else:
                    self.print_usage()
                    continue
                
            elif args[0] == 'group':
                if len(args) < 2:
                    self.print_usage()
                    continue
                self.group(args[1:])
                
            elif args[0] == 'delete':
                self.delete()
                print "Thanks for messaging!"
                sys.exit()
                
            elif args[0] == 'exit':
                print "Thanks for messaging!"
                sys.exit()
                
            else:
                self.print_usage()
    
    def register(self):
        pass
    def list_users(self, text):
        pass
    def list_groups(self, text):
        pass
    def get(self):
        pass
    def send_user(self, username, message):
        pass
    def send_group(self, username, message):
        pass
    def group(self, usernames):
        pass
    def delete(self):
        pass
