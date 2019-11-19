#FLM: Font: Find Slanted Shapes
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

def check_slanted(work_glyph):
	for layer in font.masters():
		for shape in work_glyph.shapes(layer):
			if shape.transform.type() == 8: #Slant transform
				return work_glyph.name

# - Init ------------------------------------------------
app_version = '0.01'
app_name = '[SG] Font Find Slanted Shapes'
font = pFont()
process_glyphs = font.pGlyphs()
glyphs_incompatible = []
glyphs_slantedferences = []
glyphs_search = set()
strong_test = True

# - Process --------------------------------------------
print '%s %s\n' %(app_name, app_version) + '-'*30

# - Decompose mixed reference glyphs
for work_glyph in process_glyphs:
	result = check_slanted(work_glyph)
	if result is not None: glyphs_slantedferences.append(result)

# - Output
output('Glyphs found with Slant transform', glyphs_slantedferences)

# - Finish --------------------------------------------
print 'DONE.'

