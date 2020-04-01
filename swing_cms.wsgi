#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/ciudadmujer.gob.sv/cmsv_happy/")

from swing_main import app as application
# 
# Replace this secret key for enhanced security.
#
# You could use a random generated string like:
#   python -c 'import os; print(os.urandom(16))'
#
application.secret_key = 'f63369280e32b1d90f783af2'.encode('utf8')
