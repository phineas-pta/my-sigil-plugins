# -*- coding: utf-8 -*-

# additional modules: Sigil > src/Resource_Files/plugin_launchers/python

def run(bk: "BookContainer") -> int:

	import re

	if bk.epub_version().startswith("3."):
		navID = bk.getnavid()
		tmp = bk.readfile(navID)
		tmp = tmp.replace("<h1>Table of Contents</h1>", "<h1>Mục lục</h1>")
		tmp = re.sub(r'\s+<nav epub:type="landmarks" id="landmarks" hidden="">\s+<h1>Landmarks</h1>\s+<ol>\s+</ol>\s+</nav>', "", tmp)
		tmp = re.sub(r"<li>\s+(<a href.+</a>)\s+</li>", r"<li>\1</li>", tmp) # too much spacing in table of contents
		bk.writefile(navID, tmp)

	pattern1 = re.compile(r"  +(,\.!\?;)") # too much spacing before punctuation
	pattern2 = re.compile(r"(\w)  +(\w)") # too much spacing between words
	for fileID, _ in bk.text_iter():
		tmp = bk.readfile(fileID)
		tmp = tmp.replace(' class="sigil_not_in_toc"', "")
		tmp = pattern1.sub(r"\1", tmp)
		tmp = pattern2.sub(r"\1 \2", tmp)
		bk.writefile(fileID, tmp)

	return 0

if __name__ == "__main__":
	import sys
	print("i reached main when i should not have")
	sys.exit(-1)
