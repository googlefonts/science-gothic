#FLM: Kern : Kerning Cutoff Filter
# NOTE: Works across layers that should be equal
# ----------------------------------------
# (C) Vassil Kateliev, 2025 (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
#-----------------------------------------
# www.typerig.com

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------
import fontlab as fl6
import fontgate as fgt
import PythonQt as pqt

from typerig.proxy.fl.objects.glyph import pGlyph
from typerig.proxy.fl.objects.font import pFont
from typerig.core.objects.collection import extBiDict

# - Init ------------------------------------------------
app_version = '1.1'
app_name = '[SG] Font: Kerning Cutoff Filter'

cutoff_values = (100., -250.) # Maximum kernig value allowed
pairs_processed = 0

font = pFont()

for layer_name in font.masters():
	#if 'Lt' not in layer_name: continue

	pairs_processed = 0
	layer_kerning = font.kerning(layer_name)

	for kern_pair, kern_value in layer_kerning.items():
		if not min(cutoff_values) <= kern_value <= max(cutoff_values):
			new_kern_value = max(cutoff_values) if kern_value > 0 else min(cutoff_values)
			layer_kerning.set(kern_pair.asTuple(), new_kern_value)
			pairs_processed += 1

	print(f'{app_name}, {app_version}: Layer: {layer_name}; Pairs: {pairs_processed}; Filter applied: {cutoff_values}.')

# - Finish --------------------------------------------
if pairs_processed > 0 :
	font.update()
	font.updateObject(font.fl, 'Font kerning updated!', verbose=True)
	print(f'{app_name}, {app_version}: Done.')

