#FLM: Font: Bind metrics to recipes
# NOTE: Find presumably bad recipes that use non mark glyps
# ----------------------------------------
# (C) Vassil Kateliev, 2025 (http://www.kateliev.com)
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
import pprint

# - Init --------------------------
font = pFont()
process_glyphs = font.selected_pGlyphs()

# - Process ------------------------
for glyph in process_glyphs:
	layer_recipe=''

	for layer_name in font.masters():
		layer_recipe = glyph.layer(layer_name).recipe.replace(' ','').replace('=','')
		layer_recipe = layer_recipe[:layer_recipe.index('@')]
		glyph.setLSBeq(f'={layer_recipe}', layer_name)
		glyph.setRSBeq(f'={layer_recipe}', layer_name)

	glyph.update()
	glyph.updateObject(glyph.fl, 'Bind Metrics')
	print(f'DONE:\t/{glyph.name} bound with recipe: ={layer_recipe}')

