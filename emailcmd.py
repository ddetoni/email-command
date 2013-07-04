import poplib

class Email(object):
    """
    Handles emails


    self.username = username
    self.password = password
    self.host = host

    self.welcome = mail.getwelcome()
    self.stat = mail.stat()
    self.list = mail.list()

    self.num_messages = Number of messages
    self.mail = The POP3_SSL object
    self.messages = messages retrieved
    """

    def has_new_mails(self):
        if self.stat[1] > 0:
            return True
        else:
            return False

    def get_emails(self):
        num = self.num_messages
        self.messages = []
        messages = []

        for i in range(num):
            response, lines, bytes = self.mail.retr(i + 1)

            # Remove trailing blank lines from message
            while lines[-1] == "":
                del lines[-1]

            try:
                endOfHeader = lines.index('')
                header = lines[:endOfHeader]
                body = lines[endOfHeader+1:]
            except ValueError:
                header = lines
                body = []

            messages.append({"header": header, "body": body})

        self.messages = messages
        
    def __connect(self):
        try:
            mail = poplib.POP3_SSL(self.host)
            self.welcome = mail.getwelcome()
            mail.user(self.username)
            mail.pass_(self.password)
            self.stat = mail.stat()
            self.list = mail.list()
            self.num_messages = len(self.list[1])
            self.mail = mail
        except:
            print "Failed to connect"

    def __init__(self, username=None, password=None, host=None):
        self.username = username
        self.password = password
        self.host = host

        self.__connect()

        if self.has_new_mails():
            self.get_emails()
        else:
            self.messages = []

class EmailCommand(Email):
    """
    Run commands via email
    """

    def __init__(self, username=None, password=None, host=None):
        Email.__init__(self, username, password, host)