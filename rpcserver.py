# -*- coding: utf-8 -*-

from __future__ import print_function
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import sys
import os

import config
import index
import search
import epub

def __makeResultEntry(docid):
	entry = {'id':docid}
	file_path = idx.document(docid)
	info = epub.get_info(file_path)
	entry['author'] = info.authors()
	entry['title'] = info.titles()
	return entry
	
def __search(keywords, page=0, resultsOnPage=10):
	docs = search.search(keywords, idx)
	docs = docs[page*resultsOnPage:(page+1)*resultsOnPage]
	result = [__makeResultEntry(docid) for docid in docs]
	return result

class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)
	
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print ('Usage: python', sys.argv[0], 'path/to/lib')
		os._exit(os.EX_USAGE)
	
	global idx
	idx = index.Index(sys.argv[1].decode('utf-8'))
	
	server = SimpleXMLRPCServer((config.RPCServerHost, config.RPCServerPort), requestHandler=RequestHandler)
	server.register_introspection_functions()
	
	server.register_function(__search, 'search')
	server.serve_forever()
