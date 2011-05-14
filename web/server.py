#!/usr/bin/env python

from wsgiref.simple_server import make_server
import handler
import config

if __name__ == '__main__':
	httpd = make_server('', config.WebServerPort, handler.Application)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		print('stopping server...')
