# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import urlparse
import cgi
import xmlrpclib
import wsgiref.util

import config
import templates
from contenttype import ContentType

class Application(object):
	def __init__(self, environ, start_response):
		if config.ApplicationPath[-1] != '/':
			config.ApplicationPath += '/'
		
		page = wsgiref.util.shift_path_info(environ)
		
		self.environ = environ
		self.start_response = start_response
		self.query_string = urlparse.parse_qs(environ['QUERY_STRING'])
		self.path_parts = self.environ['PATH_INFO'].split('/')
		
		self.response_headers = []
		self.status = '200 OK'
		self.response_body = ''
		
		if page == '':
			self.index()
		elif page == 'search':
			self.search()
		elif page == 'description':
			self.description()
		elif page == 'image':
			self.image()
		else:
			self.move_to_index()
		
	def __iter__(self):
		self.start_response(self.status, self.response_headers)
		yield self.response_body
		
	def __get_proxy(self):
		return xmlrpclib.ServerProxy('http://'+config.RPCServerHost+':'+str(config.RPCServerPort))
		
	def index(self):
		self.response_headers.append(('Content-Type', 'text/html; charset=utf-8'))
		self.response_body = (templates.html % u'').encode('utf-8')
		
	def search(self):
		self.response_headers.append(('Content-Type', 'text/html; charset=utf-8'))
		keywords = cgi.escape(self.query_string.get('keywords', [''])[0]).decode('utf-8')
		
		proxy = self.__get_proxy()
		result = proxy.search(keywords, 0, 30)
		result = map(lambda entry: templates.entry % entry, result)
		result = '\n'.join(result)
		result_table = templates.result % {'keywords': keywords, 'rows': result}
		response_body = templates.html % result_table
		self.response_body = response_body.encode('utf-8')
	
	def description(self):
		self.response_headers.append(('Content-Type', 'text/html; charset=utf-8'))
		if len(self.path_parts) > 1:
			docid = int(self.path_parts[1])
			proxy = self.__get_proxy()
			info = proxy.detailed_info(docid)
			info['app_path'] = config.ApplicationPath
			if info['cover']:
				info['image'] = templates.image % info
			else:
				info['image'] = ''
			response_body = templates.description % info
		else:
			response_body = u'missed document id'
		self.response_body = response_body.encode('utf-8')
		
	def __image_content_type(self, name):
		ext = name.lower().split('.')[-1]
		return ContentType.extensions.get(ext, 'image')
			
	def image(self):
		if len(self.path_parts) > 1:
			docid = int(self.path_parts[1])
			proxy = self.__get_proxy()
			cover = proxy.get_cover(docid)
			self.response_body = cover[1].data
			self.response_headers.append(('Content-Type', self.__image_content_type(cover[0])))
			self.response_headers.append(('Title', cover[0].encode('utf-8')))
		else:
			self.response_headers.append(('Content-Type', 'image'))

	def move_to_index(self):
		self.status = '301 Moved Permanently'
		redirect_url = self.environ['wsgi.url_scheme'] + '://' + self.environ['HTTP_HOST'] + config.ApplicationPath
		
		self.response_headers.append(('Content-Type', 'text/html; charset=utf-8'))
		self.response_headers.append(('Location', redirect_url))
		response_body = templates.move % redirect_url
		self.response_body = response_body.encode('utf-8')
