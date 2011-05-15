# -*- coding: utf-8 -*-

from __future__ import print_function
import xmlrpclib
import config

def printEntry(entry):
	entry['author'] = ', '.join(entry['author'])
	entry['title'] = ', '.join(entry['title'])
	print('%(id)d. Author(s): %(author)s, Title: %(title)s' % entry)

if __name__ == '__main__':
	proxy = xmlrpclib.ServerProxy('http://'+config.RPCServerHost+':'+str(config.RPCServerPort))
	print ('press Ctrl-D to exit')
	while True:
		try:
			keywords = raw_input('# ').decode(config.SystemCodePage)
			ndocs, result = proxy.search(keywords)
			print('found %d books' % ndocs)
			map(printEntry, result)
		except EOFError:
			print ('')
			break
		except xmlrpclib.Fault, err:
			print('A remote error occured')
			print('Error code: %d' % err.faultCode)
			print('Error string: %s' % err.faultString)
		except xmlrpclib.ProtocolError, err:
			print('A protocol error occurred')
			print('URL: %s' % err.url)
			print('HTTP/HTTPS headers: %s' % err.headers)
			print('Error code: %d' % err.errcode)
			print('Error message: %s' % err.errmsg)
			break