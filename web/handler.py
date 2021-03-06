# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
import urlparse
import cgi
import xmlrpclib
import wsgiref.util
import uuid

import config
import templates
from contenttype import ContentType

class Application(object):
	def __init__(self, environ, start_response):
		if config.ApplicationPath[-1] != '/':
			config.ApplicationPath += '/'
		
		page = wsgiref.util.shift_path_info(environ)
		
		self.app_url = environ['wsgi.url_scheme'] + '://' + environ['HTTP_HOST'] + config.ApplicationPath
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
		elif page == 'book':
			self.download_book()
		else:
			self.move_to_index()
		
	def __iter__(self):
		self.start_response(self.status, self.response_headers)
		yield self.response_body
		
	def __get_proxy(self):
		return xmlrpclib.ServerProxy('http://'+config.RPCServerHost+':'+str(config.RPCServerPort))
		
	def index(self):
		self.response_headers.append(('Content-Type', 'text/html; charset=utf-8'))
		self.response_body = (templates.html % (self.app_url, u'')).encode('utf-8')

	def search(self):
		
		def processEntry(entry, pos):
			entry['pos'] = pos
			if(entry['author']):
				entry['author'] = u', '.join(entry['author'])
			else:
				entry['author'] = u'unknown author'
			if(entry['title']):
				entry['title'] = entry['title'][0]
			else:
				entry['title'] =  u'unknown title'
			return templates.entry % entry
		
		self.response_headers.append(('Content-Type', 'text/html; charset=utf-8'))
		keywords = self.query_string.get('keywords', [''])[0].decode('utf-8')
		page = int(self.query_string.get('page', ['1'])[0])-1
		
		proxy = self.__get_proxy()
		ndocs, result = proxy.search(keywords, page, config.DocumentsOnPage)
		
		#paging
		npages = (ndocs + config.DocumentsOnPage-1)/config.DocumentsOnPage
		pagerefs = ''
		if npages > 1:
			pageref_params = {'keywords': cgi.urllib.quote_plus(keywords.encode('utf-8'))}
			for p in range(npages):
				pageref_params['page'] = p+1
				if page != p:
					pagerefs += templates.pageref % pageref_params
				else:
					pagerefs += templates.page % pageref_params
		
		result = map(processEntry, result, range(page*config.DocumentsOnPage+1, min((page+1)*config.DocumentsOnPage, ndocs)+1))
		result = '\n'.join(result)
		result_table = templates.result % {'keywords': cgi.escape(keywords), 'rows': result, 'ndocs': ndocs, 'pagerefs': pagerefs}
		response_body = templates.html % (self.app_url, result_table)
		self.response_body = response_body.encode('utf-8')
	
	def description(self):
		self.response_headers.append(('Content-Type', 'text/html; charset=utf-8'))
		if len(self.path_parts) > 1:
			docid = int(self.path_parts[1])
			proxy = self.__get_proxy()
			info = proxy.detailed_info(docid)
			info['app_url'] = self.app_url
			if(info['author']):
				info['author'] = u', '.join(info['author'])
			else:
				info['author'] = u'unknown author'
			if(info['title']):
				info['short_title'] = info['title'][0]
				info['title'] = u'<br />'.join(info['title'])
			else:
				info['title'] =  u'unknown title'
				info['short_title'] = info['title']
			info['description'] = u'<br />'.join(info['description'])
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
			self.response_headers.append(('Content-Disposition', 'Inline; filename="%s"' % cover[0].encode('utf-8')))
		else:
			self.response_headers.append(('Content-Type', 'image'))
			
	def download_book(self):
		if len(self.path_parts) > 1:
			docid = int(self.path_parts[1])
			proxy = self.__get_proxy()
			data = proxy.get_book(docid).data
			if len(self.path_parts) > 2:
				name = self.path_parts[2]
			else:
				name = str(uuid.uui4())+'.epub'
			self.response_body = data
			self.response_headers.append(('Content-Type', ContentType.extensions['epub']))
			self.response_headers.append(('Content-Disposition', 'Attachment; filename="%s"' % name))

	def move_to_index(self):
		self.status = '301 Moved Permanently'
		self.response_headers.append(('Content-Type', 'text/html; charset=utf-8'))
		self.response_headers.append(('Location', self.app_url))
		response_body = templates.move % self.app_url
		self.response_body = response_body.encode('utf-8')
