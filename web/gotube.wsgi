#!/bin/python3
import sys
sys.path.append('/var/www/gotube/web')
from dotenv import load_dotenv
load_dotenv()

from server import app as application