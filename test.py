import emailcmd
import config

ecmd = emailcmd.EmailCommand(config.username, config.password, config.host)
print ecmd.has_new_mails()