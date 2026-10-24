# -*- coding: utf-8 -*-

from smartypants import _Attr

DEFAULT_PREFERENCES = {
	"B": {
		"details": "double and single backticks to curly ones",
		"value": _Attr.B,
		"enabled": False,
	},
	"q": {
		"details": "double and single quotes to curly ones",
		"value": _Attr.q,
		"enabled": True,
	},
	"D": {
		"details": "double dashes to en-dashes, triple quotes to em-dashes",
		"value": _Attr.D,
		"enabled": False,
	},
	"i": {
		"details": "double dashes to em-dashes, triple quotes to en-dashes",
		"value": _Attr.i,
		"enabled": False,
	},
	"e": {
		"details": "triple full-stop to ellipses",
		"value": _Attr.e,
		"enabled": True,
	},
	"h": {
		"details": "output html entities instead of numeric character references",
		"value": _Attr.h,
		"enabled": False,
	},
	"s": {
		"details": "output ascii equivalents instead of numeric character references",
		"value": _Attr.s,
		"enabled": False,
	},
	"u": {
		"details": "output unicode characters instead of numeric character references",
		"value": _Attr.u,
		"enabled": True,
	},
	# i left out "b", "d", "w" because it seems duplicated
}

def validate_prefs(prefs: dict) -> str:
	if prefs["D"]["enabled"] and prefs["i"]["enabled"]:
		return "choose only 1 option for dashes"
	elif prefs["h"]["enabled"] + prefs["s"]["enabled"] + prefs["u"]["enabled"] > True:
		return "choose only 1 option for output"
	else:
		return ""

def combine_prefs(prefs: dict) -> int:
	res = _Attr.set0
	for v in prefs.values():
		if v["enabled"]:
			res |= v["value"]
	return res
