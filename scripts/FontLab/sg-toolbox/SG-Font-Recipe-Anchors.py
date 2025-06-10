#FLM: Check: Anchor recipes 
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

# - Process --------------------------------------------
print(f'{app_name}, {app_version}:')
check_count = 0

for work_glyph in process_glyphs:
	bug_found = False
	
	
	for layer_name in font.masters():
		for anchor in work_glyph.anchors(layer_name):
			if anchor.expressionX or anchor.expressionY:
				print(f'WARN:\t/{work_glyph.name} | {anchor.name}')
				continue

		
		

# - Finish --------------------------------------------
print(f'{app_name}, {app_version}: Found {check_count} glyphs with anchor problems.')


