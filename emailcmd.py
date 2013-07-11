import poplib
import json
import subprocess

class Email(object):
    """Handles email"""

    def has_new_mails(self):
        if not is_connected:
            raise Exception("Not connected")

        if self.stat[1] > 0:
            return True
        return False

    def get_emails(self, delMsgs=True):
        """
        Retrieves all messages and store them in a list.
        An element contains a dict of header and body.

        Keyword arguments:
        delMsgs -- Mark all messages as deleted on retrieve
                   Note: Providers like Gmail can still keep deleted messages
                   depending on user setting.
        """

        if not self.is_connected:
            raise Exception("Not connected")

        num = self.num_messages
        self.messages = []
        messages = []

        for i in range(num):
            response, lines, bytes = self.mail.retr(i + 1)

            # Remove trailing blank lines from message.
            while lines[-1] == "":
                del lines[-1]

            # "lines" is a list.
            # Each element in the list is a line.

            try:
                endOfHeader = lines.index('')
                header = lines[:endOfHeader]
                body = lines[endOfHeader+1:]
            except ValueError:
                header = lines
                body = []

            messages.append({"header": header, "body": body})
            if delMsgs:
                self.mail.dele(i + 1)

        self.messages = messages

    def connect(self):
        mail = poplib.POP3_SSL(self.host)
        self.welcome = mail.getwelcome()
        mail.user(self.username)
        mail.pass_(self.password)
        self.stat = mail.stat()
        self.list = mail.list()
        self.num_messages = len(self.list[1])
        self.mail = mail
        self.is_connected = True

    def disconnect(self):
        if self.mail:
            self.mail.quit()
            self.mail = None
        self.is_connected = False

    def __init__(self, username=None, password=None, host=None):
        self.username = username
        self.password = password
        self.host = host
        self.welcome = None
        self.stat = None
        self.list = None
        self.num_messages = 0
        self.mail = None
        self.messages = []
        self.is_connected = False


class EmailCommand(Email):
    """
    Run commands via email.
    The body of a message must contain a valid JSON format.

    The following will suffice for now...

    {
        type: terminal,
        command: []
    }
    """

    def run_command(self, delMsgs=True):
        """
        Run all commands in the email.

        Keyword arguments:
        delMsgs -- Mark all messages as deleted on retrieve
        """

        self.get_emails(delMsgs)

        if len(self.messages) <= 0:
            return

        for message in self.messages:
            # One command per line in body
            for command in message["body"]:
                try:
                    command = json.loads(command)
                    if command["type"] == "terminal":
                        subprocess.call(command["command"])
                except:
                    print "Failed to run command"

    def __init__(self, username=None, password=None, host=None):
        Email.__init__(self, username, password, host)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()