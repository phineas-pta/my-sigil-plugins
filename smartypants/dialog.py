# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox, QButtonGroup

# from typing import TYPE_CHECKING # require python 3.5
# if TYPE_CHECKING:
# 	from PySide6.QtWidgets import QCloseEvent
# 	from preferences import JSONPrefs
## additional modules: Sigil > src/Resource_Files/plugin_launchers/python

class PluginApplication(QApplication):
	def __init__(self, args: list) -> None:
		super().__init__(args)
		self.app_results = {} # placeholder to save modified prefs


class guiMain(QDialog):
	def __init__(self, prefs: "JSONPrefs") -> None:
		super().__init__()
		self.setWindowTitle("SmartyPants")
		self.prefs = prefs
		self.checkboxes = {} # placeholder to be built later
		self.setup_ui()

	def setup_ui(self) -> None:
		layout = QVBoxLayout()

		for k, v in self.prefs.items():
			self.checkboxes[k] = QCheckBox(v["details"], self)
			self.checkboxes[k].setChecked(v["enabled"])
			layout.addWidget(self.checkboxes[k])

		output_grp = QButtonGroup(self)
		output_grp.setExclusive(True)
		output_grp.addButton(self.checkboxes["h"])
		output_grp.addButton(self.checkboxes["s"])
		output_grp.addButton(self.checkboxes["u"])

		button_box = QDialogButtonBox(QDialogButtonBox.Ok)
		button_box.accepted.connect(self.close)
		button_box.rejected.connect(self.close)
		layout.addWidget(button_box)

		self.setLayout(layout)
		self.show()

	def closeEvent(self, event: "QCloseEvent") -> None:
		for k in self.prefs.keys():
			self.prefs[k]["enabled"] = self.checkboxes[k].isChecked()
		PluginApplication.instance().app_results = self.prefs # save prefs
		event.accept() # let the window close
