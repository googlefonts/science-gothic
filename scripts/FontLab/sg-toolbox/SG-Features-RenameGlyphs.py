#FLM: Features: Rename Glyphs
# NOTE: Find and rename glyph names in font and features using a predefined pattern
# ----------------------------------------
# (C) Vassil Kateliev, 2024 (http://www.kateliev.com)
# (C) Karandash Type Foundry
#-----------------------------------------
# www.typerig.com


# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------
import fontlab as fl6
import fontgate as fgt

from typerig.proxy.fl.objects.font import pFont
from typerig.proxy.fl.objects.glyph import eGlyph

# - Config --------------------------
reported = 	["dzcaron","hcircumflex","idotless","kcommaaccent","lj","nj","oogonek","rcommaaccent","scedilla","tcedilla","uni1E81","uni1E83","uni1E85"]
collected = ["uni01C6","uni0125","dotlessi","uni0137","uni01C9","uni01CC","uni01EB","uni0157","uni015F","uni0163","wgrave","wacute","wdieresis"]
glyph_rename_dict = dict(zip(reported, collected))

# - Init --------------------------
font = pFont()
font_features = font.getFeatureTags()

# -- Fix OT features
for tag in font_features:
	feature = font.getFeature(tag)
	do_update = False

	for find, replace in glyph_rename_dict.items():
		if find in feature: 
			print('WARN:\tFeature: {}; Find: {}; Replace: {};'.format(tag, find, replace))
			do_update = True
		
		feature.replace(find, replace)

	if do_update:
		font.delFeature(tag)
		font.setFeature(tag, feature)

# -- Fix glyph names
for glyph in font.pGlyphs():
	glyph_name = glyph.name
	do_update = False

	# - Basic glyph name
	if glyph_name in glyph_rename_dict.keys():
		print('WARN:\tGlyph name: /{}; Rename: /{};'.format(glyph_name, glyph_rename_dict[glyph_name]))
		glyph.name = glyph_rename_dict[glyph_name]
		do_update = True
		

	# - Composite glyph name:
	if '.' in glyph_name: 
		base, suffix = glyph.name.split('.', 1)

		if base in glyph_rename_dict.keys():
			new_name = '{}.{}'.format(glyph_rename_dict[base], suffix)
			print('WARN:\tGlyph name: /{}; Rename: /{};'.format(glyph_name, new_name))
			glyph.name = new_name
			do_update = True

	if do_update:
		try:
			glyph.update()
		except AttributeError:
			pass

# - Finish it
font.update()
print('DONE:\tRenaming glyphs in font and features...')