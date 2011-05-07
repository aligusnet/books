import os
import sys
import epub
import index
import lexems

def intersect(lhs, rhs):
	i, j = 0, 0
	n, m = len(lhs), len(rhs)
	result = []
	while i < n and j < m:
		d = lhs[i] - rhs[j]
		if d == 0:
			result.append(lhs[i])
			i +=1; j += 1
		elif d < 0:
			i += 1
		else:
			j += 1
	return result

def search(keywords, idx):
	
	def size_cmp(lhs, rhs):
		return len(lhs) - len(rhs)
	
	keywords = lexems.get(keywords)
	docs = []
	for keyword in keywords:
		docs.append(idx.docids(keyword.lower()))
	
	if len(docs) == 0:
		return docs
	
	docs.sort(size_cmp)
	
	docids = docs[0]
	for i in xrange(1, len(docs)):
		docids = intersect(docids, docs[i])
	
	result = []
	for docid in docids:
		result.append(idx.document(docid))
		
	return result

def printResult(docs):
	for file_name in docs:
		info = epub.get_info(file_name)
		print info.author.strip() + '.', info.title + '. (' + file_name + ')'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage: ' + sys.argv[0] + ' dir [keywords]'
		os._exit(os.EX_USAGE)
	
	idx = index.Index(sys.argv[1].decode('utf-8'))
	
	if len(sys.argv) > 2:
		keywords = []
		for i in xrange(2, len(sys.argv)):
			keywords.append(sys.argv[i].decode('utf-8'))
		docs = search(' '.join(keywords), idx)
		printResult(docs)
		os._exit(os.EX_OK)
		
	print 'press Ctrl-D to exit'
	while True:
		try:
			keywords = raw_input('# ').decode('utf-8')
		except EOFError:
			print ('')
			break
		docs = search(keywords, idx)
		printResult(docs)