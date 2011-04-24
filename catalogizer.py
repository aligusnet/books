# -*- coding: utf-8 -*-

import os
import sys
import fnmatch
import shutil
import epub

DEFAULT_DIRECTORY_MODE = 0755
DEFAULT_FILE_MODE = 0644

def normalize_name(name):
    name = name.lower()
    parts = []
    for part in name.lower().split(' '):
        if part != '':
            parts.append(part)
    return ' '.join(parts).title(), parts[-1][0]
                
def build_tree(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        for name in files:
            if fnmatch.fnmatch(name, '*.epub'):
                try:
                    full_name = os.path.join(root, name)
                    info = epub.get_info(full_name)
                    creator, letter = normalize_name(info.author)
                    title, _ = normalize_name(info.title)
                    target_name = os.path.join(target_dir, letter, creator, title+'.epub')
                    creator_dir = os.path.dirname(target_name)
                    if not os.path.exists(creator_dir):
                        os.makedirs(creator_dir, DEFAULT_DIRECTORY_MODE)
                    shutil.copy(full_name, target_name)
                    os.chmod(target_name, DEFAULT_FILE_MODE)
                except Exception, ex:
                    print ex, ': error while processing file: ' + full_name

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + ' source_dir target_dir'
        os._exit(os.EX_USAGE)
    build_tree(sys.argv[1], sys.argv[2])