#FLM: Check: Anchor inconsistency 
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
app_version = '1.0'
app_name = '[SG] Check: Anchor inconsistency'

font = pFont()
process_glyphs = font.pGlyphs()

test_layers = [	('Lt', 'Lt Ctr'),
				('Lt Cnd', 'Lt Cnd Ctr'),
				('Lt Exp', 'Lt Exp Ctr'),
				('Lt S', 'Lt Ctr S'),
				('Lt Cnd S', 'Lt Cnd Ctr S'),
				('Lt Exp S', 'Lt Exp Ctr S')]

delta_tolerance = 2
isclose = lambda a, b: abs(int(a.point.x()) - int(b.point.x())) >= delta_tolerance or abs(int(a.point.y()) - int(b.point.y())) >= delta_tolerance

# - Process --------------------------------------------
print(f'{app_name}, {app_version}:')
check_count = 0

for work_glyph in process_glyphs:
	bug_found = False
	
	for base_layer, check_layer in test_layers:
		log = f'[{base_layer} / {check_layer}] '
		
		if len(work_glyph.components(base_layer)): continue
		
		base_layer_anchors = work_glyph.anchors(base_layer)
		

		for anchor in base_layer_anchors:
			check_anchor = work_glyph.findAnchor(anchor.name, check_layer)
			
			if check_anchor is not None:
				if isclose(anchor, check_anchor):
					log += anchor.name + ' '
					bug_found = True

					# - Force set anchor coordinates
					check_anchor.point = anchor.point
					
			else:
				print(f'ERROR:\t/{work_glyph.name} | Missing anchor: {anchor.name} on layer: {check_layer}')
		
		
		if bug_found: 
			print(f'WARN:\t/{work_glyph.name} | {log}')
			work_glyph.update()
			#work_glyph.updateObject(work_glyph.fl, verbose=False)
		

	if bug_found: check_count += 1

# - Finish --------------------------------------------
print(f'{app_name}, {app_version}: Found {check_count} glyphs with anchor problems.')


