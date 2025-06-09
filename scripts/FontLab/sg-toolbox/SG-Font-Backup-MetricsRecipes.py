#FLM: Backup: Metric Recipes
# NOTE: Works across layers that should be equal
# ----------------------------------------
# (C) Vassil Kateliev, 2019 (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
#-----------------------------------------
# www.typerig.com

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependencies -----------------
from pathlib import Path
import json

import fontlab as fl6

from typerig.proxy.fl.objects.glyph import pGlyph
from typerig.proxy.fl.objects.font import pFont

# - Init ------------------------------------------------
app_version = '1.0'
app_name = '[SG] Backup: Metric Recipes'

font = pFont()
process_glyphs = font.pGlyphs()

font_path = Path(font.fl.path)
save_filename = font_path.parent / Path(str(font_path.stem) + '-metric-backup.json')


# - Process --------------------------------------------
print(f'{app_name}, {app_version}:')
check_count = 0
backup_metric_dict = {}

for work_glyph in process_glyphs:
	lsb, rsb = work_glyph.getSBeq()

	if len(lsb) or len(rsb):
		backup_metric_dict[work_glyph.name] = {'LSB':str(lsb), 'RSB':str(rsb)}


save_filename.write_text(json.dumps(backup_metric_dict, indent=2))

# - Finish --------------------------------------------
print(f'{app_name}, {app_version}: {check_count} Glyph metric recipes saved to: {save_filename}.')


