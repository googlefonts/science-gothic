#FLM: Font: Report Bad Recipes
# NOTE: Find presumably bad recipes that use non mark glyps
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
import pprint

# - Init --------------------------
collect_output = {}
font = pFont()
all_recipes = ['{}{}'.format(glyph.name,glyph.layer('Regular').recipe) for glyph in font.pGlyphs()]

# - Non mark glyphs as reported by FontBakey - Issue #321
not_marks = set('/acute/breve/cedilla/circumflex/dieresis/dotaccent/grave/hungarumlaut/ijdot/macron/ogonek/ring/tilde/underscore/uni02C7'.split('/'))
not_marks = [accent for accent in not_marks if len(accent) and accent != ' ']

# - Process ------------------------
for accent in not_marks:
	for recipe in all_recipes:
		if all([accent in recipe,
			  	accent +'comb' not in recipe, 
			  	accent not in recipe.split('=',1)[0]]): 
			
			collect_output.setdefault(accent,[]).append(recipe)

# - Output
pprint.pprint(collect_output)