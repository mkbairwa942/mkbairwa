#!/usr/bin/python
activate_this = '/var/www/Capital_vercel1/myenv/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Capital_vercel1/")
from Capital_vercel1 import app as application
application.secret_key = 'Add-my-secret-1234-key!@$$%^&*(sdfsdf643535##$$'