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
app_version = '1.8'
app_name = '[SG] Copy Layers'

# -- Copy Presets (by request)
copy_presets = {'contrast':[('Blk','Blk Ctr'),
							('Blk Cnd','Blk Cnd Ctr'),
							('Blk Exp','Blk Exp Ctr'),
							('Cnd','Cnd Ctr'),
							('Medium','Ctr'),
							('Exp','Exp Ctr'),
							('Lt','Lt Ctr'),
							('Lt Cnd','Lt Cnd Ctr'),
							('Lt Exp','Lt Exp Ctr')],

				'width': 	[('Blk','Blk Cnd'),
							('Medium','Cnd'),
							('Lt','Lt Cnd'),
							('Blk','Blk Exp'),
							('Medium','Exp'),
							('Lt','Lt Exp')]
				}

# -- GUI related
table_dict = {1:OrderedDict([('Master Name', None), ('SRC', False), ('DST', False)])}
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
				if m > 0: newitem.setCheckState(QtCore.Qt.Unchecked if not data[layer][key] else QtCore.Qt.Checked) 

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
class dlg_CopyLayer(QtGui.QDialog):
	def __init__(self):
		super(dlg_CopyLayer, self).__init__()
	
		# - Init
		self.active_font = pFont()
		self.pMode = 0
		
		# - Basic Widgets
		self.tab_masters = WTableView(table_dict)
		self.table_populate()

		self.edt_checkStr = QtGui.QLineEdit()
		self.edt_checkStr.setPlaceholderText('DST string')
		self.edt_checkStr.setToolTip('Enter search criteria for selectively selecting destination masters.')
		self.btn_refresh = QtGui.QPushButton('Clear')
		self.btn_checkOn = QtGui.QPushButton('Select')
		self.btn_execute = QtGui.QPushButton('Execute Selection')
		self.btn_preset_contrast = QtGui.QPushButton('Copy to Contrast Masters')
		self.btn_preset_width = QtGui.QPushButton('Copy to Width Masters')

		self.btn_refresh.clicked.connect(self.table_populate)
		self.btn_checkOn.clicked.connect(lambda: self.table_populate(True))
		self.btn_execute.clicked.connect(self.execute_table)
		self.btn_preset_contrast.clicked.connect(lambda: self.execute_preset(copy_presets['contrast']))
		self.btn_preset_width.clicked.connect(lambda: self.execute_preset(copy_presets['width']))

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
		layoutV.addWidget(QtGui.QLabel('Copy Options:'),	2, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.chk_outline,					3, 0, 1, 2)
		layoutV.addWidget(self.chk_guides, 					3, 2, 1, 2)
		layoutV.addWidget(self.chk_anchors,					3, 4, 1, 2)
		layoutV.addWidget(self.chk_ref,						3, 6, 1, 2)
		layoutV.addWidget(self.chk_lsb,						4, 0, 1, 2)
		layoutV.addWidget(self.chk_adv,						4, 2, 1, 2)
		layoutV.addWidget(self.chk_rsb,						4, 4, 1, 2)
		layoutV.addWidget(self.chk_lnk,						4, 6, 1, 2)
		layoutV.addWidget(QtGui.QLabel('Master Layers: Single source to multiple destinations'),	5, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(QtGui.QLabel('Search:'),			6, 0, 1, 1)
		layoutV.addWidget(self.edt_checkStr, 				6, 1, 1, 3)
		layoutV.addWidget(self.btn_checkOn, 				6, 4, 1, 2)
		layoutV.addWidget(self.btn_refresh, 				6, 6, 1, 2)
		layoutV.addWidget(self.tab_masters, 				7, 0, 15, 8)
		layoutV.addWidget(self.btn_execute, 				22, 0, 1,8)
		layoutV.addWidget(QtGui.QLabel('Master Layers: Copy Presets'),	23, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_preset_contrast, 		24, 0, 1,8)
		layoutV.addWidget(self.btn_preset_width, 			25, 0, 1,8)

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

	def table_populate(self, filterDST=False):
		if not filterDST:	
			self.tab_masters.setTable({n:OrderedDict([('Master Name', master), ('SRC', False), ('DST', False)]) for n, master in enumerate(self.active_font.pMasters.names)})
			self.tab_masters.resizeColumnsToContents()
		else:
			#print ';'.join(sorted(self.active_font.pMasters.names))
			self.tab_masters.setTable({n:OrderedDict([('Master Name', master), ('SRC', False), ('DST', self.edt_checkStr.text in master)]) for n, master in enumerate(self.active_font.pMasters.names)})
			self.tab_masters.resizeColumnsToContents()

	def getCopyOptions(self):
		options = {'out': self.chk_outline.isChecked(),
					'gui': self.chk_guides.isChecked(),
					'anc': self.chk_anchors.isChecked(),
					'lsb': self.chk_lsb.isChecked(),
					'adv': self.chk_adv.isChecked(),
					'rsb': self.chk_rsb.isChecked(),
					'lnk': self.chk_lnk.isChecked(),
					'ref': self.chk_ref.isChecked()
					}
		return options

	def execute_table(self):
		# - Init
		copy_options = self.getCopyOptions()
		process_glyphs = getProcessGlyphs(self.pMode)
		
		# - Process
		process_dict = self.tab_masters.getTable()
		process_src = process_dict['SRC'][0]
		process_dst = process_dict['DST']

		for wGlyph in process_glyphs:
			for dst_layer in process_dst:
				self.copyLayer(wGlyph, process_src, dst_layer, copy_options, True)

			wGlyph.update()
			wGlyph.updateObject(wGlyph.fl, 'Glyph: %s\tCopy Layer | %s -> %s.' %(wGlyph.name, process_src, '; '.join(process_dst)))

	def execute_preset(self, preset_list):
		# - Init
		copy_options = self.getCopyOptions()
		process_glyphs = getProcessGlyphs(self.pMode)
		print_preset = [' -> '.join(item) for item in preset_list]
		
		# - Process
		for wGlyph in process_glyphs:
			for process_src, process_dst in preset_list:
				self.copyLayer(wGlyph, process_src, process_dst, copy_options, True)

			wGlyph.update()
			wGlyph.updateObject(wGlyph.fl, 'Glyph: %s\tCopy Layer Preset | %s.' %(wGlyph.name, ' | '.join(print_preset)))

# - RUN ------------------------------
dialog = dlg_CopyLayer()