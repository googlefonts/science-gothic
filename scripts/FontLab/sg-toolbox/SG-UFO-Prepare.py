#FLM: UFO: Prepare Font
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
	result_string = '/'+' /'.join(sorted(glyph_list))
	print '%s: %s\n' %(msg_str, result_string)

# - Init ------------------------------------------------
app_version = '0.21'
app_name = '[SG] UFO Prepare Font'
font = pFont()
process_glyphs = font.pGlyphs()
glyphs_incompatible = {}
glyphs_mixreferences = []
glyphs_search = set()
strong_test = True

# - Process --------------------------------------------
print '%s %s\n' %(app_name, app_version) + '-'*30

# - Remove empty tags from glyphs
for work_glyph in process_glyphs:
	if len(work_glyph.tags):
		if any([tag in string.whitespace for tag in work_glyph.tags]):
			glyphs_search.add(work_glyph.name)
			work_glyph.fl.tags = [tag for tag in work_glyph.tags if tag not in string.whitespace]
			work_glyph.update()
			#work_glyph.updateObject(work_glyph.fl, verbose=False)

output('Bad glyphs tags (removed)', list(glyphs_search))

# - Decompose mixed reference glyphs
for work_glyph in process_glyphs:
	if work_glyph.isMixedReference():
		glyphs_mixreferences.append(work_glyph.name)

		for layer in work_glyph.layers():
			work_glyph.decompose(layer.name)
			work_glyph.dereference(layer.name)

output('Mixed reference Glyphs (decomposed)', glyphs_mixreferences)

# - Remove Incompatible glyphs
for work_glyph in process_glyphs:
	if not work_glyph.isCompatible(strong_test): 
		glyphs_incompatible[work_glyph.name] = work_glyph.fl

for glyph_name, glyph in glyphs_incompatible.iteritems():
	font.fl.deleteGlyph(glyph)

output('Incompatible Glyphs (removed)', glyphs_incompatible.keys())

# - Finish --------------------------------------------
font.update()
print 'DONE.'

