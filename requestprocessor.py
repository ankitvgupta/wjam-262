import pdb

class RequestProcessor:

    def __init__(self):
        # userId -> user object
        self.users      = {}
        # groupId -> name, list of userIds
        self.groups     = {}
        # userId -> pending messages
        self.messages   = {}
        # for constant time reference
        self.groupNames = {}
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

    def register_user(self, request_object):
        if request_object["username"] in self.groupNames:
            return { "success" : False, "response" : "Username is already taken." }

        next_user_id                = self.get_next_id(self.users)
        self.users[next_user_id]    = { "username" : request_object["username"], "password" : request_object["password"] }
        self.usernames[request_object["username"]] = next_user_id
        next_group_id               = self.get_next_id(self.groups)
        self.groups[next_group_id]  = { "name" : request_object["username"], "users" : [next_user_id] }
        self.groupNames[request_object["username"]] = next_group_id
        self.messages[next_user_id] = []
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
        self.groups[next_id] = { "name" : request_object["name"], "users" : request_object["users"] }
        self.groupNames[request_object["name"]] = next_id
        return { "success" : True, "response" : None }

    def list_groups(self, request_object):
        response = self.groups

        if "matchstring" in request_object:
            response = dict((k, v) for k, v in self.groups.items() if self.is_matching(request_object["matchstring"], v["name"]))

        return { "success" : True, "response" : response }

    # TODO Stub and Client uses names and not ids
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

    # TODO Stub and Client uses names and not ids
    def get_messages(self, request_object):
        validation = self.validate_user(request_object)
        if not validation["success"]:
            return validation

        user_id = self.usernames[request_object["username"]]

        messages = self.messages[user_id]
        self.messages[user_id] = []
        return { "success" : True, "response" : messages }

    # TODO Stub and Client uses names and not ids
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
