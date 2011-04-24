# -*- coding: utf-8 -*-

import zipfile
from lxml import etree

class Info(object):
	def __init__(self, res):
		self.title = res[u'title']
		self.author = res[u'creator']
		#self.language = res[u'language']

def get_info(file_name):
    ns = {
            u'n':u'urn:oasis:names:tc:opendocument:xmlns:container',
            u'pkg':u'http://www.idpf.org/2007/opf',
            u'dc':u'http://purl.org/dc/elements/1.1/'
        }
    
    zip = zipfile.ZipFile(file_name)
    txt = zip.read(u'META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath(u'n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]
    
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath(u'/pkg:package/pkg:metadata',namespaces=ns)[0]
    
    res = {}
    for s in [u'title', u'creator']:
        res[s] = (p.xpath(u'dc:%s/text()'%(s), namespaces=ns)[0])
            
    return Info(res)