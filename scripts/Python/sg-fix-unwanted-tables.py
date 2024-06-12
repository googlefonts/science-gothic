#!/usr/bin/env python3

# SCRIPT: SG-FIX-UNWANTED-TABLES
# NOTE: Remove a predefined set of tables from the finished fonts
# -----------------------------------------------------------
# PROJECT: Science Gothic
#------------------------------------------------------------
# NOTE: A modified copy of 
# NOTE: #https://github.com/googlefonts/gftools/blob/main/Lib/gftools/scripts/fix_unwanted_tables.py
# ----------------------------------------------------------
#
# ORIGINAL DISCLAIMER:
#
# Copyright 2019 The Google Font Tools Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# See AUTHORS.txt for the list of Authors and LICENSE.txt for the License.
#

import argparse
from fontTools.ttLib import TTFont
import logging
# from gftools.fix import remove_tables

# - Glued from gftools.fix --------------------------------------
log = logging.getLogger(__name__)

UNWANTED_TABLES = frozenset(
    [
        "Debg",
        "DSIG", # NOTE: Added for https://github.com/googlefonts/gftools/issues/564
        "FFTM",
        "MVAR", # NOTE: Added for GS on 20 Feb 2024
        "prop",
        "TSI0",
        "TSI1",
        "TSI2",
        "TSI3",
        "TSI5",
        "TTFA"
    ]
)

def remove_tables(ttFont, tables=None):
    """Remove unwanted tables from a font. The unwanted tables must belong
    to the UNWANTED_TABLES set.

    Args:
        ttFont: a TTFont instance
        tables: an iterable containing tables remove
    """
    tables_to_remove = UNWANTED_TABLES if not tables else frozenset(tables)
    font_tables = frozenset(ttFont.keys())

    tables_not_in_font = tables_to_remove - font_tables
    if tables_not_in_font:
        log.warning(
            f"Cannot remove tables '{list(tables_not_in_font)}' since they are "
            f"not in the font."
        )

    required_tables = tables_to_remove - UNWANTED_TABLES
    if required_tables:
        log.warning(
            f"Cannot remove tables '{list(required_tables)}' since they are required"
        )

    tables_to_remove = UNWANTED_TABLES & font_tables & tables_to_remove
    if not tables_to_remove:
        return
    log.info(f"Removing tables '{list(tables_to_remove)}' from font")
    for tbl in tables_to_remove:
        del ttFont[tbl]

# - Main -------------------------------------------------
def parse_tables(table_string):
    return table_string.split(",")

def main(args=None):
    description = "Removes unwanted tables from one or more font files"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-t", "--tables", type=str, help="One or more comma separated table names"
    )
    parser.add_argument("FONTPATH", nargs="+", help="One or more font files")

    args = parser.parse_args(args)

    tables = parse_tables(args.tables) if args.tables else None

    for fontpath in args.FONTPATH:
        ttfont = TTFont(fontpath)
        remove_tables(ttfont, tables)
        ttfont.save(fontpath)


if __name__ == "__main__":
    main()
