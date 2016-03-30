"""
RequestProcessor

This is the central data structure in the server backend. The server instantiates a
RequestProcessor. The main calls to the public methods in RequestProcessor
include a request_object, which is an internal dictionary-based data structure
which is transfer protocol-agnostic, meaning it works the same with both the
WireProtocol and REST API. Thus, the RequestProcessor has no knowledge of what
the transfer protocol is.

The RequestProcessor implements the main functions of the backend, such as adding users,
deleting users, creating groups, sending/receiving messages, etc.

"""
class RequestProcessor:

    def __init__(self):
        # user id -> user object
        self.users      = {}
        # group id -> name, list of user ids
        self.groups     = { 0 : { "name" : "all", "users" : [] } }
        # user id -> pending messages
        self.messages   = {}
        # group name -> group id
        self.groupNames = { "all" : 0 }
        # username -> user id
        self.usernames  = {}

    """
    Gets the next available user or group id.

    :param dictionary: This is either self.users or self.groups.

    :return the next available index.
    """
    def get_next_id(self, dictionary):
        # Return zero for an empty dictionary.
        if len(dictionary) == 0:
            return 0
        # max(dictionary) will iterate over the indices in the
        # dictionary and pick the maximum.
        return max(dictionary) + 1

    """
    Returns whether a string matches the pattern passed in by the user.
    Used in the listing of accounts and groups.

    :param matchstring: A pattern to compare the string against.
    :param string: Either a group name or a username.

    Assumptions:
    We assume that only one wildcard character '*' is permitted,
    and that it will come at the end of a string. Any characters
    after the first * will be truncated. Therefore, '*abcdefg'
    would be equivalent to '*', and would match every string.

    :return true/false.
    """
    def is_matching(self, matchstring, string):
        # If no wild card, we just test equality.
        if '*' not in matchstring:
            return matchstring == string

        # Truncate starting at the first wild card
        # and check if the prefixes match.
        before_star = matchstring.split('*')[0]
        return string[:len(before_star)] == before_star

    """
    Confirm that the username and password fields are correct.

    :param request_object: This is the internal request object that
    contains the information needed for the given request

    Assumptions:
    This will cause a crash if the username/password fields are missing.
    The client code enforces providing a username/password, so that will not happen.

    :return dictionary indicating success/failure, text response on failure.
    """
    def validate_user(self, request_object):
        # Verify that the username is valid.
        username = request_object["username"]
        if username not in self.usernames:
            return { "success" : False, "response" : "User does not exist." }

        # Verify that the username/password combination is valid.
        user_id = self.usernames[username]
        if self.users[user_id]["password"] != request_object["password"]:
            return { "success" : False, "response" : "Invalid password." }

        return { "success" : True, "response" : "Success!" }

    """
    Adds a user to a group.

    This is currently only called to add  new users to the 'all' group.

    :param username: The name of the user to be added to the group.
    :param groupname: The name of the group.

    :return dictionary indicating success/failure, text response on failure.
    """
    def add_user_to_group(self, username, groupname):
        group_id = self.groupNames[groupname]
        user_id  = self.usernames[username]

        # Don't add a user multiple times to the same group,
        # as this could result in duplicate messages.
        if user_id not in self.groups[group_id]["users"]:
            self.groups[group_id]["users"].append(user_id)

    """
    Register a new user.

    :param request_object: This is the internal request object that
    contains the information needed for the given request

    Assumptions:
    This will cause a crash if the username field is missing.
    The client code enforces providing a username, so that will not happen.

    :return dictionary indicating success/failure, text response on failure.
    """
    def register_user(self, request_object):
        # Return failure if the username is taken
        # either as another user or as a group name
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

    """
    Return a list of all accounts (or just those that match a wildcard).

    :param request_object: This is the internal request object that
    contains the information needed for the given request.

    The wildcard must be specified in a "matchstring" attribute in request_object.
    If left out, this will return all accounts.

    :return dictionary indicating success/failure, list of accounts.
    """
    def list_accounts(self, request_object):
        response       = {}
        relevant_users = self.users

        # Filters the users down to the subset that match the matchstring.
        if "matchstring" in request_object and request_object["matchstring"]:
            relevant_users = dict((k, v) for k, v in self.users.items() if self.is_matching(request_object["matchstring"], v["username"]))

        # Extracts just the username from the user objects so we don't
        # return any credentials!
        for user_id in relevant_users:
            response[user_id] = relevant_users[user_id]["username"]

        return { "success" : True, "response" : response }

    """
    Initializes a new group.

    :param request_object: This is the internal request object that
    contains the name of the group and the list of users to be added
    to the group.

    Assumptions:
    request_object["name"] is the name of the group.
    request_object["users"] is a list of users.

    :return dictionary indicating success/failure, text response on failure.
    """
    def create_group(self, request_object):
        # Verify that the group name is free.
        if request_object["name"] in self.groupNames:
            return { "success" : False, "response" : "Group name is already taken." }

        next_id = self.get_next_id(self.groups)

        # Check that all the users are valid.
        users = []
        for user in request_object["users"]:
            if user not in self.usernames:
                return { "success" : False, "response" : "One or more users don't exist." }
            else:
                users.append(self.usernames[user])

        # Initialize the new group.
        self.groups[next_id] = { "name" : request_object["name"], "users" : users }
        self.groupNames[request_object["name"]] = next_id
        return { "success" : True, "response" : None }

    """
    Return a list of all groups (or just those that match a wildcard).

    :param request_object: This is the internal request object that
    contains the information needed for the given request.

    The wildcard must be specified in a "matchstring" attribute in request_object.
    If left out, this will return all groups.

    :return dictionary indicating success/failure, list of groups.
    """
    def list_groups(self, request_object):
        # Get all groups excluding the groups that actually represent single users.
        # A group with one member will be listed as long as it wasn't the dummy
        # group created upon initializing a user.
        relevant_groups = dict((k, v) for k, v in self.groups.items() if len(v["users"]) != 1 or self.users[v["users"][0]]["username"] != v["name"])

        # Filters the groups down to those that match the string.
        if "matchstring" in request_object and request_object["matchstring"]:
            relevant_groups = dict((k, v) for k, v in relevant_groups.items() if self.is_matching(request_object["matchstring"], v["name"]))

        # Parse the group data structure to make it human-readable before returning.
        response = {}
        for group_id in relevant_groups:
            response[group_id] = { "name" : relevant_groups[group_id]["name"], "users" : map(lambda user_id : self.users[user_id]["username"], relevant_groups[group_id]["users"]) }

        return { "success" : True, "response" : response }

    """
    Sends a message to a group or user.

    :param request_object: This is the internal request object that
    contains the name of the group (or user) and the message.

    Assumptions:
    request_object["groupname"] is the name of the group (or user).
    request_object["message"] is a list of users.
    request_object["username"] and request_object["password"] contain
    the appropriate credentials (automatically submitted via the client).

    :return dictionary indicating success/failure, text response on failure.
    """
    def send_message(self, request_object):
        # Checks credentials so you can't spoof messages!
        validation = self.validate_user(request_object)
        if not validation["success"]:
            return validation

        group_name = request_object["groupname"]

        # Check that it is a valid group.
        if group_name not in self.groupNames:
            return { "success" : False, "response" : "Group does not exist." }

        group_id = self.groupNames[group_name]

        # Send the message to everyone in the group.
        for user_id in self.groups[group_id]['users']:
            self.messages[user_id].append('%s: %s' % (request_object["username"], request_object["message"]))

        return { "success" : True, "response" : "Message sent." }

    """
    Gets all of the messages that have been sent to a user.

    :param request_object: This is the internal request object that
    contains the username and password.

    Assumptions:
    request_object["username"] and request_object["password"] contain
    the appropriate credentials (automatically submitted via the client).

    :return dictionary indicating success/failure, the list of messages.
    """
    def get_messages(self, request_object):
        # Validate credentials so you can't get other people's messages.
        validation = self.validate_user(request_object)
        if not validation["success"]:
            return validation

        user_id = self.usernames[request_object["username"]]

        # Returns the messages and clears the cached messages.
        messages = self.messages[user_id]
        self.messages[user_id] = []
        return { "success" : True, "response" : messages }

    """
    Deletes an account.

    :param request_object: This is the internal request object that
    contains the username and password.

    Assumptions:
    request_object["username"] and request_object["password"] contain
    the appropriate credentials (automatically submitted via the client).

    :return dictionary indicating success/failure, text response on failure.
    """
    def delete_account(self, request_object):
        # Ensures you can't delete someone else's account.
        validation = self.validate_user(request_object)
        if not validation["success"]:
            return validation

        username = request_object["username"]
        user_id  = self.usernames[username]

        # Clears the user object.
        del self.users[user_id]
        del self.usernames[username]

        # Clears the user from its groups.
        empty_groups = []
        for group_id in self.groups:
            if user_id in self.groups[group_id]['users']:
                self.groups[group_id]['users'].remove(user_id)
                if len(self.groups[group_id]['users']) == 0:
                    empty_groups.append(group_id)

        # Removes any now-empty groups.
        for group_id in empty_groups:
            del self.groupNames[self.groups[group_id]["name"]]
            del self.groups[group_id]

        # Removes the user's message queue.
        del self.messages[user_id]

        return { "success" : True, "response" : None }
