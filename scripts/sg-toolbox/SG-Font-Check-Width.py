#FLM: Check: Glyph width inconsistancies
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
from typerig.brain import isclose, ratfrac
from typerig.proxy import pFont, pGlyph
from typerig.string import diactiricalMarks

# - Init ------------------------------------------------
app_version = '0.2'
app_name = '[SG] Check: Width inconsistancies'

font = pFont()
#process_glyphs = font.pGlyphs(font.uppercase() + font.lowercase())
process_glyphs = font.selected_pGlyphs()

master_mark = 'Ctr'
error_margin = 20 #units
check_pairs = [(name, '%s %s'%(name, master_mark)) for name in font.masters() if master_mark not in name]

# - Process --------------------------------------------
print '%s %s\n' %(app_name, app_version) + '-'*30

if not len(process_glyphs): process_glyphs.append(pGlyph())

# - Remove empty tags from glyphs
for work_glyph in process_glyphs:
	error_list = []
	error_flag = False
	for pair in check_pairs:
		try:
			a = work_glyph.getBounds(pair[0]).width()
			b = work_glyph.getBounds(pair[1]).width()
			if not isclose(a, b, error_margin):
				error_flag = True
				error_list.append((pair[0], pair[1], a-b))
		except AttributeError:
			pass

	if error_flag: print 'WARN:\t Glyph: %s;\t BBOX width: %s' %(work_glyph.name, ' | '.join(['%s : %s : %s' %item for item in error_list]))	

# - Finish --------------------------------------------

print 'DONE.'

