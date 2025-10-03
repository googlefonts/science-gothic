#FLM: Kern : Audit Kerning Symmetry
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

def getUniGlyph(char, font):
	if '/' in char and char != '//':
		return char.replace('/','')

	return font.fl.findUnicode(ord(char)).name

def round_to_5(n):
	return 5 * round(n / 5)

def calc_value(one, two):
	if one is None: return two
	if two is None: return one

	if 0 <= abs(abs(one) - abs(two)) <= 10:
		return float(round_to_5(min(one, two)))
	else:
		return float(round_to_5((one + two)/2))

# - CFG -----------------------------------------------
app_version = '1.6'
app_name = '[SG] Font: Audit Kerning Symmetry'

check_string = 'A V W Y U X 8 0 T O o v w x : ! * | ` . -'
check_list = ['/a.sc', '/v.sc', '/w.sc', '/y.sc', '/t.sc', '/x.sc', '/o.sc']

skip_layers = ['Ctr']

# - Init ------------------------------------------------
font = pFont()

check_pairs = [(getUniGlyph(item[0].strip(), font), getUniGlyph(item[1].strip(), font)) for item in combinations(check_list + check_string.split(' '), 2)]
reverse_pairs = [tuple(reversed(item)) for item in check_pairs]
pairs_processed = 0

for layer_name in font.masters():
	skip_flag = False
	
	for skip_cond in skip_layers:
		if skip_cond in layer_name: skip_flag=True

	if skip_flag: continue

	# - Process
	temp_data = {}
	pairs_processed = 0
	
	layer_kerning = font.kerning(layer_name)
	temp_classes = font.kerning_groups_to_dict(layer_name, False, False)
	
	for key, value in temp_classes.items():
		temp_data.setdefault(value[1], {}).update({key : value[0]})

	layer_classes = {key:extBiDict(value) for key, value in temp_data.items()}
	layer_pairs = build_kern_pairs(check_pairs, layer_kerning, layer_classes, True)
	layer_pairs_inverse = build_kern_pairs(reverse_pairs, layer_kerning, layer_classes, True)
	
	for pid in range(len(layer_pairs)):
		pair = layer_pairs[pid]
		inverse = layer_pairs_inverse[pid]
		report_pair = check_pairs[pid]

		pair_value = layer_kerning.get(pair)
		inverse_value = layer_kerning.get(inverse)

		if pair_value != inverse_value:
			flag = '. DONE' if None not in (pair_value, inverse_value) else '! WARN'
			new_value = calc_value(pair_value, inverse_value)
			layer_kerning.set(pair, new_value)
			layer_kerning.set(inverse, new_value)
			pairs_processed += 1

			print(f'{flag}: Layer: {layer_name}; Pair: {report_pair}; Non-match: {pair_value}/{inverse_value} => {new_value};')
			

# - Finish --------------------------------------------
if pairs_processed > 0 :
	font.update()
	font.updateObject(font.fl, 'Font kerning updated!', verbose=True)

print(f'{app_name}, {app_version}: Done.')
