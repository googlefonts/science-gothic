#FLM: Font: Interpolate Glyphs
# ----------------------------------------
# (C) Vassil Kateliev, 2019 (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
#-----------------------------------------
# www.typerig.com

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependancies
from typerig.brain import linInterp as lerp
from typerig.glyph import eGlyph
from typerig.proxy import pFont, pGlyph

# - Functions ------------------------------------------
def lerpXY(t0, t1, tx, ty):
	return (lerp(t0[0], t1[0], tx), lerp(t0[1], t1[1], ty))

# - Init ------------------------------------------------
app_version = '0.1'
app_name = '[SG] Interpolate glyphs'
font = pFont()

# -- Config ----------------------------------------------
src_glyph_names = ('k', 'k.new') 	# source glyphs - should be compatible
dst_glyph_name = None 				# None points to current active glyph - you should create one first and it should be a duplicate of one of the sources

tx = .5 							# interpolation time along X
ty = .5 							# interpolation time along Y

# - Process ----------------------------------------------
src_glyph = (font.glyph(src_glyph_names[0], eGlyph), font.glyph(src_glyph_names[1], eGlyph))
dst_glyph = eGlyph() if dst_glyph_name is None else font.glyph(dst_glyph_name, eGlyph)

for layer in font.masters():
	src_array_t0 = src_glyph[0]._getCoordArray(layer).asPairs()
	src_array_t1 = src_glyph[1]._getCoordArray(layer).asPairs()
	process_array = zip(src_array_t0[0], src_array_t1[0])
	dst_array = [lerpXY(item[0], item[1], tx, ty) for item in process_array]
	dst_glyph._setCoordArray(dst_array, layer)

dst_glyph.update()
dst_glyph.updateObject(dst_glyph.fl, 'Done:\t %s %s:\t %s' %(app_name, app_version, dst_glyph.name))




