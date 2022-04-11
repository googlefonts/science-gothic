#FLM: Metrics: Relink SC metrics
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
app_version = '0.01'
app_name = '[SG] Metrics: Relink SMCP metrics to SC'
font = pFont()
process_glyphs = font.pGlyphs()
glyphs_processed = []
fr_pair = ('.smcp', '.sc')

# - Process --------------------------------------------
print '%s %s\n' %(app_name, app_version) + '-'*30

# - Decompose mixed reference glyphs
for work_glyph in process_glyphs:
	flag_glyph = False

	for layer in font.masters():
		old_lsb, old_rsb = work_glyph.getSBeq(layer)
		
		if fr_pair[0] in old_lsb: 
			new_lsb = old_lsb.replace(*fr_pair)
			work_glyph.setLSBeq(new_lsb, layer)
			flag_glyph = True

		if fr_pair[0] in old_rsb: 
			new_rsb = old_rsb.replace(*fr_pair)
			work_glyph.setRSBeq(new_lsb, layer)
			flag_glyph = True

	if flag_glyph: glyphs_processed.append(work_glyph.name)

# - Output
if len(process_glyphs):
	output('Processed glyphs', glyphs_processed)
	font.update()

# - Finish --------------------------------------------
print 'DONE.'

