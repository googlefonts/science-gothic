# SCRIPT:   SG Rename Fonts
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2024         (http://www.kateliev.com)
#------------------------------------------------------------
# No warranties. By using this you agree
# that you use it at your own risk!

__version__ = 1.0

# - Dependencies --------------------------------------------
import os
import argparse

# -- String -------------------------------------------------
tool_name = 'SG Rename Fonts'
tool_description = 'A tool for executing bulk font file renames.'

# - Config --------------------------------------------------
font_style_abbrev = [
					('Black', 'Blk'),
					('Bold', 'Bd'),
					('Caps', 'Cp'),
					('Compressed', 'Cmp'),
					('Condensed', 'Cnd'),
					('Contrast','Cntr'),
					('Demi', 'D'),
					('Display', 'Dsp'),
					('Expanded','Exp'),
					('Extended', 'Ext'),
					('Extra', 'X'),
					('Grunge', 'Grn'),
					('Heavy', 'Hv'),
					('High','Hi'),
					('Italic', 'It'),
					('Light', 'Lt'),
					('Maximum','Max'),
					('Medium', 'Md'),
					('Narrow', 'Nw'),
					('Oblique', 'Ob'),
					('Regular', 'Reg'),
					('Sans', 'Sans'),
					('Semi', 'Sm'),
					('Thin', 'Th'),
					('Ultra','Ult'),
]

font_style_abbrev_dict = dict(reversed(sorted(font_style_abbrev, key=lambda i: len(i[1]))))

# - Functions -------------------------------------------------

def rename_files(folder_path, replacement_dict):
	# - Iterate through all files in the specified folder
	for filename in os.listdir(folder_path):
		new_filename = filename
		
		# - Replace occurrences of keys in the dictionary with their corresponding values
		for key, value in replacement_dict.items():
			new_filename = new_filename.replace(key, value)
		
		# - Create the full old and new file paths
		old_file_path = os.path.join(folder_path, filename)
		new_file_path = os.path.join(folder_path, new_filename)
		
		# - Rename the file
		os.rename(old_file_path, new_file_path)
		print(f'REN: {old_file_path} --> {new_file_path}')


# - Run ---------------------------------------------------------
arg_parser = argparse.ArgumentParser(prog=tool_name, description=tool_description, formatter_class=argparse.RawDescriptionHelpFormatter)
arg_parser.add_argument('folder_path', type=str, help='The path to the folder containing the files to be renamed.')

args = arg_parser.parse_args()
rename_files(args.folder_path, font_style_abbrev_dict)