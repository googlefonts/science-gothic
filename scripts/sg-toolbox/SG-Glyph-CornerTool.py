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

# - Init --------------------------------
app_version = '1.1'
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
presets = {'Lowercase': { 	'Lt': [(233.77,(.85,.85)), (192.67,(.80,.80))],
							'Medium': None,
							'Blk': None,
							'Lt Cnd': [(205.55,(.85,.85)), (164.44,(.80,.80))],
							'Cnd': None,
							'Blk Cnd': None,
							'Lt Exp': [(233.77,(.85,.85)), (192.67,(.80,.80))],
							'Exp': None,
							'Blk Exp': None,
							'Lt Ctr': [(233.77,(.85,.85)), (192.67,(.80,.80))],
							'Ctr': None,
							'Blk Ctr': None,
							'Lt Cnd Ctr': [(205.55,(.85,.85)), (164.44,(.80,.80))],
							'Cnd Ctr': None,
							'Blk Cnd Ctr': None,
							'Lt Exp Ctr': [(233.77,(.85,.85)), (192.67,(.80,.80))],
							'Exp Ctr': None,
							'Blk Exp Ctr': None
							},
			'Uppercase': { 	'Lt': [(233.77,(.85,.85)), (192.67,(.80,.80))],
							'Medium': None,
							'Blk': None,
							'Lt Cnd': [(205.55,(.85,.85)), (164.44,(.80,.80))],
							'Cnd': None,
							'Blk Cnd': None,
							'Lt Exp': [(233.77,(.85,.85)), (192.67,(.80,.80))],
							'Exp': None,
							'Blk Exp': None,
							'Lt Ctr': [(233.77,(.85,.85)), (192.67,(.80,.80))],
							'Ctr': None,
							'Blk Ctr': None,
							'Lt Cnd Ctr': [(205.55,(.85,.85)), (164.44,(.80,.80))],
							'Cnd Ctr': None,
							'Blk Cnd Ctr': None,
							'Lt Exp Ctr': [(233.77,(.85,.85)), (192.67,(.80,.80))],
							'Exp Ctr': None,
							'Blk Exp Ctr': None
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

		self.btn_corner_in_TL = QtGui.QPushButton('TL (in)')
		self.btn_corner_in_TR = QtGui.QPushButton('TR (in)')
		self.btn_corner_in_BL = QtGui.QPushButton('BL (in)')
		self.btn_corner_in_BR = QtGui.QPushButton('BR (in)')
		self.btn_corner_out_TL = QtGui.QPushButton('TL (out)')
		self.btn_corner_out_TR = QtGui.QPushButton('TR (out)')
		self.btn_corner_out_BL = QtGui.QPushButton('BL (out)')
		self.btn_corner_out_BR = QtGui.QPushButton('BR (out)')
		self.btn_corner_in = QtGui.QPushButton('Inner Corner')
		self.btn_corner_out = QtGui.QPushButton('Outer Corner')
		self.btn_setStart = QtGui.QPushButton('Set Start Point')

		self.btn_corner_in_TL.clicked.connect(lambda: self.in_corner((0,0)))
		self.btn_corner_in_TR.clicked.connect(lambda: self.in_corner((0,1)))
		self.btn_corner_in_BL.clicked.connect(lambda: self.in_corner((1,0)))
		self.btn_corner_in_BR.clicked.connect(lambda: self.in_corner((1,1)))
		self.btn_corner_out_TL.clicked.connect(lambda: self.out_corner((0,0)))
		self.btn_corner_out_TR.clicked.connect(lambda: self.out_corner((0,1)))
		self.btn_corner_out_BL.clicked.connect(lambda: self.out_corner((1,0)))
		self.btn_corner_out_BR.clicked.connect(lambda: self.out_corner((1,1)))
		self.btn_corner_in.clicked.connect(lambda: self.in_corner((0,0)))
		self.btn_corner_out.clicked.connect(lambda: self.out_corner((0,0)))
		self.btn_setStart.clicked.connect(self.set_start)
		#self.btn_execute.clicked.connect(self.execute_table)
						
		# - Build layouts 
		layoutV = QtGui.QGridLayout() 
		layoutV.addWidget(QtGui.QLabel('Preset:'),			0, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.cmb_preset,					1, 0, 1, 8)
		layoutV.addWidget(QtGui.QLabel('Outer Corner:'),	2, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_corner_out,				3, 0, 1, 8)
		#layoutV.addWidget(self.btn_corner_out_TL,			3, 0, 1, 4)
		#layoutV.addWidget(self.btn_corner_out_TR,			3, 4, 1, 4)
		#layoutV.addWidget(self.btn_corner_out_BL,			4, 0, 1, 4)
		#layoutV.addWidget(self.btn_corner_out_BR,			4, 4, 1, 4)
		layoutV.addWidget(QtGui.QLabel('Inner Corner:'),	5, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_corner_in,				6, 0, 1, 8)
		#layoutV.addWidget(self.btn_corner_in_TL,			6, 0, 1, 4)
		#layoutV.addWidget(self.btn_corner_in_TR,			6, 4, 1, 4)
		#layoutV.addWidget(self.btn_corner_in_BL,			7, 0, 1, 4)
		#layoutV.addWidget(self.btn_corner_in_BR,			7, 4, 1, 4)
		layoutV.addWidget(QtGui.QLabel('Utils:'),			8, 0, 1, 8, QtCore.Qt.AlignBottom)
		layoutV.addWidget(self.btn_setStart,				9, 0, 1, 8)

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

	def in_corner(self, mode):
		glyph = eGlyph()
		selected_contours = {layer:glyph.selectedAtContours(layer)[0] for layer in presets[self.cmb_preset.currentText].keys()}
		selected_nodes =  {layer:glyph.selectedNodes(layer, extend=eNode) for layer in presets[self.cmb_preset.currentText].keys()}
		
		for layer, preset in presets[self.cmb_preset.currentText].iteritems():
			if preset is not None:
				selection = selected_nodes[layer]
				selection[0].cornerRound(*preset[1])

			else:
				cid, nid = selected_contours[layer]
				wNode = glyph.contours(layer)[cid].nodes()[nid]
				glyph.contours(layer)[cid].insert(nid, getNodesDummy(wNode.x, wNode.y))

		glyph.update()
		glyph.updateObject(glyph.fl, 'DONE:\t Glyph: %s\tInner corner.' %glyph.name) 

	def out_corner(self, mode):
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
					node_first.cornerRound(*preset[0])

		glyph.update()
		glyph.updateObject(glyph.fl, 'DONE:\t Glyph: %s\tOuter corner.' %glyph.name) 

# - RUN ------------------------------
dialog = dlg_cornerTool()
