class RequestProcessor:

    def __init__(self):
        # userId -> user object
        self.users    = {}
        # groupId -> list of userIds
        self.groups   = {}
        # userId -> pending messages
        self.messages = {}

    def get_next_id(self, dictionary):
        if len(dictionary) == 0:
            return 0
        return max(dictionary) + 1

    def register_user(self, request_object):
        next_user_id                = self.get_next_id(self.users)
        self.users[next_user_id]    = { "username" : request_object["username"], "password" : request_object["password"] }
        next_group_id               = self.get_next_id(self.groups)
        self.groups[next_group_id]  = { "name" : request_object["username"], "users" : [next_user_id] }
        self.messages[next_user_id] = []
        return { "success" : True, "response" : None }

    def list_accounts(self, request_object):
        response = {}
        for user_id in self.users:
            response[user_id] = self.users[user_id]["username"]
        return { "success" : True, "response" : response }

    def create_group(self, request_object):
        next_id = self.get_next_id(self.groups)
        self.groups[next_id] = { "name" : request_object["name"], "users" : request_object["users"] }
        return { "success" : True, "response" : None }

    def list_groups(self, request_object):
        return { "success" : True, "response" : self.groups }

    def send_message(self, request_object):
        group_id = request_object["group_id"]
        if group_id not in self.groups:
            return { "success" : False, "response" : "Group ID does not exist." }

        for user_id in self.groups[group_id]['users']:
            self.messages[user_id].append(request_object['message'])

    def get_messages(self, request_object):
        user_id  = request_object['user_id']

        if user_id not in self.messages:
            return { "success" : False, "response" : "User ID does not exist." }

        messages = self.messages[user_id]
        self.messages[user_id] = []
        return { "success" : True, "response" : messages }

    def delete_account(self, request_object):
        user_id = request_object['user_id']
        if user_id not in self.users:
            return { "success" : False, "response" : "User does not exist." }

        del self.users[user_id]

        empty_groups = []
        for group_id in self.groups:
            if user_id in self.groups[group_id]['users']:
                self.groups[group_id]['users'].remove(user_id)
                if len(self.groups[group_id]['users']) == 0:
                    empty_groups.append(group_id)

        for group_id in empty_groups:
            del self.groups[group_id]

        del self.messages[user_id]

        return { "success" : True, "response" : None }
