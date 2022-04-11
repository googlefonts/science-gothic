#FLM: SG Audit
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2022 	(http://www.kateliev.com)
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
import sys, datetime, math
from collections import OrderedDict
from itertools import product

import fontlab as fl6
import fontgate as fgt

from typerig.proxy.fl.objects.glyph import pGlyph
from typerig.proxy.fl.objects.font import pFont
from typerig.proxy.fl.objects.node import eNode
from typerig.proxy.fl.objects.contour import pContour

from typerig.core.objects.line import Line
from typerig.core.base.message import *

from PythonQt import QtCore
from typerig.proxy.fl.gui import QtGui
from typerig.proxy.fl.gui.widgets import getProcessGlyphs, TRCollapsibleBox

# - Init ---------------------------
global pLayers
global pMode
pLayers = None
pMode = 0
app_name, app_version = 'SG | Audit', '1.4'

# - Config -----------------------------
o = 'on'
c = 'curve'

# -- Allowed suffixes
glyph_suffix_separator = '.'
suffix_allowed = ['slnt', 'sups', 'loclCAT', 'case', 'zero', 'smcp', 'c2sc', 'notdef', 'alt2', 'alt', 'dnom', 'tnum', 'numr', 'sc', 'cyr', 'sinf']
suffix_allowed = [glyph_suffix_separator + item for item in suffix_allowed]

# -- Strings and messages configuration
empty_record = [('Empty Audit Record', [])]
fileFormats = 'Audit Record (*.txt);;'
column_delimiter = ' | '

# - Functions --------------------------
def tuple_delta(a, b, delta):
	if len(a) == len(b):
		for i in range(len(a)):
			if abs(int(a[i] - b[i])) > int(delta):
				return True
	else:
		raise ValueError('ERROR:\tNon matching dimensions for input tuples!')

	return False

def inter_layer_diff(glyph, layers):
	'''Return the maximum deviation of a node between given layers'''

	inter_layer_data = []

	for layer_name in layers:
		inter_layer_data.append((layer_name, [n.asCoord() for n in glyph.nodes(layer_name, extend=eNode)]))
	
	inter_layer_distances = []
	inter_layer_data.append(inter_layer_data[0])
	
	for i in range(len(inter_layer_data) - 1):
		current_distances = []
		layer_name_1, layer_nodes_1 = inter_layer_data[i]
		layer_name_2, layer_nodes_2 = inter_layer_data[i+1]

		for point_pair in zip(layer_nodes_1, layer_nodes_2):
			new_line = Line(*point_pair)
			current_distances.append(new_line.length)
		
		max_distance = max(current_distances)
		inter_layer_distances.append(((layer_name_1, layer_name_2), (current_distances.index(max_distance), max_distance)))
		
	return inter_layer_distances

def broken_smooth(glyph, layer_name, delta=1.):
	'''Find broken smooth nodes that have one or more handles not aligned'''
	for node in glyph.nodes(layer_name, extend=eNode):
		if node.smooth and (not node.getNext().isOn() or not node.getPrev().isOn()):
			prev_line = node.getPrevOffLine()
			next_line = node.getNextOffLine()

			if prev_line.length < 1: continue
			if next_line.length < 1: continue

			if abs(prev_line.angle - next_line.angle) > delta:
				return True

	return False

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

	def audit_contour_start(self, reference_layer_name, examine_layers_list):
		# - Test Helpers
		def quadrant(contour, quadrants):
			xMin, yMin, xMax, yMax = contour.bounds
			contour_center = ((xMin + xMax)/2, (yMin + yMax)/2)
			contour_start = (contour.first.x, contour.first.y)
			start_line = Line(contour_center, contour_start)
			start_angle = start_line.angle
			start_angle = start_angle if start_angle > 0 else 360 + start_angle

			for q in range(len(quadrants)):
				if int(start_angle) <= quadrants[q]: 
					return q # return quadrant

		def near_bounds(contour):
			xMin, yMin, xMax, yMax = contour.bounds
			contour_start = (contour.first.x, contour.first.y)

			xMid = (xMin + xMax)/2
			yMid = (yMin + yMax)/2
			test_tuples = list(product((xMin, xMid, xMax), (yMin, yMid, yMax)))
			#test_tuples.pop(test_tuples.index((xMid, yMid)))
			test_lengths = [Line(node, contour_start).length for node in test_tuples]
			test_score = [item[0] for item in sorted(enumerate(test_lengths), key=lambda n: n[1])]
			return test_score

		def near_bounds_score(reference, test):
			score = 0
			len_reference = len(reference)
			if len_reference == len(test):
				for i in range(len_reference):
					if reference[i] == test[i]:
						score += len_reference - i
				return score >= len_reference
			return False


		# - Init
		error_name = 'Contour >> Possible non matching start point'
		error_layers = []
		test_layers = examine_layers_list
		
		# -- Set Quadrant test
		# -- Test if the start node of every layer falls in the same quadrant as the reference layer.
		# -- Origin is set at the contour geometric center. For quadrants are rotated by chosen degree
		# -- to avoid 90 degree matches (mostly in symmetrical shapes like circles)
		rotate = 45
		degree_step = 90
		quadrants = range(rotate + degree_step, 360 + rotate + degree_step, degree_step)

		reference_quad = []
		check_contours = [] # list of base contours that have area > 0
		reference_contours = self.contours(reference_layer_name)

		# -- Set Near bounds test
		# -- Create a set of 9 nodes, representing the four coordinates forming the contours BBox
		# -- and the middle of the sides between them. Create a set of vectors from each node to the
		# -- the current start node. Enumerate them, then sort by length. Comparing the results of each
		# -- layers length score to the reference, should render pretty much the same results if they match.
		reference_score = []
		
		for cid in range(len(reference_contours)):
			current_contour = reference_contours[cid]
			if current_contour.convertToFgContour(current_contour.transform).area() != 0:
				reference_quad.append(quadrant(current_contour, quadrants))
				reference_score.append(near_bounds(current_contour))
				check_contours.append(cid)

		# - Process
		for layer_name in test_layers:
			layer_contours = self.contours(layer_name)
			layer_quad = [quadrant(layer_contours[cid], quadrants) for cid in check_contours]
			if reference_quad != layer_quad:
				layer_score = [near_bounds(layer_contours[cid]) for cid in check_contours]
				
				for ref, test in zip(reference_score, layer_score):
					if not near_bounds_score(ref, test):
						error_layers.append(layer_name)
		
		# - End
		self.__write_record(len(error_layers), error_name, error_layers)

	def audit_contour_winding(self, reference_layer_name, examine_layers_list):
		error_name = 'Contour >> Non matching winding direction'
		error_layers = []

		# - Process
		test_layers = examine_layers_list
		reference_winding = [contour.clockwise for contour in self.contours(reference_layer_name)]
		glyph_layer_winding = []

		for layer in test_layers:
			layer_winding = [contour.clockwise for contour in self.contours(layer)]
			if reference_winding != layer_winding:
				error_layers.append(layer)
		
		# - End
		self.__write_record(len(error_layers), error_name, error_layers)

	def audit_layer_winding(self, reference_layer_name, examine_layers_list):
		error_name = 'Layer >> Contour direction is not PS'
		error_layers = []

		# - Process
		test_layers = examine_layers_list + [reference_layer_name]
		for layer in test_layers:
			try:
				layer_contour_area = [(abs(contour.area), contour.area < 0) for contour in self.contours(layer, extend=pContour)]
				if len(layer_contour_area) and max(layer_contour_area, key=lambda t:t[0])[1]:
					error_layers.append(layer)
			except AttributeError:
				pass

		# - End
		if len(set(test_layers)) == len(set(error_layers)):
			self.__write_record(len(error_layers), error_name, error_layers)

	def audit_layer_winding_score(self, reference_layer_name, examine_layers_list):
		error_name = 'Layer >> Contour direction is not PS (Bounds Area Score)'
		error_layers = []

		# - Process
		test_layers = examine_layers_list + [reference_layer_name]
		for layer in test_layers:
			try:
				layer_contour_area = [(contour.width*contour.height, contour.isCCW()) for contour in self.contours(layer, extend=pContour)]
				if len(layer_contour_area) and not max(layer_contour_area, key=lambda t:t[0])[1]:
					error_layers.append(layer)
			except AttributeError:
				pass

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

	def audit_layer_compatible_by_node_type(self, reference_layer_name, examine_layers_list, strong_test=True):
		error_name = 'Layer >> Non matching masters (Type Test)'
		error_layers = []

		# - Process
		reference = [node.type for node in self.nodes(reference_layer_name)]

		for layer_name in examine_layers_list:
			current_layer = [node.type for node in self.nodes(layer_name)]
				
			if current_layer != reference:
				error_layers.append(layer_name)
				break
		# - End
		self.__write_record(len(error_layers), error_name, list(set(error_layers)))


	def audit_outline_line_semi(self, reference_layer_name, examine_layers_list, error_delta=2):
		key_line_horizontal = 'Line >> Semi Horizontal'
		key_line_vertical = 'Line >> Semi Vertical'
		error_line_horizontal, error_line_vertical = [], []

		test_layers = examine_layers_list + [reference_layer_name]

		for layer in test_layers:
			for node in self.nodes(layer, extend=eNode):
				if node.type == o and node.getNext().type == o:
					examine_angle = math.degrees(node.angleToNext()) % 180
					if 0 < examine_angle <= error_delta or 180 - error_delta <= examine_angle < 180 :
						error_line_horizontal.append(layer)

					if 90 - error_delta <= examine_angle <= 90 + error_delta and examine_angle != 90:
						error_line_vertical.append(layer)

		self.__write_record(len(error_line_horizontal), key_line_horizontal, list(set(error_line_horizontal)))
		self.__write_record(len(error_line_vertical), key_line_vertical, list(set(error_line_vertical)))

	def audit_outline_broken_smooth(self, reference_layer_name, examine_layers_list, error_delta=10.):
		key_broken_smooth = 'Outline >> Broken smooth connections'
		error_broken_smooth = []

		test_layers = examine_layers_list + [reference_layer_name]

		for layer in test_layers:
			if broken_smooth(self, layer, error_delta):
				error_broken_smooth.append(layer)

		self.__write_record(len(error_broken_smooth), key_broken_smooth, list(set(error_broken_smooth)))

# - Sub widgets ------------------------
class CheckableComboBox(QtGui.QComboBox):
	def __init__(self):
		super(CheckableComboBox, self).__init__()
		self.view().pressed.connect(self.handleItemPressed)
		self.setModel(QtGui.QStandardItemModel(self))
		self.checked_items = []

	def handleItemPressed(self, index):
		item = self.model().itemFromIndex(index)
		if item.checkState() == QtCore.Qt.Checked:
			item.setCheckState(QtCore.Qt.Unchecked)
			if item.text() in self.checked_items:
				self.checked_items.pop(self.checked_items.index(item.text()))
		else:
			item.setCheckState(QtCore.Qt.Checked)
			self.checked_items.append(item.text())
			
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
				new_item.setCheckState(0, QtCore.Qt.Checked) 

		# - Fit data
		for c in range(self.columnCount):
			self.resizeColumnToContents(c)	

		self.expandAll()
		self.blockSignals(False)

	def getTree(self):
		returnDict = OrderedDict()
		root = self.invisibleRootItem()

		for i in range(root.childCount()):
			item = root.child(i)

			returnDict[item.text(0)] = [[item.child(n).text(c) for c in range(item.child(n).columnCount())] for n in range(item.childCount()) if item.child(n).checkState(0) == QtCore.Qt.Checked]
		
		return returnDict

class tool_tab(QtGui.QWidget):
	def __init__(self):
		super(tool_tab, self).__init__()

		# - Init
		temp = pGlyph()
		self.active_font = pFont()
		layer_names = [layer.name for layer in temp.layers() if '#' not in layer.name]
		
		# - Widgets
		# -- Progress bar
		self.progress = QtGui.QProgressBar()
		self.progress.setMaximum(100)

		# -- Report Tree
		self.audit_report = OrderedDict(empty_record)
		self.header_names = ['Glyph', 'Layers']
		self.audit_tree = TRWAuditTree(self.audit_report, self.header_names)
		self.audit_tree.selectionModel().selectionChanged.connect(self.auto_preview)
		
		# -- Test List
		temp_audit_glyph = auditGlyph(temp.fg, self.active_font.fg, self.audit_report)
		audit_tests = [test.replace('_', ' ').replace('audit', '').title() for test in temp_audit_glyph.get_all_tests()]

		self.audit_list = QtGui.QListWidget()
		self.audit_list.setAlternatingRowColors(True)
		self.audit_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.audit_list.addItems(audit_tests)

		# -- Audit Options
		self.cmb_layers = CheckableComboBox()
		self.cmb_layers.addItems(['All Masters'] + layer_names)
		
		self.cmb_reference = QtGui.QComboBox()
		self.cmb_reference.addItems(layer_names)
		
		if 'Regular' in layer_names:
			self.cmb_reference.setCurrentIndex(layer_names.index('Regular'))

		# -- Action Buttons
		self.btn_audit_run = QtGui.QPushButton('Process Entire Font')
		self.btn_audit_glyphs = QtGui.QPushButton('Process Glyph Selection')
		self.btn_audit_tests = QtGui.QPushButton('Selected tests only')
		self.btn_audit_reset = QtGui.QPushButton('Reset Record')
		self.btn_audit_save = QtGui.QPushButton('Save Record')
		self.btn_audit_select = QtGui.QPushButton('Auto Select Glyphs')
		self.btn_select_cheked = QtGui.QPushButton('Select Checked Glyphs')
		
		self.btn_audit_select.setCheckable(True)
		self.btn_audit_tests.setCheckable(True)
		self.btn_audit_select.setChecked(False)
		self.btn_audit_tests.setChecked(True)

		self.btn_audit_run.clicked.connect(lambda: self.process_audit(False))
		self.btn_audit_glyphs.clicked.connect(lambda: self.process_audit(True))
		self.btn_select_cheked.clicked.connect(lambda: self.selected_preview())

		self.btn_audit_reset.clicked.connect(self.reset)
		self.btn_audit_save.clicked.connect(self.save_audit)
		
		# - Build Layout
		lay_main = QtGui.QVBoxLayout()
		lay_audit = QtGui.QGridLayout()
		lay_audit.addWidget(self.btn_audit_tests, 				 0,  0,  1,  2)
		lay_audit.addWidget(self.btn_audit_select, 				 0,  2,  1,  2)
		lay_audit.addWidget(self.btn_select_cheked, 			 0,  4,  1,  2)
		
		lay_audit.addWidget(self.btn_audit_save, 				 0,  6,  1,  2)
		lay_audit.addWidget(self.btn_audit_reset, 				 0,  8,  1,  2)
		lay_audit.addWidget(self.btn_audit_glyphs, 				 0,  10,  1, 2) 
		lay_audit.addWidget(self.btn_audit_run, 				 0, 12,  1,  4) 
		lay_audit.addWidget(QtGui.QLabel('Audit Tests:'),		 1,  0,  1,  4)
		lay_audit.addWidget(self.audit_list, 					 2,  0, 21,  4) 
		lay_audit.addWidget(QtGui.QLabel('Audit Report:'),		 1,  4,  1, 12)
		lay_audit.addWidget(self.audit_tree, 					 2,  4, 23, 12)
		lay_audit.addWidget(QtGui.QLabel('Reference:'),			23,  0,  1,  1)
		lay_audit.addWidget(self.cmb_reference, 				23,  1,  1,  3)
		lay_audit.addWidget(QtGui.QLabel('Audit on:'),			24,  0,  1,  1)
		lay_audit.addWidget(self.cmb_layers, 					24,  1,  1,  3)
		lay_audit.addWidget(self.progress, 						25,  0,  1,  16)

		# - Finish
		lay_main.addLayout(lay_audit)
		self.setLayout(lay_main)
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

	def selected_preview(self):
		export_report = self.audit_tree.getTree()
		selected_glyphs = set()
		
		for key, value in export_report.items():
			for item in value:
				selected_glyphs.add(item[0])
		
		self.active_font.unselectAll()
		self.active_font.selectGlyphs(list(selected_glyphs))

	def save_audit(self):
		export_report = self.audit_tree.getTree()
		fontPath = os.path.split(self.active_font.fg.path)[0]
		fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Audit Record', fontPath, fileFormats)

		if fname != None:
			with open(fname, 'w') as exportFile:
				for key, value in export_report.items():
					export_glyph_names = '/'.join([item[0] for item in value]) 

					write_string = '\n{border}\n# {title}\n{border}\n'.format(border='#'*10, title=key + '/(%s)' %len(value))
					write_string += '\n'.join(['/{glyph}{delimit}{result};'.format(glyph=item[0], delimit=column_delimiter, result=item[1]) for item in value]) + '\n'
					write_string += '\n# {title} Affected glyphs string:\n/'.format(title=key)
					write_string += export_glyph_names

					exportFile.writelines(write_string)

				output(7, app_name, 'Font: %s; Audit report saved to: %s.' %(self.active_font.name, fname))
		
	def process_audit(self, selected=False):
		# - Init
		self.audit_report = OrderedDict()
		reference_layer_name = self.cmb_reference.currentText
		
		if self.cmb_layers.currentText == 'All Masters':
			all_masters = self.active_font.masters()
			
			if reference_layer_name in all_masters:
				all_masters.pop(all_masters.index(reference_layer_name))
			
			process_layers = all_masters
		
		else:
			selected_layers = self.cmb_layers.checked_items
			
			if reference_layer_name in selected_layers:
				selected_layers.pop(selected_layers.index(reference_layer_name))
			
			process_layers = selected_layers

		output(1, app_name, 'Font: %s; Audit report started!' %self.active_font.name)

		# - Set progress bar
		all_glyph_counter = 0
		self.progress.setValue(all_glyph_counter)

		# - Run Tests
		probe_glyphs = self.active_font.glyphs() if not selected else self.active_font.selectedGlyphs()
		glyph_count = len(probe_glyphs)

		for fg_glyph in probe_glyphs:
			audit_glyph = auditGlyph(fg_glyph, self.active_font.fg, self.audit_report)
			
			if self.btn_audit_tests.isChecked():
				selected_tests = [('audit' + item.text()).replace(' ', '_').lower() for item in self.audit_list.selectedItems()]
				audit_glyph.run_tests(selected_tests, reference_layer_name, process_layers)
			else:
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

# - Test ----------------------
if __name__ == '__main__':
	test = tool_tab()
	test.setWindowTitle('%s %s' %(app_name, app_version))
	test.setGeometry(100, 100, 900, 600)
	test.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # Always on top!!
	
	test.show()