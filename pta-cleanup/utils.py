# -*- coding: utf-8 -*-

import re

def clean_nav(text: str) -> str:
	res = text.replace("<h1>Table of Contents</h1>", "<h1>Mục lục</h1>")
	res = re.sub(r'\s+<nav epub:type="landmarks" id="landmarks" hidden="">\s+<h1>Landmarks</h1>\s+<ol>\s+</ol>\s+</nav>', "", res)
	res = re.sub(r"<li>\s+(<a href.+</a>)\s+</li>", r"<li>\1</li>", res) # too much spacing in table of contents
	return res

_spacing1 = re.compile(r"  +(,\.!\?;)") # too much spacing before punctuation
_spacing2 = re.compile(r"(\w)  +(\w)") # too much spacing between words
_spacing3 = re.compile(r"<p>\s+")
_spacing4 = re.compile(r"\s+</p>")
def clean_spacing(text: str) -> str:
	res = text.replace(' class="sigil_not_in_toc"', "")
	res = _spacing1.sub(r"\1", res)
	res = _spacing2.sub(r"\1 \2", res)
	res = _spacing3.sub("", res)
	res = _spacing4.sub("", res)
	return res
