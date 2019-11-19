#FLM: Font: Check QA
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
import gc

def output(msg_str, glyph_list):
	result_string = '/'+' /'.join(sorted(glyph_list)) if len(glyph_list) else None
	print '%s: %s\n' %(msg_str, result_string)

# - Init ------------------------------------------------
app_version = '0.01'
app_name = '[SG] Font QA'
font = pFont()
process_glyphs = font.pGlyphs()
glyphs_incompatible = []
glyphs_mixreferences = []
glyphs_search = set()
strong_test = True

# - Process --------------------------------------------
print '%s %s\n' %(app_name, app_version) + '-'*30

# - Decompose mixed reference glyphs
for work_glyph in process_glyphs:
	if work_glyph.isMixedReference():
		glyphs_mixreferences.append(work_glyph.name)

	if not work_glyph.isCompatible(strong_test): 
		glyphs_incompatible.append(work_glyph.name)

# - Output
output('Mixed reference Glyphs found', glyphs_mixreferences)
output('Incompatible Glyphs found', glyphs_incompatible)

# - Finish --------------------------------------------
gc.collect()
print 'DONE.'

