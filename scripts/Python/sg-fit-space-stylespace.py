# Script: Fit designspace to userspace and generate stylespace
# Note: Will generate a XML snippet to be inserted into 
# Note: .stylespace file
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2025     (http://www.kateliev.com)
#------------------------------------------------------------

# - Dependacies 
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# - Helpers --------------------------------------------
# - Handle Stylespace  ---------------------------------
# - XML -> Python dict
def xml_to_axis_dict(xml_elem):
	items = list(xml_elem)
	result = {}

	flags = None
	name = None
	value = None

	i = 0
	while i < len(items):
		key = items[i].text
		val_elem = items[i+1]

		if key == "flags":
			flags = [child.text for child in val_elem.findall("string")]
		elif key == "name":
			name = val_elem.text
		elif key == "value":
			value = float(val_elem.text)

		i += 2

	# Apply ElidableAxisValueName rule
	if flags and "ElidableAxisValueName" in flags:
		name = f"({name})"

	result[name] = value
	return result

def xml_to_full_dict(xml_string):
	root = ET.fromstring(xml_string)
	result = {}
	for dict_elem in root.findall("dict"):
		result.update(xml_to_axis_dict(dict_elem))
	return result

# - Python dict -> XML
def axis_dict_to_xml(data):
	root = ET.Element("array")  # container for multiple <dict>
	
	for name, value in data.items():
		dict_elem = ET.SubElement(root, "dict")

		# Check if name is "elidable"
		elidable = name.startswith("(") and name.endswith(")")
		plain_name = name[1:-1] if elidable else name

		# Add flags if elidable
		if elidable:
			key_elem = ET.SubElement(dict_elem, "key")
			key_elem.text = "flags"
			array_elem = ET.SubElement(dict_elem, "array")
			string_elem = ET.SubElement(array_elem, "string")
			string_elem.text = "ElidableAxisValueName"

		# Add name
		key_elem = ET.SubElement(dict_elem, "key")
		key_elem.text = "name"
		name_elem = ET.SubElement(dict_elem, "string")
		name_elem.text = plain_name

		# Add value
		key_elem = ET.SubElement(dict_elem, "key")
		key_elem.text = "value"
		value_elem = ET.SubElement(dict_elem, "real")
		value_elem.text = str(value)

	return root

def axis_dict_to_xml_string(data, pretty=True):
	root = axis_dict_to_xml(data)
	xml_bytes = ET.tostring(root, encoding="utf-8")
	if pretty:
		dom = minidom.parseString(xml_bytes)
		return dom.toprettyxml(indent="\t")
	return xml_bytes.decode("utf-8")

# - Fit designspace ----------------------------------------------------------
def fit_space(design_space, user_space):
	d_min, d_max = min(design_space), max(design_space)
	u_min, u_max = min(user_space), max(user_space)
	scale = (u_max - u_min) / (d_max - d_min)
	return [(x - d_min) * scale + u_min for x in design_space]

# - Config --------------------------------------------------------------------
axis_string='UltraCondensed=0, ExtraCondensed=125, Condensed=250, SemiCondensed=375, (Normal)=500, SemiExpanded=675, Expanded=750, ExtraExpanded=1000'
user_space = [50,200]

# - Init
axis_str_list = [item.strip().split('=') for item in axis_string.split(',')]
design_space = {name:float(value) for name,value in axis_str_list}

# - Result
new_designspace = dict(zip(design_space.keys(),fit_space(design_space.values(), user_space)))
print(axis_dict_to_xml_string(new_designspace))