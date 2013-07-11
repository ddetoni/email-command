import emailcmd
import config
import sched
import time

s = sched.scheduler(time.time, time.sleep)
def yo(sc): 
    with emailcmd.EmailCommand(config.username, config.password, config.host) as ecmd:
    	ecmd.run_command()
    sc.enter(10, 1, yo, (sc,))

s.enter(10, 1, yo, (s,))
s.run()


