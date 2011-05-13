# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import urlparse
import cgi

import xmlrpclib
import config
import templates

def strEntry(entry):
	return templates.entry % entry

def search(keywords):
	proxy = xmlrpclib.ServerProxy('http://'+config.RPCServerHost+':'+str(config.RPCServerPort))
	result = proxy.search(keywords, 0, 30)
	result = map(strEntry, result)
	result = '\n'.join(result)
	return {'keywords': keywords.encode('utf-8'), 'rows': result.encode('utf-8')}

def description(docid):
	proxy = xmlrpclib.ServerProxy('http://'+config.RPCServerHost+':'+str(config.RPCServerPort))
	result = proxy.detailed_info(docid)
	if result['cover']:
		result['image'] = templates.image % result
	else:
		result['image'] = ''
	return templates.description % result
	
def image(docid):
	proxy = xmlrpclib.ServerProxy('http://'+config.RPCServerHost+':'+str(config.RPCServerPort))
	cover = proxy.get_cover(docid)
	return (cover[0], cover[1].data)

def application(environ, start_response):
	path = environ['PATH_INFO']
	qs = urlparse.parse_qs(environ['QUERY_STRING'])
	response_headers = [('Content-Type', 'text/html; charset=utf-8')]
	response_body = ''
	if path.endswith('search'):
		if 'keywords' in qs:
			sr = search(cgi.escape(qs['keywords'][0]).decode('utf-8'))
		else:
			sr = {'keywords': '', 'rows': ''}
		result_table = templates.result % sr
		response_body = templates.html % result_table
	elif path.endswith('description'):
		if 'id' in qs:
			response_body = description(int(qs['id'][0])).encode('utf-8')
		else:
			response_body = 'incorrect document id'
	elif path.endswith('image'):
		response_headers = [('Content-Type', 'image')]
		if 'id' in qs:
			cover = image(int(qs['id'][0]))
			response_body = cover[1]
	else:
		response_body = templates.html % ''
	
	status = '200 OK'
	
	response_headers.append(('Content-Length', str(len(response_body))))
	start_response(status, response_headers)
	return [response_body]
