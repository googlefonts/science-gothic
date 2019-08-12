#FLM: Glyph: Copy Layer (TypeRig)
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
from collections import OrderedDict
from typerig.gui import getProcessGlyphs
from typerig.proxy import pFont, pGlyph

# - Init --------------------------------
app_version = '1.5'
app_name = '[SG] Copy Layers'

# -- GUI related
table_dict = {1:OrderedDict([('Master Name', None), ('IN', None), ('OUT', None)])}
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
				newitem = QtGui.QTableWidgetItem(str(data[layer][key])) if m == 0 else QtGui.QTableWidgetItem()
				if m > 0: newitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
				if m > 0: newitem.setCheckState(QtCore.Qt.Unchecked) 
				self.setItem(n, m, newitem)
				
		self.setHorizontalHeaderLabels(name_column)
		self.setVerticalHeaderLabels(name_row)
		self.blockSignals(False)

	def getTable(self):
		returnDict = {}
		for row in range(self.rowCount):
			#returnDict[self.item(row, 0).text()] = (self.item(row, 1).checkState() == QtCore.Qt.Checked, self.item(row, 2).checkState() == QtCore.Qt.Checked)
			if self.item(row, 1).checkState() == QtCore.Qt.Checked:
				returnDict.setdefault('SRC',[]).append(self.item(row, 0).text())
			
			if self.item(row, 2).checkState() == QtCore.Qt.Checked:
				returnDict.setdefault('DST',[]).append(self.item(row, 0).text())

		return returnDict

	def markChange(self, item):
		item.setBackground(QtGui.QColor('powderblue'))

