# -*- coding: utf-8 -*-
"""
Epub files parser
"""
from __future__ import unicode_literals
import zipfile
import os
from lxml import etree

class Reader(object):
	ns = {
			'n':'urn:oasis:names:tc:opendocument:xmlns:container',
			'pkg':'http://www.idpf.org/2007/opf',
			'dc':'http://purl.org/dc/elements/1.1/'
		}
	def __init__(self, file_name):
		self.zip = zipfile.ZipFile(file_name)
		txt = self.zip.read('META-INF/container.xml')
		tree = etree.fromstring(txt)
		cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=self.ns)[0]
		self.data_path = os.path.dirname(cfname)
		cf = self.zip.read(cfname)
		tree = etree.fromstring(cf)
		self.metadata = tree.xpath('/pkg:package/pkg:metadata',namespaces=self.ns)[0]
		
	def __read_metadata(self, tag):
		return tuple(self.metadata.xpath('dc:%s/text()'%(tag), namespaces=self.ns))
		
	def __read_data_file(self, file_name):
		return self.zip.read(os.path.join(self.data_path, file_name))

	def read_authors(self):
		return self.__read_metadata('creator')
		
	def read_titles(self):
		return self.__read_metadata('title')
	
	def read_descriptions(self):
		return self.__read_metadata('description')
		
	def read_languages(self):
		return self.__read_metadata('language')
		
	def __read_cover_path(self):
		lst_meta = self.metadata.xpath('pkg:meta', namespaces=self.ns)
		for meta in lst_meta:
			d = dict(meta.items())
			if d.get('name', '') == 'cover':
				return d.get('content', '')
		return ''
		
	def read_cover(self):
		path = self.__read_cover_path()
		name = os.path.basename(path)
		if path:
			return name, self.__read_data_file(path)
		return ('', '')

class Info(object):
	"""
	Stores metadata info of epub file
	
	author - list of authors
	title - list of title
	language - list of languages
	"""
	def __init__(self, file_name):
		"initialize new Info object"
		
		reader = Reader(file_name)
		self.title_ = reader.read_titles()
		self.author_ = reader.read_authors()
		self.language_ = reader.read_languages()
		
	def authors(self):
		"""
		I.authors() -> str
		
		return string containing comma-separated list of authors
		"""
		return ', '.join(self.author_)
		
	def titles(self):
		"""
		I.titles() -> str
		
		return string containing comma-separated list of titles
		"""
		return ', '.join(self.title_)
