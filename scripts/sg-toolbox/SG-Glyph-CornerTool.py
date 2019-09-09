#FLM: Glyph: Corner Tool (TypeRig)
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
from typerig.proxy import pFont, pContour
from typerig.glyph import eGlyph
from typerig.node import eNode
from typerig.brain import Line, Curve
from typerig.curve import eCurveEx

# - Init --------------------------------
app_version = '1.5'
app_name = '[SG] Corner Tool'

# -- Parts -----------------------------
def getNodesDummy(x, y):
	return [fl6.flNode(x,y, nodeType=1), fl6.flNode(x,y, nodeType=4), fl6.flNode(x,y, nodeType=4)]#, fl6.flNode(x,y, nodeType=1)]

# -- Presets for building angles:
# -- { glyph type:{
# --				layer name: [outer angle tuple (radius, (curvature out, curvature in),
# -- 							(inner angle tuple (radius, (curvature out, curvature in)]
# --							...
# -- 				layer n:	[(angle n, (curvature n)), (...,(...))]
# --			}}
presets = {'Lowercase': {
							'Blk Cnd Ctr': 	None,
							'Blk Cnd': 		None
							'Blk Ctr': 		None,
							'Blk Exp Ctr': 	None,
							'Blk Exp': 		None,
							'Blk': 			None,
							'Cnd Ctr': 		None,
							'Cnd': 			None,
							'Ctr': 			None,
							'Exp Ctr': 		None,
							'Exp': 			None,
							'Lt Cnd Ctr': 	[(205.548, (0.825, 0.75)), (164.438, (0.85, 0.75))],
							'Lt Cnd': 		[(205.548, (0.825, 0.75)), (164.438, (0.85, 0.75))],
							'Lt Ctr': 		[(233.773, (0.85, 0.85)), (192.666, (0.85, 0.75))],
							'Lt': 			[(233.773, (0.85, 0.85)), (192.666, (0.85, 0.85))],
							'Lt Exp Ctr': 	[(228.548, (0.85, 0.85)), (192.666, (0.85, 0.85))],
							'Lt Exp': 		[(228.548, (0.85, 0.85)), (192.666, (0.85, 0.85))],
							'Medium': 		None,
						},

			'Uppercase': {	
							'Blk Cnd Ctr': 	None,
							'Blk Cnd': 		None,
							'Blk Ctr': 		None,
							'Blk Exp Ctr': 	None,
							'Blk Exp': 		None,
							'Blk': 			None,
							'Cnd Ctr': 		None,
							'Cnd': 			None,
							'Ctr': 			None,
							'Exp Ctr': 		None,
							'Exp': 			None,
							'Lt Cnd Ctr': 	[(282.843, (0.78, 0.78)), (229.12, (0.75, 0.742))],
							'Lt Cnd': 		[(282.843, (0.78, 0.78)), (229.12, (0.75, 0.742))],
							'Lt Ctr': 		[(413.793, (0.81, 0.85)), (360.168, (0.84, 0.80))],
							'Lt': 			[(413.793, (0.81, 0.85)), (360.168, (0.84, 0.80))],
							'Lt Exp Ctr': 	[(424.264, (0.86, 0.86)), (370.535, (0.85, 0.85))],
							'Lt Exp':		[(424.264, (0.86, 0.86)), (370.535, (0.85, 0.85))],
							'Medium': 		None
						},

			'User': 	{ 	
							'Blk Cnd Ctr': 	None,
							'Blk Cnd': 		None,
							'Blk Ctr': 		None,
							'Blk Exp Ctr':	None,
							'Blk Exp': 		None,
							'Blk': 			None,
							'Cnd Ctr': 		None,
							'Cnd': 			None,
							'Ctr': 			None,
							'Exp Ctr':		None,
							'Exp': 			None,
							'Lt Cnd Ctr': 	[(0.,(0.,0.)), (0.,(0.,0.))],
							'Lt Cnd': 		[(0.,(0.,0.)), (0.,(0.,0.))],
							'Lt Ctr': 		[(0.,(0.,0.)), (0.,(0.,0.))],
							'Lt': 			[(0.,(0.,0.)), (0.,(0.,0.))],
							'Lt Exp Ctr': 	[(0.,(0.,0.)), (0.,(0.,0.))],
							'Lt Exp': 		[(0.,(0.,0.)), (0.,(0.,0.))],
							'Medium': 		None
						}
			}


