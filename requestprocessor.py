class RequestProcessor:

  def __init__(self):
    # userId -> user object
    users    = {}
    # groupId -> list of userIds
    groups   = {}
    # userId -> pending messages
    messages = {}

  def register_user(self, request_object):
      pass

  def list_accounts(self, request_object):
      pass

  def create_group(self, request_object):
      pass

  def list_groups(self, request_object):
      pass

  def send_message(self, request_object):
      pass

  def get_messages(self, request_object):
      pass

  def delete_account(self, request_object):
      pass
