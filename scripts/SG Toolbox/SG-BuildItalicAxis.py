#FLM: Font: Build Italic Axis (TypeRig)
# ----------------------------------------
# (C) Vassil Kateliev, 2019 (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
#-----------------------------------------
# www.typerig.com

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------
import fontlab as fl6
from PythonQt import QtCore, QtGui

import os
from math import radians
from itertools import product
from collections import OrderedDict

from typerig.proxy import pFont, pGlyph
from typerig.brain import fontFamilly, linAxis, geoAxis, linspread, geospread

# - Init --------------------------------
app_version = '1.2'
app_name = 'Build Italic Axis'
fileFormats = ['FontLab Encoding File (*.enc)', 'Text File (*.txt)']

# -- Transformation parameters
italic_transform_angle = 10
italic_transform_shift = -20

# -- Master & Axis related
italic_axis_names = [('Italic', 'ital', 'it'), ('Slant', 'slnt', 'sl')] #Registered: https://docs.microsoft.com/en-us/typography/opentype/spec/dvaraxisreg
italic_axis_names_T = map(list, zip(*italic_axis_names))

# -- GUI related
table_dict = {1:OrderedDict([('Master Name', None), ('Angle', None), ('Shift', None)])}
spinbox_range = (-99, 99)

# - Widgets --------------------------------
class WTableView(QtGui.QTableWidget):
	def __init__(self, data):
		super(WTableView, self).__init__()
		
		# - Init
		self.setColumnCount(max(map(len, data.values())))
		self.setRowCount(len(data.keys()))

		# - Set 
		self.setTable(data)		
		self.itemChanged.connect(self.markChange)

		# - Styling
		self.horizontalHeader().setStretchLastSection(True)
		self.setAlternatingRowColors(True)
		self.setShowGrid(False)
		#self.resizeColumnsToContents()
		self.resizeRowsToContents()

	def setTable(self, data, reset=False):
		name_row, name_column = [], []
		self.blockSignals(True)

		self.setColumnCount(max(map(len, data.values())))
		self.setRowCount(len(data.keys()))

		# - Populate
		for n, layer in enumerate(sorted(data.keys())):
			name_row.append(layer)

			for m, key in enumerate(data[layer].keys()):
				name_column.append(key)
				newitem = QtGui.QTableWidgetItem(str(data[layer][key]))
				self.setItem(n, m, newitem)
				
		self.setHorizontalHeaderLabels(name_column)
		self.setVerticalHeaderLabels(name_row)
		self.blockSignals(False)

	def getTable(self):
		returnDict = {}
		for row in range(self.rowCount):
			returnDict[self.verticalHeaderItem(row).text()] = OrderedDict([(self.horizontalHeaderItem(col).text(), self.item(row, col).text()) for col in range(self.columnCount)])

		return returnDict

	def markChange(self, item):
		item.setBackground(QtGui.QColor('powderblue'))

