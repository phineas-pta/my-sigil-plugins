# -*- coding: utf-8 -*-

import sys

# from typing import TYPE_CHECKING # require python 3.5
# if TYPE_CHECKING:
# 	from bookcontainer import BookContainer
## additional modules: Sigil > src/Resource_Files/plugin_launchers/python

from config import DEFAULT_PREFERENCES, validate_prefs, combine_prefs
from dialog import guiMain, PluginApplication
from smartypants import smartypants


def run(bk: "BookContainer") -> int:
	prefs = bk.getPrefs()
	if len(prefs) == 0: # 1st run
		# prefs = DEFAULT_PREFERENCES # DO NOT DO THIS because prefs is not a normal dict
		for k, v in DEFAULT_PREFERENCES.items():
			prefs[k] = v

	app = PluginApplication(sys.argv)
	w = guiMain(prefs)
	app.exec()
	new_prefs = app.app_results

	msg = validate_prefs(new_prefs)
	if msg != "":
		raise ValueError(msg)
	bk.savePrefs(new_prefs)

	attr = combine_prefs(new_prefs)
	for fileID, _ in bk.text_iter():
		bk.writefile(id=fileID, data=smartypants(text=bk.readfile(fileID), attr=attr))

	return 0


if __name__ == "__main__":
	print("i reached main when i should not have")
	sys.exit(-1)
