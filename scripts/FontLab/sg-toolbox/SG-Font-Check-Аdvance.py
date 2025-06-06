#FLM: Check: Metric inconsistency 
# NOTE: Works across layers that should be equal
# ----------------------------------------
# (C) Vassil Kateliev, 2019 (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
#-----------------------------------------
# www.typerig.com

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------

import fontlab as fl6

from typerig.proxy.fl.objects.glyph import pGlyph
from typerig.proxy.fl.objects.font import pFont

# - Init ------------------------------------------------
app_version = '1.3'
app_name = '[SG] Check: Metric inconsistency'

font = pFont()
process_glyphs = font.pGlyphs()

test_layers = [	('Lt', 'Lt Ctr'),
				('Lt Cnd', 'Lt Cnd Ctr'),
				('Lt Exp', 'Lt Exp Ctr'),
				('Lt S', 'Lt Ctr S'),
				('Lt Cnd S', 'Lt Cnd Ctr S'),
				('Lt Exp S', 'Lt Exp Ctr S')]

delta_tolerance = 1

# - Process --------------------------------------------
print(f'{app_name}, {app_version}:')
check_count = 0

for work_glyph in process_glyphs:
	bug_found = False
	
	for base_layer, check_layer in test_layers:
		log = f'[{base_layer} / {check_layer}]'
		
		if len(work_glyph.components(base_layer)): continue
		
		base_layer_advance = work_glyph.getAdvance(base_layer)
		check_layer_advance = work_glyph.getAdvance(check_layer)
		
		base_layer_lsb = work_glyph.getLSB(base_layer)
		check_layer_lsb = work_glyph.getLSB(check_layer)
		
		if abs(base_layer_advance - check_layer_advance) >= delta_tolerance:
			work_glyph.setAdvance(base_layer_advance, check_layer)
			log += f'\tADV: {base_layer_advance} / {check_layer_advance};'

		if abs(base_layer_lsb - check_layer_lsb) >= delta_tolerance:
			work_glyph.setLSB(base_layer_lsb, check_layer)
			log += f'\tLSB: {base_layer_lsb} / {check_layer_lsb};'
		
		if 'LSB' in log or 'ADV' in log:
			print(f'WARN:\t/{work_glyph.name} | {log}')
			#work_glyph.setSBeq(('',''), check_layer)
			bug_found = True

	if bug_found: check_count += 1

# - Finish --------------------------------------------
print(f'{app_name}, {app_version}: Found {check_count} glyphs with metric problems.')


