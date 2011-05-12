import urlparse
import cgi

import xmlrpclib
import config

html = """
<html>
<body>
	<form method="get" action="search">
		<p>
			books: <input type="text" name="keywords">
		</p>
	</form>
	<p>
	<h3>%(keywords)s</h3>
	%(result)s
	</p>
</body>
</html>
"""

def strEntry(entry):
	return '%(id)d. %(author)s. <b>%(title)s</b>' % entry


def search(keywords):
	proxy = xmlrpclib.ServerProxy('http://'+config.RPCServerHost+':'+str(config.RPCServerPort))
	result = proxy.search(keywords, 0, 30)
	result = map(strEntry, result)
	result = '<br \>'.join(result)
	return {'keywords': keywords.encode('utf-8'), 'result': result.encode('utf-8')}


def application(environ, start_response):
	path = environ['PATH_INFO']
	sr = {'keywords': '', 'result': ''}
	if path == '/search':
		qs = urlparse.parse_qs(environ['QUERY_STRING'])
		if 'keywords' in qs:
			sr = search(cgi.escape(qs['keywords'][0]).decode('utf-8'))
	response_body = html % sr
	
	status = '200 OK'
	
	response_headers = [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)
	return [response_body]
