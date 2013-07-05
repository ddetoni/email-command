# email-command #

Run commands via email.

Notes
-----

* Requirement: Python (>= 2.7.3)
* Rename config_example.py to config.py -- set variables respectively.
* Use a dedicated email
    * It deletes all messages it opened
    * Some email providers like gmail still keep deleted messages depending on user setting
* Run run.py or in background with nohup python run.py > /dev/null 2>&1 &
* Use the following email body format:

    {"type": "terminal", "command": ["ls", "-la"]}
    {"type": "terminal", "command": ["touch", "meow"]}

* Must be a valid JSON format
* One command per line
* **Use at your own risk!**


License
-------

Licensed under the Apache License, Version 2.0. See: LICENSE for more info.