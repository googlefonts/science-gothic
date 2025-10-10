# Script: Font Instance Name Shortener
# Note: Compose, shorten and normalize VF instance names
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2025     (http://www.kateliev.com)
# (C) Karandash Type Foundry        (http://www.karandash.eu)
#------------------------------------------------------------

#------------------------------------------------------------
# PROJECT: Science Gothic - Variable Font (Google)
# BY: Thomas Phinney <thomas@thefontdetective.com>
# HOME: https://github.com/tphinney/science-gothic/issues
#------------------------------------------------------------

import json
import re

# - Config ---------------------------------------------------------
font_style_abbrev = [
    ('Black', 'Blk'), ('Bold', 'Bd'), ('Caps', 'Cp'), ('Compressed', 'Cmp'),
    ('Condensed', 'Cnd'), ('Contrast','Cntr'), ('Demi', 'D'), ('Display', 'Dsp'),
    ('Expanded','Exp'), ('Extended', 'Ext'), ('Extra', 'X'), ('Grunge', 'Grn'),
    ('Heavy', 'Hv'), ('High','Hi'), ('Italic', 'It'), ('Light', 'Lt'),
    ('Maximum','Max'), ('Medium', 'Md'), ('Narrow', 'Nw'), ('Oblique', 'Ob'),
    ('Regular', 'Reg'), ('Sans', 'Sans'), ('Semi', 'Sm'), ('Thin', 'Th'),
    ('Ultra','Ult')
]

abbrev_dict = dict(font_style_abbrev)

font_name = 'Science Gothic'

priority = {
    "wt": 421,
    "wd": 500,
    "co": 0,
    "sl": 0
}

# - Helper functions ------------------------------------------------
def abbreviate_name(name, max_len=32):
    '''
    Convert camel-case or concatenated names to spaced abbreviations
    and ensure length <= max_len.
    '''
    # - Split camel-case / concatenated words
    words = re.findall(r'[A-Z][a-z]*|[0-9]+', name)
    
    # - Apply abbreviation if exists
    abbr_words = [abbrev_dict.get(w, w) for w in words]
    
    # - Join and truncate if necessary
    result = ' '.join(abbr_words)
    
    if len(result) > max_len:
        result = result[:max_len].rstrip()
        print(result)

    return result

def sort_key(instance):
    loc = instance["location"]
    
    # Compute "priority" score for each axis: 0 if it matches preferred value, 1 otherwise
    wt_score = 0 if loc.get("wt", 0) == priority["wt"] else 1
    wd_score = 0 if loc.get("wd", 0) == priority["wd"] else 1
    co_score = 0 if loc.get("co", 0) == priority["co"] else 1
    sl_score = 0 if loc.get("sl", 0) == priority["sl"] else 1

    # The sort tuple:
    # Priority matches come first (0), then non-matches (1), and finally the actual value to maintain natural order
    return (wt_score, loc.get("wt", 0),
            wd_score, loc.get("wd", 0),
            co_score, loc.get("co", 0),
            sl_score, -loc.get("sl", 0))

# - Main function ---------------------------------------------------------
def process_font_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_instances = []

    for inst in data['instances']:
        try:
            family_name = inst['tfn']
        except KeyError:
            family_name = font_name

        style_name = inst['tsn']

        if len(family_name + style_name) > 30:
            new_style = abbreviate_name(inst['name'])
        else:
            new_style = style_name

        new_inst = inst.copy()
        #new_inst['name'] = new_style
        new_inst['tsn'] = f'{style_name}'
        new_inst['sgn'] = f'{family_name} {new_style}'

        new_instances.append(new_inst)

        new_instances.sort(key=sort_key)


    new_data = {
        'dataType': data.get('dataType', 'com.fontlab.info.instances'),
        'instances': new_instances
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2)
    print(f'Processed JSON saved to {output_file}')

# - Example usage
if __name__ == '__main__':
    input_json = r'd:\1.json'
    output_json = 'science_gothic_instances.json'
    process_font_json(input_json, output_json)
