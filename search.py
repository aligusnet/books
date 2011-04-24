import os
import sys
import epub
import index

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'Usage: ' + sys.argv[0] + ' dir keywords'
		os._exit(os.EX_USAGE)

	idx = index.Index(sys.argv[1].decode('utf-8'))
	keyword = sys.argv[2].decode('utf-8')
	
	docids = idx.docids(keyword.lower())
	for docid in docids:
		file_name = idx.document(docid)
		info = epub.get_info(file_name)
		print info.author.strip() + '.', info.title + '. (' + file_name + ')'