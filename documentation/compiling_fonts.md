# Our FontLab > UFO+Designspace+FontMake workflow:

This is how we get from FontLab VFC files to final variable TTFs. 

If you are working directly with UFOs only, and not starting with the FontLab source, you would skip to point 9 below.

For point 1 and 3, we use a FontLab script, which is here in the repo. It is assumed you have this script installed and know how to run scripts from FontLab.

1. Run _Font: Check QA_ script that is in the scripts folder within FL. (Note that "_SG-UFO-Prepare.py_" is basically the same script, only it deletes problem glyphs! But the project is no longer in early stages, so deleting glyphs to make the font build is no longer an acceptable tradeoff.)
1. Correct any problem glyphs by decomposing them, etc. Manually decompose problem glyphs not caught by the script. *  (Currently none)
1. If problems were fixed, Run _Font: Check QA_ again.
1. Convert outlines to TT with `Tools > Actions > Basics > Convert to TT Curves` (be sure to set "All Masters" at top, and check "Apply to entire font" at bottom left)
1. Check _Features Panel > “Hamburger” menu (top left) > Include Classes:  _Kerning_ and _OpenType_  should be checked (on); _Tags_ and _Virtual Tags_ should be unchecked (off)
1. Delete any [mark] [mkmk] and [kern] features from the _Features Panel_; then from the panel’s hamburger menu, recreate them
1. In the _Kerning panel_, use the Match Kerning operation from the “hamburger menu” at the bottom right of the panel.
1. Export your UFO+Designspace (File > Export Font As, select "DesignSpace + UFO" near the bottom)
1. Run fontmake from the command line, in the same folder as the output file:
`fontmake -m *.designspace -o variable --keep-overlaps` (if you only have one designspace file in the folder)
or 
`fontmake -m ScienceGothic[YOPQ,wdth,wght,slnt].designspace -o variable --keep-overlaps` (substitute exact file name if different)
1. Remove MVAR table with gftools `gftools fix-unwanted-tables *.ttf`, as required by https://github.com/tphinney/science-gothic/issues/244
1. Run `gftools-fix-nonhinting.py *.ttf ScienceGothic[YOPQ,wdth,wght,slnt]1.ttf` per https://github.com/tphinney/science-gothic/issues/239
1. run `gftools fix-dsig --autofix *.ttf` (Note: this may need to be the last step in any sequence of fixes) #251
1. Remove old unfixed files
1. Make sure final font file is named correctly, per Google specs. e.g. `ScienceGothic[YOPQ,wdth,wght,slnt].ttf`
1. TESTING steps are part of the compile process, as follows...
1. Run `fontbakery check-googlefonts ScienceGothic[YOPQ,wdth,wght,slnt].ttf`
1. Run `ftxvalidator ScienceGothic[YOPQ,wdth,wght,slnt].ttf`

At this time, we are still fixing some issues identified by FontBakery. It also appears ftxvalidator might not be running properly—TBD.

----
* Running the script will not always find every broken glyph. For example, at one point /zero.zero was the ultimate evil. It was compatible and did not use a mixed reference, but nevertheless fontmake would result an error. (Eventually Thomas rebuilt it and the problem went away.) If you encounter a case like this at the fontmake stage later on, back up to this point and fix (flatten) the incompatible characters, even though the script shows no reason for a problem.
