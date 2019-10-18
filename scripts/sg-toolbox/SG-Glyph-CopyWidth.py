#FLM: Glyph: Copy BBox Data (TypeRig)
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
from typerig.proxy import pFont, pGlyph
from typerig.node import eNodesContainer

# - Init --------------------------------
app_version = '0.3'
app_name = '[SG] Copy Bbox Width'

# - Classes ----------------------
class dlg_widthTool(QtGui.QDialog):
	# - Copy Metric properties from other glyph
	def __init__(self):
		super(dlg_widthTool, self).__init__()

		# - Edit Fields
		self.edt_width = QtGui.QLineEdit()
		self.edt_height = QtGui.QLineEdit()

		self.edt_width.setPlaceholderText('Glyph Name')
		self.edt_height.setPlaceholderText('Glyph Name')

		# - Spin Box
		self.spb_width_percent =  QtGui.QSpinBox()
		self.spb_height_percent = QtGui.QSpinBox()
		self.spb_width_units =  QtGui.QSpinBox()
		self.spb_height_units = QtGui.QSpinBox()

		self.spb_width_percent.setMaximum(200)
		self.spb_height_percent.setMaximum(200)
		self.spb_width_units.setMaximum(200)
		self.spb_height_units.setMaximum(200)
		self.spb_width_units.setMinimum(-200)
		self.spb_height_units.setMinimum(-200)

		self.spb_width_percent.setSuffix('%')
		self.spb_height_percent.setSuffix('%')
		self.spb_width_units.setSuffix(' u')
		self.spb_height_units.setSuffix(' u')

		self.spb_width_percent.setMaximumWidth(50)
		self.spb_height_percent.setMaximumWidth(50)
		self.spb_width_units.setMaximumWidth(50)
		self.spb_height_units.setMaximumWidth(50)

		self.reset_fileds()

		# - Buttons
		self.btn_copyBBox_width = QtGui.QPushButton('&Copy Width')
		self.btn_copyBBox_height = QtGui.QPushButton('&Copy Height')
		self.btn_copyBBox_width.clicked.connect(lambda: self.copy_bbox(False))
		self.btn_copyBBox_height.clicked.connect(lambda: self.copy_bbox(True))
		
		# - Build
		self.layoutV = QtGui.QGridLayout() 
		self.layoutV.addWidget(QtGui.QLabel('Width:'), 	0, 0, 1, 1)
		self.layoutV.addWidget(self.edt_width, 			0, 1, 1, 3)
		self.layoutV.addWidget(QtGui.QLabel('@'), 		0, 4, 1, 1)
		self.layoutV.addWidget(self.spb_width_percent, 	0, 5, 1, 1)
		self.layoutV.addWidget(QtGui.QLabel('+'), 		0, 6, 1, 1)
		self.layoutV.addWidget(self.spb_width_units, 	0, 7, 1, 1)
		self.layoutV.addWidget(self.btn_copyBBox_width,	0, 8, 1, 1)

		self.layoutV.addWidget(QtGui.QLabel('Height:'), 1, 0, 1, 1)
		self.layoutV.addWidget(self.edt_height, 		1, 1, 1, 3)
		self.layoutV.addWidget(QtGui.QLabel('@'), 		1, 4, 1, 1)
		self.layoutV.addWidget(self.spb_height_percent, 1, 5, 1, 1)
		self.layoutV.addWidget(QtGui.QLabel('+'), 		1, 6, 1, 1)
		self.layoutV.addWidget(self.spb_height_units, 	1, 7, 1, 1)
		self.layoutV.addWidget(self.btn_copyBBox_height,1, 8, 1, 1)

		# - Set Widget
		self.setLayout(self.layoutV)
		self.setWindowTitle('%s %s' %(app_name, app_version))
		self.setGeometry(300, 300, 400, 50)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # Always on top!!
		self.show()

	def reset_fileds(self):
		# - Reset text fields
		self.edt_width.setText('')
		self.edt_height.setText('')
		
		# - Reset spin-box
		self.spb_width_percent.setValue(100)
		self.spb_height_percent.setValue(100)
		self.spb_width_units.setValue(0)
		self.spb_height_units.setValue(0)

	def copy_bbox(self, copy_height=False):
		font = pFont()
		dst_glyph = pGlyph()
		
		if copy_height:
			src_glyph = font.glyph(self.edt_height.text) if len(self.edt_height.text) else None
		else:
			src_glyph = font.glyph(self.edt_width.text) if len(self.edt_width.text) else None
		
		for layer in font.masters():
			selection = eNodesContainer(dst_glyph.selectedNodes(layer))
			
			if copy_height:
				dst_glyph_height = dst_glyph.getBounds(layer).height()
				src_glyph_height = src_glyph.getBounds(layer).height()

				dst_glyph_y = dst_glyph.getBounds(layer).y()
				src_glyph_y = src_glyph.getBounds(layer).y()

				adjPercent = self.spb_height_percent.value
				adjUnits = self.spb_height_units.value
				
				process_shift = src_glyph_height*adjPercent/100  - dst_glyph_height + adjUnits
				process_y = src_glyph_y*adjPercent/100 - dst_glyph_y + adjUnits

				selection.shift(0, process_shift)
				
				if process_y != 0:
					selection = eNodesContainer(dst_glyph.nodes(layer))
					selection.shift(0, process_y)

			else:
				dst_glyph_width = dst_glyph.getBounds(layer).width()
				src_glyph_width = src_glyph.getBounds(layer).width()

				adjPercent = self.spb_width_percent.value
				adjUnits = self.spb_width_units.value

				process_shift = src_glyph_width*adjPercent/100 - dst_glyph_width + adjUnits
				selection.shift(process_shift, 0)


		dst_glyph.updateObject(dst_glyph.fl, 'Copy BBox | SRC: %s; DST: %s.' %(src_glyph.name, dst_glyph.name))
		dst_glyph.update()
		
# - Finish --------------------------------------------
dialog = dlg_widthTool()