# - Dialogs --------------------------------
class dlg_cornerTool(QtGui.QDialog):
	def __init__(self):
		super(dlg_cornerTool, self).__init__()
	
		# - Init
		self.active_font = pFont()
		self.pMode = 0
		
		# - Basic Widgets
		self.cmb_preset = QtGui.QComboBox()
		self.cmb_preset.addItems(presets.keys())

		self.btn_corner_in = QtGui.QPushButton('Inner Corner')
		self.btn_corner_revIn = QtGui.QPushButton('Inner Swap')
		self.btn_corner_getIn = QtGui.QPushButton('Get User Inner')
		self.btn_corner_out = QtGui.QPushButton('Outer Corner')
		self.btn_corner_revOut = QtGui.QPushButton('Outer Swap')
		self.btn_corner_getOut = QtGui.QPushButton('Get User Outer')
		self.btn_setStart = QtGui.QPushButton('Set Start Point')
		self.btn_measure = QtGui.QPushButton('Measure Corner')

		self.btn_corner_in.clicked.connect(lambda: self.in_corner(False))
		self.btn_corner_out.clicked.connect(lambda: self.out_corner(False))
		self.btn_corner_revIn.clicked.connect(lambda: self.in_corner(True))
		self.btn_corner_revOut.clicked.connect(lambda: self.out_corner(True))
		self.btn_corner_getOut.clicked.connect(lambda: self.get_measurment(0))
		self.btn_corner_getIn.clicked.connect(lambda: self.get_measurment(1))
		self.btn_measure.clicked.connect(lambda: self.get_measurment(-1))
		self.btn_setStart.clicked.connect(self.set_start)
						
		# - Build layouts 
		layoutV = QtGui.QGridLayout() 
		layoutV.addWidget(QtGui.QLabel('Preset:'),			0, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.cmb_preset,					1, 0, 1, 8)
		layoutV.addWidget(self.btn_corner_getOut,			2, 0, 1, 4)
		layoutV.addWidget(self.btn_corner_getIn,			2, 4, 1, 4)
		layoutV.addWidget(QtGui.QLabel('Outer Corner:'),	3, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_corner_out,				4, 0, 1, 4)
		layoutV.addWidget(self.btn_corner_revOut,			4, 4, 1, 4)
		layoutV.addWidget(QtGui.QLabel('Inner Corner:'),	6, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_corner_in,				7, 0, 1, 4)
		layoutV.addWidget(self.btn_corner_revIn,			7, 4, 1, 4)
		layoutV.addWidget(QtGui.QLabel('Utils:'),			9, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_setStart,				10, 0, 1, 4)
		layoutV.addWidget(self.btn_measure,					10, 4, 1, 4)

		# - Set Widget
		self.setLayout(layoutV)
		self.setWindowTitle('%s %s' %(app_name, app_version))
		self.setGeometry(300, 300, 300, 200)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) # Always on top!!
		self.show()

	# - Procedures
	def set_start(self):
		glyph = eGlyph()
		selected_contours = {layer:glyph.selectedAtContours(layer)[0] for layer in presets[self.cmb_preset.currentText].keys()}

		for layer, selection in selected_contours.iteritems():
			cid, nid = selection
			glyph.contours(layer)[cid].setStartPoint(nid)

		glyph.update()
		glyph.updateObject(glyph.fl, 'CHANGE:\t Glyph: %s\tSet Start Point.' %glyph.name)

	def get_measurment(self, mode=-1):
		glyph = eGlyph()
		
		for layer in presets[self.cmb_preset.currentText].keys():
			if presets['User'][layer] is not None:
				probe = glyph.selectedNodes(layer, extend=eNode)[0]
				segment_nodes = probe.getSegmentNodes()
				selSegment = eCurveEx(segment_nodes)
				probe_line = Line(segment_nodes[0], segment_nodes[-1])
				lenght = probe_line.getLenght()
				c0, c1 = selSegment.curve.getHobbyCurvature()
				
				if mode == 0:
					presets['User'][layer][0] = (round(lenght,3), (round(c0.real,3), round(c1.real,3)))
				elif mode ==1:
					presets['User'][layer][1] = (round(lenght,3), (round(c0.real,3), round(c1.real,3)))
				else:
					print 'Measure:\t Glyph: %s;\tLayer: %s;\tLength: %s; Curvature: %s, %s' %(glyph.name, layer, round(lenght,3), round(c0.real,3), round(c1.real,3))

		if mode > -1:
			print 'UPDATE:\t User Preset: %s' %['Outer Corner', 'Inner Corner'][mode]
		else:
			modifiers = QtGui.QApplication.keyboardModifiers() 
			if modifiers == QtCore.Qt.ShiftModifier:
				print presets['User']

	def in_corner(self, swap=False):
		glyph = eGlyph()
		selected_contours = {layer:glyph.selectedAtContours(layer)[0] for layer in presets[self.cmb_preset.currentText].keys()}
		selected_nodes =  {layer:glyph.selectedNodes(layer, extend=eNode) for layer in presets[self.cmb_preset.currentText].keys()}
		
		for layer, preset in presets[self.cmb_preset.currentText].iteritems():
			if preset is not None:
				selection = selected_nodes[layer]
				lenght, curvature = preset[1]
				c0, c1 = curvature
				selection[0].cornerRound(lenght, [(c0,c1),(c1,c0)][swap])

			else:
				cid, nid = selected_contours[layer]
				wNode = glyph.contours(layer)[cid].nodes()[nid]
				glyph.contours(layer)[cid].insert(nid, getNodesDummy(wNode.x, wNode.y))

		glyph.update()
		glyph.updateObject(glyph.fl, 'DONE:\t Glyph: %s\tInner corner.' %glyph.name) 

	def out_corner(self, swap=False):
		glyph = eGlyph()
		selected_nodes =  {layer:glyph.selectedNodes(layer, extend=eNode) for layer in presets[self.cmb_preset.currentText].keys()}

		for layer, preset in presets[self.cmb_preset.currentText].iteritems():
			if preset is not None:
				selection = selected_nodes[layer]

				if len(selection) > 1:
					# - Rebuild corner
					node_first = selection[0]
					node_last = selection[-1]
					
					line_in = node_first.getPrevLine() if node_first.getPrevOn(False) not in selection else node_first.getNextLine()
					line_out = node_last.getNextLine() if node_last.getNextOn(False) not in selection else node_last.getPrevLine()

					crossing = line_in & line_out

					node_first.smartReloc(*crossing)
					node_first.parent.removeNodesBetween(node_first.fl, node_last.getNextOn())

					# - Round
					lenght, curvature = preset[0]
					c0, c1 = curvature
					node_first.cornerRound(lenght, [(c0,c1),(c1,c0)][swap])

		glyph.update()
		glyph.updateObject(glyph.fl, 'DONE:\t Glyph: %s\tOuter corner.' %glyph.name) 

# - RUN ------------------------------
dialog = dlg_cornerTool()
