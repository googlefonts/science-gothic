#FLM: SG Preflight
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2022-2023 	(http://www.kateliev.com)
# (C) Karandash Type Foundry 		(http://www.karandash.eu)
#------------------------------------------------------------

#------------------------------------------------------------
# PROJECT: Science Gothic - Variable Font (Google)
# BY: Thomas Phinney <thomas@thefontdetective.com>
# HOME: https://github.com/tphinney/science-gothic/issues
#------------------------------------------------------------

# No warranties. By using this you agree
# that you use it at your own risk!


# - Dependencies -----------------
from __future__ import absolute_import, print_function
import re
from collections import OrderedDict

import fontlab as fl6
import fontgate as fgt

from typerig.proxy.fl.application.automat import Automat
from typerig.proxy.fl.objects.glyph import pGlyph
from typerig.proxy.fl.objects.font import pFont
from typerig.proxy.fl.objects.node import pNode
from typerig.proxy.fl.objects.contour import pContour
from typerig.core.base.message import *

from PythonQt import QtCore
from typerig.proxy.fl.gui import QtGui
from typerig.proxy.fl.gui.widgets import getProcessGlyphs, fontMarkColors

# - Init ---------------------------
app_name, app_version = 'Science Gothic | Icon Preflight', '2.0'

# - Config -----------------------------
fontMarkColors = fontMarkColors[1:-1] # Removes White and Gray
contour_actions_JSON = ['{"id":"round_to_integer"}', '{"id": "decompose"}', '{"id": "converttosplines"}']

# -- Strings and messages configuration
empty_record = [('Empty Audit Record', [])]
fileFormats = 'Audit Record (*.txt);;'
column_delimiter = ' | '
search_tag = r'.["fl"].[0-9]+'
search_name = '.fill'

# -- Allowed suffixes
glyph_suffix_separator = '.'
suffix_allowed = ['slnt', 'sups', 'loclCAT', 'loclBGR', 'case', 'zero', 'smcp', 'c2sc', 'notdef', 'alt2', 'alt', 'dnom', 'tnum', 'numr', 'sc', 'cyr', 'sinf']
suffix_allowed = [glyph_suffix_separator + item for item in suffix_allowed]

# - Functions --------------------------

# - Classes ----------------------------
class auditGlyph(pGlyph):
	def __init__(self, fg_glyph, fg_font, report_hook):
		super(auditGlyph, self).__init__(fg_glyph, fg_font)
		self.audit_report = report_hook

	# - Helpers -----------------------
	def __write_record(self, condition, error_name, record):
		if condition:
			self.audit_report.setdefault(error_name, []).append((self.name, column_delimiter.join(record)))

	# - Audit Tests -------------------
	# -- Overall test functions
	def run_all_tests(self, reference_layer_name, examine_layers_list):
		audit_list = self.get_all_tests()
		self.run_tests(audit_list, reference_layer_name, examine_layers_list)

	def run_tests(self, audit_list, reference_layer_name, examine_layers_list):
		for audit_test in audit_list:
			try:
				getattr(self, audit_test)(reference_layer_name, examine_layers_list)
			except Exception as err:
				output(2, app_name, 'Glyph: %s;\tAudit: %s;\tException: %s.' %(self.name, audit_test, err))

	def get_all_tests(self):
		return [func for func in dir(self) if callable(getattr(self, func)) and 'audit_' in func]

	# -- Tests follow ------------------
	def audit_glyph_suffix(self, reference_layer_name, examine_layers_list):
		# - Init
		error_name = 'Glyph Name >> Suffix not recognized' 
		error_layers = []

		# - Process
		if glyph_suffix_separator in self.name and glyph_suffix_separator != self.name[0]:
			split_index = self.name.index(glyph_suffix_separator)
			first, rest = self.name[:split_index], self.name[split_index:]

			self.__write_record(rest not in suffix_allowed, error_name, error_layers)

	def audit_glyph_encoding(self, reference_layer_name, examine_layers_list):
		# - Init
		error_name = 'Encoding >> Missing unicode value >> Reference: %s' %reference_layer_name
		error_layers = []
	
		if '.' not in self.name:
			self.__write_record(not len(self.unicodes), error_name, error_layers)

	def audit_anchors_consistent(self, reference_layer_name, examine_layers_list):
		# - Helper
		def fetch_anchor_names(layer_name):
			return tuple(sorted([a.name for a in self.anchors(layer_name)]))

		# - Init
		error_name = 'Anchors >> Not consistent across masters' 
		error_layers = []

		reference_anchors = fetch_anchor_names(reference_layer_name)

		# - Process
		for layer_name in examine_layers_list:
			if reference_anchors != fetch_anchor_names(layer_name):
				error_layers.append(layer_name)

		# - End
		self.__write_record(len(error_layers), error_name, error_layers)

	def audit_layer_non_integer_coordinates(self, reference_layer_name, examine_layers_list):
		error_name = 'Layer >> Non integer coordinates'
		error_layers = []

		# - Process
		test_layers = examine_layers_list + [reference_layer_name]
		
		for layer in test_layers:
			for node in self.nodes(layer):
				if not node.x.is_integer() or not node.y.is_integer(): 
					error_layers.append(layer)
					break

		# - End
		self.__write_record(len(error_layers), error_name, error_layers)

	def audit_layer_compatible(self, reference_layer_name, examine_layers_list, strong_test=True):
		error_name = 'Layer >> Non matching masters'
		error_layers = []

		# - Process
		masters = self.masters()

		for layer in masters:
			for other in masters:
				if not layer.isCompatible(other, strong_test):
					error_layers.append(layer.name)
					break
		# - End
		self.__write_record(len(error_layers), error_name, list(set(error_layers)))

# - Sub widgets ------------------------
class TRWAuditTree(QtGui.QTreeWidget):
	def __init__(self, data=None, headers=None):
		super(TRWAuditTree, self).__init__()
		
		if data is not None: self.setTree(data, headers)
		self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.setAlternatingRowColors(True)

	def setTree(self, data, headers):
		self.blockSignals(True)
		self.clear()
		self.setHeaderLabels(headers)

		# - Insert 
		for key, value in data.items():
			master = QtGui.QTreeWidgetItem(self, [key])

			for sub in value:
				new_item = QtGui.QTreeWidgetItem(master, sub)

		# - Fit data
		for c in range(self.columnCount):
			self.resizeColumnToContents(c)	

		self.expandAll()
		self.blockSignals(False)

class SGPreflight(QtGui.QDialog):
	def __init__(self):
		super(SGPreflight, self).__init__()

		# - Init
		temp = pGlyph()
		self.active_font = pFont()
		layer_names = [layer.name for layer in temp.layers() if '#' not in layer.name]
		
		# - Automat
		self.auto_fl = Automat()

		# - Widgets
		# - Combo Boxes
		self.cmb_select_color = QtGui.QComboBox()
		self.color_codes = {name:value for name, value, discard in fontMarkColors}
		
		for i in range(len(fontMarkColors)):
			self.cmb_select_color.addItem(fontMarkColors[i][0])
			self.cmb_select_color.setItemData(i, QtGui.QColor(fontMarkColors[i][2]), QtCore.Qt.DecorationRole)

		# -- Boxes
		self.box_preflight = QtGui.QGroupBox('Font Preflight:')
		self.box_audit = QtGui.QGroupBox('Font Audit:')

		# -- Progress bar
		self.progress = QtGui.QProgressBar()
		self.progress.setMaximum(100)

		# -- Report Tree
		self.audit_report = OrderedDict(empty_record)
		self.header_names = ['Glyph', 'Layers']
		self.audit_tree = TRWAuditTree(self.audit_report, self.header_names)
		self.audit_tree.selectionModel().selectionChanged.connect(self.auto_preview)
		
		# -- Action Buttons
		# --- Preflight
		self.btn_preflight_info = QtGui.QPushButton('Edit Font Info')
		self.btn_preflight_audit = QtGui.QPushButton('Audit Font')
		self.btn_preflight_clean = QtGui.QPushButton('Cleanup auto layers, unused tags and labels')
		self.btn_preflight_clean_flag = QtGui.QPushButton('Remove glyphs marked with:')
		self.btn_preflight_actions = QtGui.QPushButton('Open Actions')
		self.btn_preflight_do_actions = QtGui.QPushButton('Run Actions')
		self.btn_preflight_save = QtGui.QPushButton('Save Font')
		self.btn_preflight_export = QtGui.QPushButton('Export Font')

		self.btn_preflight_info.clicked.connect(lambda n: self.auto_fl.run('Font_Info'))
		self.btn_preflight_actions.clicked.connect(lambda n: self.auto_fl.run('Action'))
		self.btn_preflight_do_actions.clicked.connect(lambda: self.process_actions())
		self.btn_preflight_save.clicked.connect(lambda n: self.auto_fl.run('SaveFontAs'))
		self.btn_preflight_export.clicked.connect(lambda n: self.auto_fl.run('Export_Fonts'))
		self.btn_preflight_clean.clicked.connect(lambda: self.process_cleanup(mode='auto'))
		self.btn_preflight_clean_flag.clicked.connect(lambda: self.process_cleanup(mode='temp'))

		# --- Audit
		self.btn_audit_reset = QtGui.QPushButton('Reset Record')
		self.btn_audit_select = QtGui.QPushButton('Auto Select Glyphs')
		self.btn_audit_select.setCheckable(True)
		self.btn_audit_select.setChecked(False)
		self.btn_preflight_audit.clicked.connect(self.process_audit)
		self.btn_audit_reset.clicked.connect(self.reset)
		
		# - Build Layout
		lay_main = QtGui.QVBoxLayout()
		lay_preflight = QtGui.QGridLayout()
		lay_preflight.addWidget(QtGui.QLabel('1: Update font info: version.'),	0, 0, 1, 4)
		lay_preflight.addWidget(self.btn_preflight_info,			1, 0, 1, 4)
		lay_preflight.addWidget(QtGui.QLabel('2: Audit Font for known glyph problems.'), 2, 0, 1, 4)
		lay_preflight.addWidget(self.btn_preflight_audit,			3, 0, 1, 4)
		lay_preflight.addWidget(QtGui.QLabel('3: Cleanup Font:'), 	4, 0, 1, 4)
		lay_preflight.addWidget(self.btn_preflight_clean, 			5, 0, 1, 4)
		lay_preflight.addWidget(self.btn_preflight_clean_flag, 		7, 0, 1, 2)
		lay_preflight.addWidget(self.cmb_select_color, 				7, 2, 1, 2)
		lay_preflight.addWidget(QtGui.QLabel('4: All glyphs/masters: Apply rounding; Decompose; Convert to TT curves.'), 8, 0, 1, 4)
		lay_preflight.addWidget(self.btn_preflight_actions,			9, 0, 1, 2)
		lay_preflight.addWidget(self.btn_preflight_do_actions,		9, 2, 1, 2)
		lay_preflight.addWidget(QtGui.QLabel('5: Save your work.'), 10, 0, 1, 4)
		lay_preflight.addWidget(self.btn_preflight_save, 			11, 0, 1, 4)
		lay_preflight.addWidget(QtGui.QLabel('6: Export fonts.'),	12, 0, 1, 4)
		lay_preflight.addWidget(self.btn_preflight_export,			13, 0, 1, 4)
		self.box_preflight.setLayout(lay_preflight)

		lay_audit = QtGui.QGridLayout()
		lay_audit.addWidget(self.btn_audit_select, 				0,  6,  1, 3)
		lay_audit.addWidget(self.btn_audit_reset, 				0,  9,  1, 3)
		lay_audit.addWidget(QtGui.QLabel('Audit Report:'),	 	1,  6,  1, 6)
		lay_audit.addWidget(self.audit_tree, 					2,  6, 20, 6)
		self.box_audit.setLayout(lay_audit)

		lay_split = QtGui.QHBoxLayout()
		lay_split.addWidget(self.box_preflight)
		lay_split.addWidget(self.box_audit)
		lay_main.addLayout(lay_split)
		lay_main.addWidget(self.progress)
		self.setLayout(lay_main)


		# - Finish
		self.setMinimumSize(300, self.sizeHint.height())

	# -- Procedures --------------------------
	def reset(self):
		self.audit_tree.clear()
		self.audit_report = {}
		self.active_font = pFont()
		self.audit_report = OrderedDict(empty_record)
		self.audit_tree.setTree(self.audit_report, self.header_names)

	def auto_preview(self):
		if self.btn_audit_select.isChecked():
			self.active_font.unselectAll()
			selection = [item.text(0) for item in self.audit_tree.selectedItems()]
			self.active_font.selectGlyphs(selection)

	def process_audit(self):
		# - Init
		self.audit_report = OrderedDict()
		reference_layer_name = 'Regular'
		process_layers = self.active_font.masters()

		# - Run Tests
		audit_glyphs = self.active_font.glyphs()
		
		# - Set progress bar
		all_glyph_counter = 0
		self.progress.setValue(all_glyph_counter)
		glyph_count = len(audit_glyphs)
		
		for fg_glyph in audit_glyphs:
			# - Audit
			audit_glyph = auditGlyph(fg_glyph, self.active_font.fg, self.audit_report)
			audit_glyph.run_all_tests(reference_layer_name, process_layers)
			
			# - Set progress
			all_glyph_counter += 1
			current_progress = all_glyph_counter*100/glyph_count
			self.progress.setValue(current_progress)
			QtGui.QApplication.processEvents()

		self.audit_report = OrderedDict([('{} ({})'.format(key, len(value)), value) for key, value in self.audit_report.items()])
		self.audit_tree.setTree(self.audit_report, self.header_names)
		self.audit_tree.collapseAll()
		
		output(0, app_name, 'Font: %s; Audit report Finished!' %self.active_font.name)
		self.progress.setValue(0)

	def process_cleanup(self, mode):
		# - Init
		process_layers = self.active_font.masters()
		process_glyphs = self.active_font.glyphs()
		temp_glyph_mark = self.color_codes[self.cmb_select_color.currentText]
		remove_glyphs = []
		
		# - Set progress bar
		all_glyph_counter = 0
		self.progress.setValue(all_glyph_counter)
		glyph_count = len(process_glyphs)
		
		for fg_glyph in process_glyphs:
			# - Init
			glyph = pGlyph(fg_glyph, self.active_font.fg)
			
			# - Remove auto layers, tags and labels
			if mode == 'auto':
				# - Cleanup
				# -- Remove Font Notes
				glyph.fl.note = ''

				# -- Remove Auto Layers
				for layer_name in process_layers:
					if glyph.layer(layer_name).autoLayer:
						glyph.layer(layer_name).autoLayer = False
				
				# -- Remove unnecessary tags
				if search_name in glyph.name and glyph.name.count(glyph_suffix_separator) > 1:
					new_tags = []
					
					for tag in glyph.tags:
						match = re.search(search_tag, tag)
						
						if not bool(match):
							new_tags.append(tag)

					glyph.tags = new_tags

				# -- Remove all non-master layers
				remove_layers = [layer for layer in glyph.layers() if layer.name not in process_layers]
				
				for layer_to_delete in remove_layers:
					glyph.fl.removeLayer(layer_to_delete)

				# -- Remove color flags
				glyph.setMark(0)

			# - Remove temporary glyphs with some user defined mark
			if mode == 'temp': 
				if glyph.mark == temp_glyph_mark:
					remove_glyphs.append(glyph.name)
			
			# - Set progress
			all_glyph_counter += 1
			current_progress = all_glyph_counter*100/glyph_count
			self.progress.setValue(current_progress)

		# - Remove glyphs from font
		self.active_font.fg.clearMaps()
		success = 0

		if (mode == 'temp' or mode == 'unic') and len(remove_glyphs):
			for glyph_name in reversed(remove_glyphs):
				ret = self.active_font.fg.removeGlyph(glyph_name)
				if ret: success += 1

			output(0, app_name, 'Font: %s; Glyphs to remove: %s; Success: %s' %(self.active_font.name, len(remove_glyphs), success))

		output(0, app_name, 'Font: %s; Cleanup Finished!' %self.active_font.name)
		self.active_font.update()
		self.progress.setValue(0)

	def process_actions(self):
		# - Init
		process_layers = self.active_font.masters()
		process_glyphs = self.active_font.glyphs(extend=fl6.flGlyph)
		
		# - Set progress bar
		all_glyph_counter = 50
		self.progress.setValue(all_glyph_counter)
		glyph_count = len(process_glyphs)

		output(1, app_name, 'Performing global font actions! Please wait the operation to be over!')
				
		# - Perform flPackage action
		self.active_font.fl.runActions(process_glyphs, contour_actions_JSON, 2, True) # 0 - Active, 1 - Selection/window, 2 - All layers/masters
			
		# - Set progress bar
		all_glyph_counter = 0
		self.progress.setValue(all_glyph_counter)
		glyph_count = len(process_glyphs)

		output(0, app_name, 'Font: {};'.format(self.active_font.name))
		#self.active_font.update()

# - Run ----------------------
Preflight = SGPreflight()
Preflight.setWindowTitle('%s %s' %(app_name, app_version))
Preflight.setGeometry(100, 100, 900, 600)
#Preflight.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # Always on top!!

Preflight.show()
