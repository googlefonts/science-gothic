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

from typerig.proxy import pFont, pGlyph

# - Init --------------------------------
app_version = '0.5'
app_name = 'Copy Layers'

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
		self.exclude_list = []
		
		# - Widgets
		self.tab_masters = WTableView(table_dict)
		self.table_populate()

		self.btn_refresh = QtGui.QPushButton('Refresh')
		self.btn_clear = QtGui.QPushButton('Clear')
		self.btn_execute = QtGui.QPushButton('Execute')

		#self.btn_exclude_file.clicked.connect(self.load_exclude_list)
		self.btn_refresh.clicked.connect(self.table_populate)
		self.btn_execute.clicked.connect(self.table_execute)
		
		# - Build layouts 
		layoutV = QtGui.QGridLayout() 
		layoutV.addWidget(QtGui.QLabel('Master Layers:'),	0, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_refresh, 				1, 0, 1, 4)
		layoutV.addWidget(self.btn_clear, 					1, 4, 1, 4)
		layoutV.addWidget(self.tab_masters, 				2, 0, 25,8)
		layoutV.addWidget(self.btn_execute, 				27, 0, 1,8)

		# - Set Widget
		self.setLayout(layoutV)
		self.setWindowTitle('%s %s' %(app_name, app_version))
		self.setGeometry(300, 300, 300, 600)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # Always on top!!
		self.show()

	def copyLayer(self, glyph, srcLayerName, dstLayerName, cleanDST=False):
		
		# -- Get shapes
		srcShapes = glyph.shapes(srcLayerName)

		# -- Cleanup destination layers
		if cleanDST:
			glyph.layer(dstLayerName).removeAllShapes()
		
		# -- Copy/Paste shapes
		for shape in srcShapes:
			newShape = glyph.layer(dstLayerName).addShape(shape.cloneTopLevel())

		# -- Copy/Paste metrics
		glyph.setLSB(glyph.getRSB(srcLayerName), dstLayerName)
		glyph.setAdvance(glyph.getAdvance(srcLayerName), dstLayerName)

	def table_populate(self):
		self.tab_masters.setTable({n:OrderedDict([('Master Name', master), ('SRC', None), ('DST', None)]) for n, master in enumerate(self.active_font.pMasters.names)})
		self.tab_masters.resizeColumnsToContents()

	def table_execute(self):
		execute_prompt = QtGui.QMessageBox.question(self, 'Please confirm', 'Are you sure that you want to proceed?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		execute_prompt = QtGui.QMessageBox.Yes
		if execute_prompt == QtGui.QMessageBox.Yes:
			# - Init
			wGlyph = pGlyph()
			process_dict = self.tab_masters.getTable()
			process_src = process_dict['SRC'][0]
			process_dst = process_dict['DST']

			for dst_layer in process_dst:
				self.copyLayer(wGlyph, process_src, dst_layer, True)

			wGlyph.update()
			wGlyph.updateObject(wGlyph.fl, 'Copy Layer | %s -> %s.' %(process_src, '; '.join(process_dst)))


		else:
			print '\nABORT:\t %s (%s)\nWARN:\t No action taken!' %(app_name, app_version)

# - RUN ------------------------------
dialog = dlg_BuildAxis()