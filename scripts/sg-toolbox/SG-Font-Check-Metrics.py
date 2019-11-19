#FLM: Check: Metric links
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
from typerig.proxy import pFont, pGlyph

def output(msg_str, glyph_list):
	result_string = '/'+' /'.join(sorted(glyph_list)) if len(glyph_list) else None
	print '%s: %s\n' %(msg_str, result_string)

# - Init ------------------------------------------------
app_version = '0.02'
app_name = '[SG] Check: Metric links'
font = pFont()
process_glyphs = font.pGlyphs()
glyphs_left = []
glyphs_right = []
glyphs_search = set()

# -- Config
left_search = 'l('
right_search = 'r('
layer_criteria =' S'
check_layers = [layer for layer in font.masters() if layer_criteria in layer]

# - Process --------------------------------------------
print '%s %s\n' %(app_name, app_version) + '-'*30

# - Decompose mixed reference glyphs
for work_glyph in process_glyphs:
	for layerName in check_layers:
		lsb_eq, rsb_eq = work_glyph.getSBeq(layerName)
		
		if left_search in lsb_eq or right_search in lsb_eq:
			glyphs_left.append(work_glyph.name)
			break

		if left_search in rsb_eq or right_search in rsb_eq:
			glyphs_right.append(work_glyph.name)
			break

# - Output
output('Glyphs LSB', list(set(glyphs_left)))
output('Glyphs RSB', list(set(glyphs_right)))

# - Finish --------------------------------------------
print 'DONE.'

