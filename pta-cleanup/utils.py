# -*- coding: utf-8 -*-

import re

def clean_nav(text: str) -> str:
	res = text.replace("<h1>Table of Contents</h1>", "<h1>Mục lục</h1>")
	res = re.sub(r'\s+<nav epub:type="landmarks" id="landmarks" hidden="">\s+<h1>Landmarks</h1>\s+<ol>\s+</ol>\s+</nav>', "", res)
	res = re.sub(r"<li>\s+(<a href.+</a>)\s+</li>", r"<li>\1</li>", res) # too much spacing in table of contents
	return res


_PATTERNS = { # format: "replacement": "pattern"
	r"\1": re.compile(r"  +(,\.!\?;)"), # too much spacing before punctuation
	r"\1 \2": re.compile(r"(\w)  +(\w)"), # too much spacing between words
	"<p>": re.compile(r"<p>\s+"),
	"</p>": re.compile(r"\s+</p>"),
	"(": re.compile(r"\(\s+"),
	")": re.compile(r"\s+\)"),
}

def clean_spacing(text: str) -> str:
	res = text.replace(' class="sigil_not_in_toc"', "")
	for repl, patt in _PATTERNS.items():
		res = patt.sub(repl, res)
	return res
