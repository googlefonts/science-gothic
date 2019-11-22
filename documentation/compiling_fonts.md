# FontLab > UFO+Designspace+FontMake workflow:

1. Convert outlines to TT with `Tools > Actions > Basics > Convert to TT Curves` (be sure to set "All Masters" at top, and check "Apply to entire font" at bottom)
1. Run _SG-UFO-Prepare.py_ that is in the scripts folder within FL. (Currently, this has no effect because everything is OK.)
1. Manually decompose problem glyphs not caught by the script. *  (Currently: /notequal)
1. Run _Font: Check QA_ Script
1. Check _Features Panel > “Hamburger” menu (top left) > Include Classes: _OpenType_ and _Kerning_ should be checked (on); Tags_ should be unchecked (off)
1. Delete any [mark] [mkmk] and [kern] features from the _Features Panel_; then from the hamburger menu, recreate them
1. Export your UFO+Designspace
1. Run fontmake from the command line, in the same folder as the output file:
`fontmake -m *.designspace -o variable --keep-overlaps` (if you only have one designspace file in the folder)
or 
`fontmake -m ScienceGothic-3a-18m.designspace -o variable --keep-overlaps` (substitute exact file name if different)
----
* Running the script will not always clean up every broken glyph. For example, at one point /zero.zero was the ultimate evil. It was compatible and did not use a mixed reference, but nevertheless fontmake would result an error. (Eventually Thomas rebuilt it and the problem went away.) If you encounter a case like this, just delete or fix (flatten) the incompatible characters, even though FL shows no reason for a problem.
