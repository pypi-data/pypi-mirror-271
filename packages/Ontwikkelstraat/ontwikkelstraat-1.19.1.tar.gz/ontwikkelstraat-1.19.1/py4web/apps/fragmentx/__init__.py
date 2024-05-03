# check compatibility
import py4web

assert py4web.check_compatible("0.1.20190709.1")
import sys

# by importing controllers you expose the actions defined in it
from . import controllers

# by importing db you expose it to the _dashboard/dbadmin
from .models import db

# sys.stdout.reconfigure(encoding="utf-8")
# sys.stderr.reconfigure(encoding="utf-8")
# import codecs # output=codecs.getwriter('utf8')(sys.stderr).write


# optional parameters
__version__ = "0.0.0"
__author__ = "Remco Boerma <remco.b@educationwarehouse.nl>"
__license__ = "Copyright"
