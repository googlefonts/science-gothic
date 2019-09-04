#FLM: Glyph: Checkout (TypeRig)
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
app_version = '0.6'
app_name = '[SG] Glyph Checkout'
table_dict = {1:OrderedDict([('Glyph Name', None), ('Tags', None), ('Time', None), ('Date', None)])}

# - Widgets -----------------------------
class WTableView(QtGui.QTableWidget):
	def __init__(self, data):
		super(WTableView, self).__init__()
		
		# - Init
		self.setColumnCount(max(map(len, data.values())))
		self.setRowCount(len(data.keys()))

		# - Set 
		self.setTable(data)		

		# - Styling
		self.setSortingEnabled(True)
		self.horizontalHeader().setStretchLastSection(True)
		self.setAlternatingRowColors(True)
		self.setShowGrid(False)
		#self.resizeColumnsToContents()
		self.resizeRowsToContents()

	def setTable(self, data):
		name_row, name_column = [], []
		self.setColumnCount(max(map(len, data.values())))
		self.setRowCount(len(data.keys()))

		# - Populate
		for n, layer in enumerate(sorted(data.keys())):
			name_row.append(layer)

			for m, key in enumerate(data[layer].keys()):
				# -- Build name column
				name_column.append(key)
				
				# -- Add first data column
				newitem = QtGui.QTableWidgetItem(str(data[layer][key])) 
				self.setItem(n, m, newitem)

		self.setHorizontalHeaderLabels(name_column)
		self.setVerticalHeaderLabels(name_row)

	def getTable(self):
		returnDict = {}
		for row in range(self.rowCount):
			pass

		return returnDict

	def keyPressEvent(self, e):
		if (e.modifiers() & QtCore.Qt.ControlModifier):
			selected = self.selectedRanges()

			if e.key() == QtCore.Qt.Key_C: #copy
				s = ''
				for r in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
					s += '/%s, ' %str(self.item(r,0).text())
									
				QtGui.QApplication.clipboard().setText(s[:-2])

# - Dialogs --------------------------------
class dlg_GlyphCheckout(QtGui.QDialog):
	def __init__(self):
		super(dlg_GlyphCheckout, self).__init__()
	
		# - Init
		self.active_font = pFont()
		
		# - Basic Widgets
		self.wgt_calendar = QtGui.QCalendarWidget(self)
		self.wgt_calendar.setGridVisible(True)
		self.wgt_calendar.clicked.connect(self.showDate)
		date = self.wgt_calendar.selectedDate

		self.tab_glyphs = WTableView(table_dict)	
		

		self.edt_checkStr = QtGui.QLineEdit()
		self.edt_checkStr.setPlaceholderText('Tag')
		self.btn_filter = QtGui.QPushButton('Filter')
		self.btn_refresh = QtGui.QPushButton('Refresh')
		self.btn_filter.clicked.connect(lambda: self.showDate(self.wgt_calendar.selectedDate, find = self.edt_checkStr.text))
		self.btn_refresh.clicked.connect(lambda: self.showDate())
				
		# - Build layouts 
		layoutV = QtGui.QGridLayout() 
		layoutV.addWidget(QtGui.QLabel('Select date:'),				0, 0, 1, 8)
		layoutV.addWidget(self.wgt_calendar, 						1, 0, 5, 8)
		layoutV.addWidget(QtGui.QLabel('Glyphs modified on date:'),	6, 0, 1, 8)
		layoutV.addWidget(self.tab_glyphs, 							7, 0, 15, 8)
		layoutV.addWidget(QtGui.QLabel('Filter by tag:'),			22, 0, 1, 1)
		layoutV.addWidget(self.edt_checkStr, 						22, 1, 1, 3)
		layoutV.addWidget(self.btn_filter, 							22, 4, 1, 2)
		layoutV.addWidget(self.btn_refresh, 						22, 6, 1, 2)
				
		# - Set Widget
		self.setLayout(layoutV)
		self.setWindowTitle('%s %s' %(app_name, app_version))
		self.setGeometry(300, 300, 500, 800)
		#self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # Always on top!!
		self.show()

	def showDate(self, date, find=None):
		if find is None:
			new_table_dict = {n:OrderedDict([('Glyph Name', glyph.name), ('Tags', '; '.join(sorted(glyph.getTags(), key=len))), ('Time', glyph.fl.lastModified.time()), ('Date', glyph.fl.lastModified.date())]) for n, glyph in enumerate(self.active_font.pGlyphs()) if glyph.fl.lastModified.date() == self.wgt_calendar.selectedDate}
		else:
			new_table_dict = {n:OrderedDict([('Glyph Name', glyph.name), ('Tags', '; '.join(sorted(glyph.getTags(), key=len))), ('Time', glyph.fl.lastModified.time()), ('Date', glyph.fl.lastModified.date())]) for n, glyph in enumerate(self.active_font.pGlyphs()) if glyph.fl.lastModified.date() == self.wgt_calendar.selectedDate and find in glyph.getTags()}
		
		self.tab_glyphs.clear()

		if len(new_table_dict.keys()):
			self.tab_glyphs.setTable(new_table_dict)
		else:
			print 'WARN:\t No glyph modification informatio found on Date:%s' %self.wgt_calendar.selectedDate
			self.tab_glyphs.setTable(table_dict)
		


# - RUN ------------------------------
dialog = dlg_GlyphCheckout()