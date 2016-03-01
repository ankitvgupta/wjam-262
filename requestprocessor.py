import pdb

class RequestProcessor:

    def __init__(self):
        # userId -> user object
        self.users      = {}
        # groupId -> name, list of userIds
        self.groups     = { 0 : { "name" : "all", "users" : [] } }
        # userId -> pending messages
        self.messages   = {}
        # for constant time reference
        self.groupNames = { "all" : 0 }
        # for username -> userId
        self.usernames  = {}

    def get_next_id(self, dictionary):
        if len(dictionary) == 0:
            return 0
        return max(dictionary) + 1

    def is_matching(self, matchstring, string):
        if '*' not in matchstring:
            return matchstring == string

        before_star = matchstring.split('*')[0]
        return string[:len(before_star)] == before_star

    def validate_user(self, request_object):
        username = request_object["username"]
        if username not in self.usernames:
            return { "success" : False, "response" : "User does not exist." }

        user_id = self.usernames[username]
        if self.users[user_id]["password"] != request_object["password"]:
            return { "success" : False, "response" : "Invalid password." }

        return { "success" : True, "response" : "Success!" }

    def add_user_to_group(self, username, groupname):
        group_id = self.groupNames[groupname]
        user_id  = self.usernames[username]

        if user_id not in self.groups[group_id]["users"]:
            self.groups[group_id]["users"].append(user_id)

    def register_user(self, request_object):
        if request_object["username"] in self.groupNames:
            return { "success" : False, "response" : "Username is already taken." }

        username                    = request_object["username"]
        # Initialize the user
        next_user_id                = self.get_next_id(self.users)
        self.users[next_user_id]    = { "username" : username, "password" : request_object["password"] }
        self.usernames[username]    = next_user_id
        # Initialize the group for the user
        next_group_id               = self.get_next_id(self.groups)
        self.groups[next_group_id]  = { "name" : username, "users" : [next_user_id] }
        self.groupNames[username]   = next_group_id
        # Initialize the messages for the user
        self.messages[next_user_id] = []
        # Add the user to the 'all' group
        self.add_user_to_group(username, "all")
        return { "success" : True, "response" : None }

    def list_accounts(self, request_object):
        response       = {}
        relevant_users = self.users

        if "matchstring" in request_object and request_object["matchstring"]:
            relevant_users = dict((k, v) for k, v in self.users.items() if self.is_matching(request_object["matchstring"], v["username"]))

        for user_id in relevant_users:
            response[user_id] = relevant_users[user_id]["username"]

        return { "success" : True, "response" : response }

    def create_group(self, request_object):
        if request_object["name"] in self.groupNames:
            return { "success" : False, "response" : "Group name is already taken." }

        next_id = self.get_next_id(self.groups)

        users = []
        for user in request_object["users"]:
            if user not in self.usernames:
                return { "success" : False, "response" : "One or more users don't exist." }
            else:
                users.append(self.usernames[user])

        self.groups[next_id] = { "name" : request_object["name"], "users" : users }
        self.groupNames[request_object["name"]] = next_id
        return { "success" : True, "response" : None }

    def list_groups(self, request_object):
        relevant_groups = dict((k, v) for k, v in self.groups.items() if len(v["users"]) != 1 or self.users[v["users"][0]]["username"] != v["name"])

        if "matchstring" in request_object:
            relevant_groups = dict((k, v) for k, v in relevant_groups.items() if self.is_matching(request_object["matchstring"], v["name"]))

        response = {}
        for group_id in relevant_groups:
            response[group_id] = { "name" : relevant_groups[group_id]["name"], "users" : map(lambda user_id : self.users[user_id]["username"], relevant_groups[group_id]["users"]) }

        return { "success" : True, "response" : response }

    def send_message(self, request_object):
        validation = self.validate_user(request_object)
        if not validation["success"]:
            return validation

        group_name = request_object["groupname"]

        if group_name not in self.groupNames:
            return { "success" : False, "response" : "Group does not exist." }

        group_id = self.groupNames[group_name]

        for user_id in self.groups[group_id]['users']:
            self.messages[user_id].append('%s: %s' % (request_object["username"], request_object["message"]))

        return { "success" : True, "response" : "Message sent." }

    def get_messages(self, request_object):
        validation = self.validate_user(request_object)
        if not validation["success"]:
            return validation

        user_id = self.usernames[request_object["username"]]

        messages = self.messages[user_id]
        self.messages[user_id] = []
        return { "success" : True, "response" : messages }

    def delete_account(self, request_object):
        validation = self.validate_user(request_object)
        if not validation["success"]:
            return validation

        username = request_object["username"]
        user_id  = self.usernames[username]

        del self.users[user_id]
        del self.usernames[username]

        empty_groups = []
        for group_id in self.groups:
            if user_id in self.groups[group_id]['users']:
                self.groups[group_id]['users'].remove(user_id)
                if len(self.groups[group_id]['users']) == 0:
                    empty_groups.append(group_id)

        for group_id in empty_groups:
            del self.groupNames[self.groups[group_id]["name"]]
            del self.groups[group_id]

        del self.messages[user_id]

        return { "success" : True, "response" : None }
