#FLM: Font: Export Stylespace
# NOTE: Export .stylespace file to be used
# NOTE: for STAT table definition using Statmake tool
# ----------------------------------------
# (C) Vassil Kateliev, 2024 (http://www.kateliev.com)
# (C) Karandash Type Foundry
#-----------------------------------------
# www.typerig.com


# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------
import os
import plistlib

import fontlab as fl6
import fontgate as fgt

from PythonQt import QtCore, QtGui
from typerig.proxy.fl.objects.font import pFont

# - Fuctions ---------------------
def parse_location_str(location_string):
	# - FL location string parse dictionary
	equation_sign = '='
	delimiter_sign = ','
	default_start = '('
	default_end = ')'
	
	# - Process
	location_list = [item.strip().replace(default_start,'').replace(default_end,'').split(equation_sign) + [default_start in item] for item in location_string.split(delimiter_sign)]
	return location_list

def parse_axis(axis):
	axis_data = {'name':axis.name, 'tag':axis.tag, 'locations':[]}
	location_list_str = parse_location_str(axis.instances2string())
	
	for name, value, default in location_list_str:
		location_dict = {'name':name, 'value':axis.checkValue(float(value))}
		if default: location_dict['flags'] = ['ElidableAxisValueName']
		axis_data['locations'].append(location_dict)

	return axis_data

# - Process --------------------------
app_version = '1.0'
app_name = '[SG] Export Stylespace'

font = pFont()
curr_path = os.path.split(font.fg.path)[0]
export_data = {'axes':[parse_axis(axis) for axis in font.fl.axes]}

export_file = QtGui.QFileDialog.getSaveFileName(None, '{} : {}'.format(app_name, app_version), str(curr_path), 'Property List (*.stylespace)')

if len(export_file):
	with open(export_file, 'wb') as exportFile:
		plistlib.dump(export_data, exportFile)

print('DONE:\tSaving stylespace: {}'.format(export_file))
