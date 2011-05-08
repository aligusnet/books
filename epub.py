# -*- coding: utf-8 -*-
"""
Epub files parser
"""
from __future__ import unicode_literals
import zipfile
from lxml import etree

class Info(object):
	"""
	Stores metadata info of epub file
	
	author - list of authors
	title - list of title
	language - list of languages
	"""
	def __init__(self, res):
		"initialize new Info object"
		self.title = res['title']
		self.author = res['creator']
		self.language = res['language']
		
	def authors(self):
		"""
		I.authors() -> str
		
		return string containing comma-separated list of authors
		"""
		return ', '.join(self.author)
		
	def titles(self):
		"""
		I.titles() -> str
		
		return string containing comma-separated list of titles
		"""
		return ', '.join(self.title)

def get_info(file_name):
	"""
	S.get_info(file_name) -> Info
	
	Parse epub file and return Info object containing metadata
	"""
	ns = {
			'n':'urn:oasis:names:tc:opendocument:xmlns:container',
			'pkg':'http://www.idpf.org/2007/opf',
			'dc':'http://purl.org/dc/elements/1.1/'
		}
	
	zip = zipfile.ZipFile(file_name)
	txt = zip.read('META-INF/container.xml')
	tree = etree.fromstring(txt)
	cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]
	
	cf = zip.read(cfname)
	tree = etree.fromstring(cf)
	p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]
	
	res = {}
	for s in ['title', 'creator', 'language']:
		res[s] = p.xpath('dc:%s/text()'%(s), namespaces=ns)
			
	return Info(res)