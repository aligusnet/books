import os
import sys

__path = os.path.dirname(__file__)
sys.path.append(__path)
os.chdir(__path)

import handler

def application(environ, start_response):
	app = handler.Application(environ, start_response)
	return app
