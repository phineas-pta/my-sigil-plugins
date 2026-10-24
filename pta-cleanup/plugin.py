# -*- coding: utf-8 -*-

# from typing import TYPE_CHECKING # require python 3.5
# if TYPE_CHECKING:
# 	from bookcontainer import BookContainer
## additional modules: Sigil > src/Resource_Files/plugin_launchers/python

from utils import clean_nav, clean_spacing

def run(bk: "BookContainer") -> int:

	if bk.epub_version().startswith("3."):
		navID = bk.getnavid()
		bk.writefile(navID, clean_nav(bk.readfile(navID)))

	for fileID, _ in bk.text_iter():
		bk.writefile(fileID, clean_spacing(bk.readfile(fileID)))

	return 0

if __name__ == "__main__":
	print("i reached main when i should not have")
	import sys
	sys.exit(-1)
