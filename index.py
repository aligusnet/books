# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import struct
import fnmatch

import lexems
import epub

def create_index(root):
	docid_file = open(os.path.join(root, u'docid'), 'wb')
	docid_idx = open(os.path.join(root, u'docid.idx'), 'wb')
	
	dictionary = {}
	index = []
	lexid = 0
	docid = 0
	for parent, dirs, files in os.walk(root):
		for name in files:
			if fnmatch.fnmatch(name, u'*.epub'):
				try:
					full_name = os.path.join(parent, name)
					docid_idx.write(struct.pack('i', docid_file.tell()))
					docid_file.write(full_name)
					info = epub.get_info(full_name)
					lex = lexems.get(info.author)
					lex.extend(lexems.get(info.title))
					for w in lex:
						if not dictionary.has_key(w):
							dictionary[w] = lexid
							lexid += 1
							index.append([])
						index[dictionary[w]].append(docid)
					docid += 1
				except Exception, ex:
					print (ex, ': error while processing file:', full_name)
				
	docid_file.close()
	docid_idx.close()
				
	index_file = open(os.path.join(root, u'index'), 'wb')
	dict_file = open(os.path.join(root, u'dict'), 'wb')
	for key, value in dictionary.items():
		for id in index[value]:
			index_file.write(struct.pack('i', id))
		dict_file.write('%i %s\n' % (index_file.tell(), key.encode('utf-8')))
	index_file.close()
	dict_file.close()
	
#-------------------------------
	
	
class Index(object):
	def __init__(self, root_dir):
		self.docid_file = open(os.path.join(root_dir, u'docid'), 'rb')
		self.index_file = open(os.path.join(root_dir, u'index'), 'rb')
		
		self.docid_idx = self._read_idx(os.path.join(root_dir, u'docid.idx'))
		self.dictionary = self._read_dictionary(os.path.join(root_dir, u'dict'))
		
	def document(self, docid):
		if len(self.docid_idx) <= docid:
			return u''
		info = self.docid_idx[docid]
		self.docid_file.seek(info[0])
		return self.docid_file.read(info[1]).decode('utf-8')
		
	def docids(self, lexem):
		INT_SIZE = 4
		if not self.dictionary.has_key(lexem):
			return ()
		info = self.dictionary[lexem]
		ndocs = info[1]/INT_SIZE
		self.index_file.seek(info[0])
		bytes = self.index_file.read(info[1])
		docs = struct.unpack('i'*ndocs, bytes)
		return docs
		
	def _read_idx(self, file_name):
		INT_SIZE = 4
		result = []
		idx = open(file_name, 'rb')
		idx.read(INT_SIZE) #skip zero
		bytes = idx.read(INT_SIZE)
		start_pos = 0
		while len(bytes) == INT_SIZE:
			curr_pos = struct.unpack('i', bytes)[0]
			result.append((start_pos, curr_pos-start_pos))
			start_pos = curr_pos
			bytes = idx.read(INT_SIZE)

		idx.close()
		return result
	
	def _read_dictionary(self, file_name):
		dictionary = {}
		dict_file = open(file_name, 'r')
		start_pos = 0
		with open(file_name, 'r') as dict_file:
			for line in dict_file:
				parts = line.rstrip().split(' ')
				curr_pos = int(parts[0])
				lexem = parts[1].decode('utf-8')
				dictionary[lexem] = (start_pos, curr_pos-start_pos)
				start_pos = curr_pos

		return dictionary
		
#-------------------------------

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print ('Usage: python', sys.argv[0], ' dir')
		os._exit(os.EX_USAGE)
	create_index(sys.argv[1])