# -*- coding: utf-8 -*-

import sys

# additional modules: Sigil > src/Resource_Files/plugin_launchers/python

from smartypants import _Attr, smartypants


def run(bk: "BookContainer") -> int:
	ATTR = _Attr.set1 | _Attr.u
	for fileID, href in bk.text_iter():
		bk.writefile(fileID, smartypants(bk.readfile(fileID), attr=ATTR))
		print(href)
	return 0


if __name__ == "__main__":
	print("i reached main when i should not have")
	sys.exit(-1)