# - Dialogs --------------------------------
class dlg_BuildAxis(QtGui.QDialog):
	def __init__(self):
		super(dlg_BuildAxis, self).__init__()
	
		# - Init
		self.active_font = pFont()
		self.exclude_list = []
		
		# - Widgets
		self.cmb_master_name = QtGui.QComboBox()
		self.cmb_axis_name = QtGui.QComboBox()
		self.cmb_axis_short = QtGui.QComboBox()
		self.cmb_axis_tag = QtGui.QComboBox()
		
		self.spb_italic_angle = QtGui.QSpinBox()
		self.spb_italic_shift = QtGui.QSpinBox()
		
		self.tab_masters = WTableView(table_dict)

		self.btn_exclude_file = QtGui.QPushButton('Select glyph exclude list')	
		self.btn_populate = QtGui.QPushButton('Populate Master Table')
		self.btn_execute = QtGui.QPushButton('Execute')

		self.cmb_master_name.setEditable(True)
		self.cmb_axis_name.setEditable(True)
		self.cmb_axis_short.setEditable(True)
		self.cmb_axis_tag.setEditable(True)

		self.spb_italic_angle.setMinimum(spinbox_range[0])
		self.spb_italic_shift.setMinimum(spinbox_range[0])

		self.spb_italic_angle.setMaximum(spinbox_range[1])
		self.spb_italic_shift.setMaximum(spinbox_range[1])
		
		self.cmb_master_name.addItems(italic_axis_names_T[0])
		self.cmb_axis_name.addItems(italic_axis_names_T[0])
		self.cmb_axis_short.addItems(italic_axis_names_T[1])
		self.cmb_axis_tag.addItems(italic_axis_names_T[2])

		self.spb_italic_angle.setValue(italic_transform_angle)
		self.spb_italic_shift.setValue(italic_transform_shift)

				
		self.cmb_axis_name.currentIndexChanged.connect(self.change_axis_name)	
		self.btn_exclude_file.clicked.connect(self.load_exclude_list)
		self.btn_populate.clicked.connect(self.table_populate)
		self.btn_execute.clicked.connect(self.table_execute)
		
		# - Build layouts 
		layoutV = QtGui.QGridLayout() 
		layoutV.addWidget(QtGui.QLabel('Build Axis:'),		0, 0, 1, 9, QtCore.Qt.AlignBottom)
		layoutV.addWidget(QtGui.QLabel('Name:'),			1, 0, 1, 1)
		layoutV.addWidget(self.cmb_axis_name,				1, 1, 1, 2)
		layoutV.addWidget(QtGui.QLabel('Short:'),			1, 3, 1, 1)
		layoutV.addWidget(self.cmb_axis_short,				1, 4, 1, 2)
		layoutV.addWidget(QtGui.QLabel('Tag:'),				1, 6, 1, 1)
		layoutV.addWidget(self.cmb_axis_tag,				1, 7, 1, 2)
		layoutV.addWidget(QtGui.QLabel('Masters:'),			2, 0, 1, 2, QtCore.Qt.AlignBottom)
		layoutV.addWidget(QtGui.QLabel('Transformation:'),	2, 2, 1, 3, QtCore.Qt.AlignBottom)
		layoutV.addWidget(QtGui.QLabel('Suffix:'),			3, 0, 1, 1)
		layoutV.addWidget(self.cmb_master_name,				3, 1, 1, 2)
		layoutV.addWidget(QtGui.QLabel('Angle:'),			3, 3, 1, 1)
		layoutV.addWidget(self.spb_italic_angle,			3, 4, 1, 2)
		layoutV.addWidget(QtGui.QLabel('Shift:'),			3, 6, 1, 1)
		layoutV.addWidget(self.spb_italic_shift,			3, 7, 1, 2)
		layoutV.addWidget(QtGui.QLabel('Glyph processing:'),5, 0, 1, 9, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_exclude_file, 			6, 0, 1, 9)
		layoutV.addWidget(QtGui.QLabel('Overview:'),		7, 0, 1, 9, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_populate, 				8, 0, 1, 9)
		layoutV.addWidget(self.tab_masters, 				9, 0, 25,9)
		layoutV.addWidget(self.btn_execute, 				34, 0, 1,9)

		# - Set Widget
		self.setLayout(layoutV)
		self.setWindowTitle('%s %s' %(app_name, app_version))
		self.setGeometry(300, 300, 400, 600)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # Always on top!!
		self.show()

	def change_axis_name(self):
		self.cmb_master_name.setCurrentIndex(self.cmb_axis_name.currentIndex)
		self.cmb_axis_short.setCurrentIndex(self.cmb_axis_name.currentIndex)
		self.cmb_axis_tag.setCurrentIndex(self.cmb_axis_name.currentIndex)

	def table_populate(self):
		self.tab_masters.setTable({n:OrderedDict([('Master Name', '%s %s' %(master, self.cmb_master_name.currentText)), ('Angle', self.spb_italic_angle.value), ('Shift', self.spb_italic_shift.value)]) for n, master in enumerate(self.active_font.pMasters.names)})
		self.tab_masters.resizeColumnsToContents()

	def load_exclude_list(self):
		fontPath = os.path.split(self.active_font.fg.path)[0]
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Load glyph exclude list', fontPath, ';;'.join(fileFormats))
		
		if fname != None:
			with open(fname, 'r') as importFile:
				for curline in importFile:
					if not curline.startswith('%'):
						self.exclude_list.append(curline.strip())

		print 'LOAD: Exclude list;\tFile: %s.' %fname

	def table_execute(self):
		execute_prompt = QtGui.QMessageBox.question(self, 'Please confirm', 'Are you sure that you want to create a new axis and append it to the font?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if execute_prompt == QtGui.QMessageBox.Yes:
			# - Init
			tab_process_masters = self.tab_masters.getTable()
			
			# - Process masters: Duplicate
			print '\nSTEP:\t Duplicating masters. ' + '-'*50		
			for index, master_dict in tab_process_masters.iteritems():
				new_name = master_dict['Master Name']
				old_name = self.active_font.pMasters.names[int(index)]
				self.active_font.pMasters.add(new_name, True, self.active_font.fl, old_name, True, False, self.active_font.pMasters.locate(old_name))
				print 'ADD:\t Master: %s; Source: %s.' %(new_name, old_name)

			self.active_font.update()
			self.active_font.updateObject(self.active_font.fl, 'Master table updated!\tFont: %s' %self.active_font.path)

			print '\nSTEP:\t Transforming masters. ' + '-'*50
			for index, master_dict in tab_process_masters.iteritems():
				# - Init
				process_layer = master_dict['Master Name']
				process_angle = radians(float(master_dict['Angle']))
				process_shift = float(master_dict['Shift'])
				new_transform = QtGui.QTransform().shear(process_angle, 0.).translate(process_shift, 0.)

				# - Process glyph: Transform layer
				for wGlyph in self.active_font.pGlyphs():
					
					if wGlyph.name not in self.exclude_list:
						wLayer = wGlyph.layer(process_layer)

						if wLayer is not None:
							# -- Transform at origin
							wBBox = wLayer.boundingBox
							wCenter = (wBBox.width()/2 + wBBox.x(), wBBox.height()/2 + wBBox.y())
							transform_to_origin = QtGui.QTransform().translate(-wCenter[0], -wCenter[1])
							transform_from_origin = QtGui.QTransform().translate(*wCenter)
							
							# -- Apply Transform
							wLayer.applyTransform(transform_to_origin)
							wLayer.applyTransform(new_transform)
							wLayer.applyTransform(transform_from_origin)

							wGlyph.update()
							#print 'MODIFY:\t Glyph: %s;\tLayer: %s.' %(wGlyph.name, process_layer)
							#wGlyph.updateObject(wGlyph.fl, ' Glyph: %s; Layer: %s' %(wGlyph.name, process_layer))
						else:
							print 'WARN:\t Glyph: %s;\tLayer: %s.\tGlyph is missing Outline or Layer! ' %(wGlyph.name, process_layer)
					else:
						print 'SKIP:\t Glyph: %s;\tExcluded from processing!' %wGlyph.name

			self.active_font.update()
			self.active_font.updateObject(self.active_font.fl, 'Glyphs Processed;\tFont: %s.' %self.active_font.path)

			# - Process Font: Add new Axis
			print '\nSTEP:\t Building axis. ' + '-'*50

			# -- Init
			new_axis = fl6.flAxis(self.cmb_axis_name.currentText,self.cmb_axis_short.currentText, self.cmb_axis_tag.currentText)
			
			# -- Process
			self.active_font.pSpace.add(new_axis)
			
			self.active_font.update()
			self.active_font.updateObject(self.active_font.fl, 'Axis: %s;\tFont: %s' %(self.cmb_axis_name.currentText, self.active_font.path))
			
			print '\nDONE:\t %s (%s)' %(app_name, app_version)
			
		else:
			print '\nABORT:\t %s (%s)\nWARN:\t No action taken!' %(app_name, app_version)

# - RUN ------------------------------
dialog = dlg_BuildAxis()