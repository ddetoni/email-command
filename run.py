import emailcmd
import config
import sched
import time

s = sched.scheduler(time.time, time.sleep)
def yo(sc): 
    ecmd = emailcmd.EmailCommand(config.username, config.password, config.host)
    ecmd.run_command()
    ecmd.cleanup()
    sc.enter(10, 1, yo, (sc,))

s.enter(10, 1, yo, (s,))
s.run()


