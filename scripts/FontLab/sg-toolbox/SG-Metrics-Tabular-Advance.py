#FLM: Metrics: Set tabular Advance 
# ----------------------------------------
# (C) Vassil Kateliev, 2024 
#-----------------------------------------
# www.typerig.com

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------

import statistics
import fontlab as fl6
import fontgate as fgt

from typerig.proxy.fl.objects.font import pFont
from typerig.proxy.fl.objects.glyph import pGlyph


# - Init
font = pFont()
width_table = {layer:{g.name:g.getAdvance(layer) for g in font.selected_pGlyphs()} for layer in font.masters()}
median_table = {layer:(list(data.keys()), statistics.median(data.values())) for layer, data in width_table.items()}

# - Run
for layer_name, med_data in median_table.items():
	glyph_list, layer_median = med_data
	
	for glyph_name in glyph_list:
		glyph = font.glyph(glyph_name)
		glyph.setAdvance(layer_median, layer_name)
	
	print('DONE:\tSetting median advance of {}u for glyphs /{} on layer :{}'.format(layer_median, '/'.join(glyph_list), layer_name))

# - Finish
print('Done.')