# -*- coding: utf-8 -*-

# from typing import TYPE_CHECKING # require python 3.5
# if TYPE_CHECKING:
# 	from bookcontainer import BookContainer
## additional modules: Sigil > src/Resource_Files/plugin_launchers/python

from utils import PATTERN, word2int

def run(bk: "BookContainer") -> int:
	for fileID, _ in bk.text_iter():
		print(fileID)
		bk.writefile(fileID, PATTERN.sub(word2int, bk.readfile(fileID)))
		print()
	return 0

if __name__ == "__main__":
	print("i reached main when i should not have")
	import sys
	sys.exit(-1)
