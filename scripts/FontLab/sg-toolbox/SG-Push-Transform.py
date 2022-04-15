#FLM: SG: Push Transform
#Note: Push shape transformation data to predefined layers
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2022 	(http://www.kateliev.com)
# (C) Karandash Type Foundry 		(http://www.karandash.eu)
#------------------------------------------------------------

#------------------------------------------------------------
# PROJECT: Science Gothic - Variable Font (Google)
# BY: Thomas Phinney <thomas@thefontdetective.com>
# HOME: https://github.com/tphinney/science-gothic/issues
#------------------------------------------------------------

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependancies
from __future__ import absolute_import, print_function

import fontlab as fl6
import fontgate as fgt
import FL as legacy
import PythonQt as pqt

from typerig.proxy.fl.objects.font import pFont
from typerig.proxy.fl.objects.glyph import eGlyph
from typerig.proxy.fl.objects.node import eNode

# - Init -----------------------------
font = pFont()
glyph = eGlyph()

# Warning: Solution is not universal, it just relies on the last part of the layer name
search_layers_suffix = ' S' # Last part of the layer name
layer_pairs = [(layer, layer + search_layers_suffix) for layer in font.masters() if search_layers_suffix not in layer]

# - Process
for layer_in, layer_out in layer_pairs:
	shapes_in = glyph.shapes(layer_in)
	shapes_out = glyph.shapes(layer_out)

	if len(shapes_in) == len(shapes_out):
		for shi in range(len(shapes_in)):
			shapes_out[shi].fl_transform = shapes_in[shi].fl_transform
	
glyph.updateObject(glyph.fl, '%s: Push transformations to *%s layers.' %(glyph.name, search_layers_suffix))
