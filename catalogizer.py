# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import shutil

import epub
import config

def normalize_name(name):
	name = name.lower()
	parts = []
	for part in name.split(' '):
		if part != '':
			parts.append(part)
	return ' '.join(parts).title(), parts[-1][0]
				
def build_tree(source_dir, target_dir):
	for root, dirs, files in os.walk(source_dir):
		for name in files:
			if name.lower().endswith('.epub'):
				full_name = os.path.join(root, name)
				try:
					info = epub.get_info(full_name)
				except Exception, ex:
					print('error while parsing file:', full_name, ex)
					continue
				
				if info.author and info.title:
					creator, letter = normalize_name(info.author[0])
					title, _ = normalize_name(info.title[0])
					target_name = os.path.join(target_dir, letter, creator, title+'.epub')
					creator_dir = os.path.dirname(target_name)
					if not os.path.exists(creator_dir):
						os.makedirs(creator_dir, config.DirectoryDefaultMode)
					shutil.copy(full_name, target_name)
					os.chmod(target_name, config.FileDefaultMode)
				else:
					print('file', full_name, "skipped, because it hasn't author and title in metadata")
				

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print ('Usage: python', sys.argv[0], ' source_dir target_dir')
		os._exit(os.EX_USAGE)
	build_tree(sys.argv[1].decode(config.SystemCodePage), sys.argv[2].decode(config.SystemCodePage))