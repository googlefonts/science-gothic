# FontLab > UFO+Designspace+FontMake workflow:

This is how the original Science Gothic team did it. If you are working directly with UFO as the masters, instead of a FontLab file, you will skip to near the end of this process (and there is nothing much special about it).

We use a FontLab script, which is here in the repo. It is assumed you have these installed and know how to run scripts from FontLab.

1. Convert outlines to TT with `Tools > Actions > Basics > Convert to TT Curves` (be sure to set "All Masters" at top, and check "Apply to entire font" at bottom left)
1. Run _Font: Check QA_ script that is in the scripts folder within FL. (Note that "_SG-UFO-Prepare.py_" is basically the same script, only it deletes problem glyphs! But the project is no longer in early stages, so deleting glyphs to make the font build is no longer an acceptable tradeoff.)
1. Manually decompose problem glyphs not caught by the script. *  (Currently: /notequal)
1. Run _Font: Check QA_ script again to verify there are no remaining problem glyphs.
1. Check _Features Panel > “Hamburger” menu (top left) > Include Classes:  _Kerning_ and _OpenType_  should be checked (on); _Tags_ and _Virtual Tags_ should be unchecked (off)
1. Delete any [mark] [mkmk] and [kern] features from the _Features Panel_; then from the hamburger menu, recreate them
1. Export your UFO+Designspace
1. Run fontmake from the command line, in the same folder as the output file:
`fontmake -m *.designspace -o variable --keep-overlaps` (if you only have one designspace file in the folder)
or 
`fontmake -m ScienceGothic-3a-18m.designspace -o variable --keep-overlaps` (substitute exact file name if different)
----
* Running the script will not always find every broken glyph. For example, at one point /zero.zero was the ultimate evil. It was compatible and did not use a mixed reference, but nevertheless fontmake would result an error. (Eventually Thomas rebuilt it and the problem went away.) If you encounter a case like this at the fontmake stage later on, back up to this point andfix (flatten) the incompatible characters, even though the script shows no reason for a problem.