# - Dialogs --------------------------------
class dlg_BuildAxis(QtGui.QDialog):
	def __init__(self):
		super(dlg_BuildAxis, self).__init__()
	
		# - Init
		self.active_font = pFont()
		self.pMode = 0
		
		# - Basic Widgets
		self.tab_masters = WTableView(table_dict)
		self.table_populate()

		self.btn_refresh = QtGui.QPushButton('Refresh')
		self.btn_clear = QtGui.QPushButton('Clear')
		self.btn_execute = QtGui.QPushButton('Execute')

		self.btn_refresh.clicked.connect(self.table_populate)
		self.btn_execute.clicked.connect(self.table_execute)

		self.rad_glyph = QtGui.QRadioButton('Glyph')
		self.rad_window = QtGui.QRadioButton('Window')
		self.rad_selection = QtGui.QRadioButton('Selection')
		self.rad_font = QtGui.QRadioButton('Font')
		self.chk_outline = QtGui.QCheckBox('Outline')
		self.chk_guides = QtGui.QCheckBox('Guides')
		self.chk_anchors = QtGui.QCheckBox('Anchors')
		self.chk_lsb = QtGui.QCheckBox('LSB')
		self.chk_adv = QtGui.QCheckBox('Advance')
		self.chk_rsb = QtGui.QCheckBox('RSB')
		self.chk_lnk = QtGui.QCheckBox('Metric Links')
		self.chk_ref = QtGui.QCheckBox('References')
		
		# -- Set States
		self.chk_outline.setCheckState(QtCore.Qt.Checked)
		self.chk_adv.setCheckState(QtCore.Qt.Checked)
		self.chk_lsb.setCheckState(QtCore.Qt.Checked)
		self.chk_anchors.setCheckState(QtCore.Qt.Checked)
		self.chk_lnk.setCheckState(QtCore.Qt.Checked)
		self.chk_ref.setEnabled(False)
		self.chk_guides.setEnabled(False)

		self.rad_glyph.setChecked(True)
		self.rad_glyph.setEnabled(True)
		self.rad_window.setEnabled(True)
		self.rad_selection.setEnabled(True)
		self.rad_font.setEnabled(False)

		self.rad_glyph.toggled.connect(self.refreshMode)
		self.rad_window.toggled.connect(self.refreshMode)
		self.rad_selection.toggled.connect(self.refreshMode)
		self.rad_font.toggled.connect(self.refreshMode)
				
		# - Build layouts 
		layoutV = QtGui.QGridLayout() 
		layoutV.addWidget(QtGui.QLabel('Process Mode:'),	0, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.rad_glyph, 					1, 0, 1, 2)
		layoutV.addWidget(self.rad_window, 					1, 2, 1, 2)
		layoutV.addWidget(self.rad_selection, 				1, 4, 1, 2)
		layoutV.addWidget(self.rad_font, 					1, 6, 1, 2)
		layoutV.addWidget(QtGui.QLabel('Master Layers:'),	2, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_refresh, 				3, 0, 1, 4)
		layoutV.addWidget(self.btn_clear, 					3, 4, 1, 4)
		layoutV.addWidget(self.tab_masters, 				4, 0, 25, 8)
		layoutV.addWidget(QtGui.QLabel('Copy Options:'),	29, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.chk_outline,					30, 0, 1, 2)
		layoutV.addWidget(self.chk_guides, 					30, 2, 1, 2)
		layoutV.addWidget(self.chk_anchors,					30, 4, 1, 2)
		layoutV.addWidget(self.chk_ref,						30, 6, 1, 2)
		layoutV.addWidget(self.chk_lsb,						31, 0, 1, 2)
		layoutV.addWidget(self.chk_adv,						31, 2, 1, 2)
		layoutV.addWidget(self.chk_rsb,						31, 4, 1, 2)
		layoutV.addWidget(self.chk_lnk,						31, 6, 1, 2)
		layoutV.addWidget(self.btn_execute, 				32, 0, 1,8)

		# - Set Widget
		self.setLayout(layoutV)
		self.setWindowTitle('%s %s' %(app_name, app_version))
		self.setGeometry(300, 300, 300, 600)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # Always on top!!
		self.show()

	def refreshMode(self):
		if self.rad_glyph.isChecked(): self.pMode = 0
		if self.rad_window.isChecked(): self.pMode = 1
		if self.rad_selection.isChecked(): self.pMode = 2
		if self.rad_font.isChecked(): self.pMode = 3

	def copyLayer(self, glyph, srcLayerName, dstLayerName, options, cleanDST=False):
		# -- Outline
		if options['out']:
			# --- Get shapes
			srcShapes = glyph.shapes(srcLayerName)

			# --- Cleanup destination layers
			if cleanDST:
				glyph.layer(dstLayerName).removeAllShapes()
			
			# --- Copy/Paste shapes
			for shape in srcShapes:
				newShape = glyph.layer(dstLayerName).addShape(shape.cloneTopLevel())

		# -- Metrics
		if options['lsb']: glyph.setLSB(glyph.getRSB(srcLayerName), dstLayerName)
		if options['adv']: glyph.setAdvance(glyph.getAdvance(srcLayerName), dstLayerName)
		if options['rsb']: glyph.setRSB(glyph.getRSB(srcLayerName), dstLayerName)
		if options['lnk']:
			glyph.setLSBeq(glyph.getSBeq(srcLayerName)[0], dstLayerName)
			glyph.setRSBeq(glyph.getSBeq(srcLayerName)[1], dstLayerName)

		# -- Anchors
		if options['anc']:
			if cleanDST:
				glyph.clearAnchors(dstLayerName)

			for src_anchor in glyph.anchors(srcLayerName):
				glyph.layer(dstLayerName).addAnchor(src_anchor)

	def table_populate(self):
		self.tab_masters.setTable({n:OrderedDict([('Master Name', master), ('SRC', None), ('DST', None)]) for n, master in enumerate(self.active_font.pMasters.names)})
		self.tab_masters.resizeColumnsToContents()

	def table_execute(self):
		# - Init
		copy_options = {'out': self.chk_outline.isChecked(),
						'gui': self.chk_guides.isChecked(),
						'anc': self.chk_anchors.isChecked(),
						'lsb': self.chk_lsb.isChecked(),
						'adv': self.chk_adv.isChecked(),
						'rsb': self.chk_rsb.isChecked(),
						'lnk': self.chk_lnk.isChecked(),
						'ref': self.chk_ref.isChecked()
						}
		
		execute_prompt = QtGui.QMessageBox.question(self, 'Please confirm', 'Are you sure that you want to proceed?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		
		# - Process
		if execute_prompt == QtGui.QMessageBox.Yes:
			# - Init
			process_glyphs = getProcessGlyphs(self.pMode)
			process_dict = self.tab_masters.getTable()
			process_src = process_dict['SRC'][0]
			process_dst = process_dict['DST']

			for wGlyph in process_glyphs:
				for dst_layer in process_dst:
					self.copyLayer(wGlyph, process_src, dst_layer, copy_options, True)

				wGlyph.update()
				wGlyph.updateObject(wGlyph.fl, 'Glyph: %s\tCopy Layer | %s -> %s.' %(wGlyph.name, process_src, '; '.join(process_dst)))

		# - Abort
		else:
			print '\nABORT:\t %s (%s)\nWARN:\t No action taken!' %(app_name, app_version)

# - RUN ------------------------------
dialog = dlg_BuildAxis()