#FLM: Font: Smooth kerning
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
windowize = lambda data, size=3: [data[i:i+size] for i in range(0, len(data), size)]

def smooth_windows_column_aware(data, window_size=3, spike_threshold=10, round_5=True):
	"""
	Smooths flat data array of N-sized windows.
	- Detects spikes by analyzing window + column trends
	- Adjusts only the spikes, keeps other values mostly intact

	Parameters:
	- data: flat list of numbers
	- window_size: number of elements per window (was triads=3)
	- spike_threshold: sensitivity to spikes
	- round_5: whether to round smoothed values to nearest multiple of 5
	"""
	n_windows = len(data) // window_size
	windows = [data[i*window_size : i*window_size+window_size] for i in range(n_windows)]
	
	# Transpose to get columns
	columns = [ [windows[t][c] for t in range(n_windows)] for c in range(window_size) ]
	
	# Result storage
	result = []

	for t in range(n_windows):
		new_window = []
		for c in range(window_size):
			val = windows[t][c]
			# Window neighbors
			window_vals = windows[t]
			window_median = sorted(window_vals)[len(window_vals)//2]
			
			# Column values
			col_vals = columns[c]
			col_median = sorted(col_vals)[len(col_vals)//2]
			
			# Spike detection: if val > window median + threshold AND val > column median + threshold
			if val - window_median > spike_threshold and val - col_median > spike_threshold:
				# Smooth: weighted average of window neighbors (excluding itself) + column median
				neighbors = [v for idx,v in enumerate(window_vals) if idx != c]
				smooth_val = (sum(neighbors) + col_median) / (len(neighbors)+1)
				
				if round_5:
					smooth_val = 5 * round(smooth_val / 5)
				
				new_window.append(smooth_val)
			else:
				new_window.append(val)  # keep original if not spike
		result.extend(new_window)
	return result

# - CFG -----------------------------------------------
app_version = '1.5'
app_name = '[SG] Font: Smooth kerning'

base_layer = 'Regular'
window_size = 3 		# Window of logically connected masters, ex: Light - Regular - Bold
smooth_treshold = 10	# Spike detect value
round_values = True 	# Round kern values to 5u

# - Init ------------------------------------------------
font = pFont()
font_masters = font.masters() # Take just once
do_update = False

# - If the cfg defined layer is missing, just default to the current one
if not base_layer in font_masters:
	base_layer = None 

# - Assume that there is matched kerning across masters
base_pairs = [pair.asTuple() for pair in font.kerning(base_layer).keys()]

# - Extract all kerning objects
font_kerning_data = [font.kerning(layer_name) for layer_name in font_masters]

for pair in base_pairs:
	pair_updated = False
	pair_data = [layer_kerning.get(pair) for layer_kerning in font_kerning_data]
	
	if None in pair_data: 
		temp_return = dict(zip(font_masters, pair_data))
		print(f'WARN: Pair: {pair} Inconsistent! Check: {temp_return}')
		continue
	
	adjusted_values = smooth_windows_column_aware(pair_data, window_size, smooth_treshold, round_values)
	
	for i in range(len(pair_data)):
		if pair_data[i] != adjusted_values[i]:
			font_kerning_data[i].set(pair, adjusted_values[i])
			do_update = True
			pair_updated = True

	if pair_updated:
		print(f'DONE: Pair: {pair} Adjusted: {pair_data} -> {adjusted_values}')

# - Finish --------------------------------------------
if do_update:
	font.update()
	font.updateObject(font.fl, 'Font kerning updated!', verbose=True)

print(f'{app_name}, {app_version}: Done.')
