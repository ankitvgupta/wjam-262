class RequestProcessor:

    def __init__(self):
      # userId -> user object
      self.users    = {}
      # groupId -> list of userIds
      self.groups   = {}
      # userId -> pending messages
      self.messages = {}

    def register_user(self, request_object):
        if len(self.users) == 0:
          next_id = 0
        else:
          next_id = max(self.users) + 1
        self.users[next_id] = { "username" : request_object["username"], "password" : request_object["password"] }
        return { "success" : True, "response" : None }

    def list_accounts(self, request_object):
        response = {}
        for user_id in self.users:
          response[user_id] = self.users["username"]
        return { "success" : True, "response" : response }

    def create_group(self, request_object):
        if len(self.groups) == 0:
          next_id = 0
        else:
          next_id = max(self.groups) + 1
        self.groups[next_id] = { "name" : request_object["name"], "users" : request_object["users"] }
        return { "success" : True, "response" : None }

    def list_groups(self, request_object):
        return { "success" : True, "response" : self.groups }

    def send_message(self, request_object):
        pass

    def get_messages(self, request_object):
        pass

    def delete_account(self, request_object):
        user_id = request_object['user_id']
        if user_id not in self.users:
          return { "success" : False, "response" : "User does not exist." }

        del self.users[user_id]
        return { "success" : True, "response" : None }
