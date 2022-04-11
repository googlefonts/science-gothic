#FLM: Glyph: Fix width
# ----------------------------------------
# (C) Vassil Kateliev, 2019 (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
#-----------------------------------------
# www.typerig.com

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------
import string
import fontlab as fl6

from typerig.proxy import *
from typerig.core.func.math import isclose, ratfrac
from typerig.proxy.string import diactiricalMarks

# - Init ------------------------------------------------
app_version = '0.2'
app_name = '[SG] Glyph Fix WIDTH inconsistancies'

font = pFont()
work_glyph = pGlyph()

master_mark = 'Ctr'
error_margin = 10 #units
check_pairs = [(name, '%s %s'%(name, master_mark)) for name in font.masters() if master_mark not in name]

# - Catch errors -------------------------------------------
def do_chek():
	error_list = []
	for pair in check_pairs:
		if work_glyph.layer(pair[0]) is not None and work_glyph.layer(pair[1]) is not None:
			a = work_glyph.getBounds(pair[0]).width()
			b = work_glyph.getBounds(pair[1]).width()
			if not isclose(a, b, error_margin):	error_list.append((pair[1], a-b))
	return error_list

# - Shift nodes -------------------------------------------
for layer, offset_x in do_chek():
	selectedNodes = work_glyph.selectedNodes(layer=layer, extend=eNode)
	
	for node in selectedNodes:
		if node.isOn:
			node.smartShift(offset_x, 0)
	
	# - Finish it
	work_glyph.update()

work_glyph.updateObject(work_glyph.fl)

# - Finish --------------------------------------------
print 'Check:\t %s' %do_chek()

