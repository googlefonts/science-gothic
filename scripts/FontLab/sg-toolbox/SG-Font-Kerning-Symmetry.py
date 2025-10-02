#FLM: Font: Audit Kerning Symmetry
# NOTE: Works across layers that should be equal
# ----------------------------------------
# (C) Vassil Kateliev, 2025 (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
#-----------------------------------------
# www.typerig.com

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------
from itertools import combinations

import fontlab as fl6
import fontgate as fgt
import PythonQt as pqt

from typerig.proxy.fl.objects.glyph import pGlyph
from typerig.proxy.fl.objects.font import pFont
from typerig.core.objects.collection import extBiDict


# - Helper ------------------------------------------------------
def build_kern_pairs(dst_names, layer_kerning, class_data, class_kern=True):
	# - Init
	dst_pairs = []

	# - Build Destination pairs
	for pair in dst_names:
		left, right = pair
		modeLeft, modeRight = False, False
		
		
		if left in class_data['KernLeft'].inverse:
			left = class_data['KernLeft'].inverse[left][0]
			modeLeft = True

		elif 'KernBothSide' in class_data and left in class_data['KernBothSide'].inverse:
			left = class_data['KernBothSide'].inverse[left][0]
			modeLeft = True

		if right in class_data['KernRight'].inverse:
			right = class_data['KernRight'].inverse[right][0]
			modeRight = True

		elif 'KernBothSide' in class_data and right in class_data['KernBothSide'].inverse:
			right = class_data['KernBothSide'].inverse[right][0]
			modeRight = True

		if class_kern: 
			dst_pairs.append(((left, modeLeft), (right, modeRight)))
		else:
			dst_pairs.append((left, right))

	return dst_pairs

# - Init ------------------------------------------------
app_version = '1.0'
app_name = '[SG] Font: Audit Kerning Symmetry'
check_pairs = list(combinations('AVTO', 2))

pairs_processed = 0
font = pFont()

for layer_name in font.masters():
	temp_data = {}
	pairs_processed = 0
	
	layer_kerning = font.kerning(layer_name)
	temp_classes = font.kerning_groups_to_dict(layer_name, False, False)
	
	for key, value in temp_classes.items():
		temp_data.setdefault(value[1], {}).update({key : value[0]})

	layer_classes = {key:extBiDict(value) for key, value in temp_data.items()}
	layer_pairs = build_kern_pairs(check_pairs, layer_kerning, layer_classes, True)
	
	for pair in layer_pairs:
		print(layer_name, pair, layer_kerning.get(pair))

	#print(f'{app_name}, {app_version}: Layer: {layer_name}; Pairs: {pairs_processed}; Filter applied: {cutoff_values}.')

# - Finish --------------------------------------------
if pairs_processed > 0 :
	font.update()
	font.updateObject(font.fl, 'Font kerning updated!', verbose=True)
	print(f'{app_name}, {app_version}: Done.')

