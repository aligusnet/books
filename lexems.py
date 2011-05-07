# -*- coding: utf-8 -*-

import Stemmer

__rustemmer = Stemmer.Stemmer('russian')

def get(text):
	text = text.lower()
	res = [u'']
	for char in text:
		if char.isalpha():
			res[-1] += char
		elif res[-1] != u'':
			res.append(u'')
	if res[-1] == u'': del res[-1]
	return __rustemmer.stemWords(res)
