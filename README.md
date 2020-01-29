# Science Gothic
## libre variable font

Science Gothic™ is a variable font with weight, width, contrast and slant axes—the equivalent of 200+ separate fonts. While the medium weight is based closely on the original Bank Gothic typeface from the early 1930s, a lowercase, design axes, and language coverage have been added. Bank Gothic was originally designed by Morris Fuller Benton in 1930–34 for American Type Founders. Science Gothic is a team effort, with primary development by Thomas Phinney, Brandon Buerkle and Vassil Kateliev.

This repo is where development and updates to this project can be found. Source files are updated ~ daily, in FontLab VFJ (vector font JSON) format and occasionally FontLab VFC (binary) format. We regularly also do UFO and compiled variable TTF (mostly variable fonts, rarely also fonts corresponding to masters and instances).

(Particularly major updates are described below, but not every update.)

### DOWNLOAD THE VARIABLE FONT
Get the latest working variable font here: https://github.com/tphinney/science-gothic/tree/master/fonts/variable/UFO%20FontMake


### Bugs
PLEASE report any BUGS OR ISSUES. You can file an issue right here in Github at: https://github.com/tphinney/science-gothic/issues. Or just ask questions on social media, whatever. But feedback is welcome!

### Building Fonts
Our process for building fonts from our FontLab VFC/VFJ sources > UFO > FontMake > TTF (variable font) is now documented here: https://github.com/tphinney/science-gothic/blob/master/documentation/compiling_fonts.md


## Release Notes

### 17 November 2019

- Slant axis is enabled! Note the form change for /a and /f when they get more than half slanted. This has generated a fair number of bugs for some glyphs in their slanted versions, but nothing unmanageable. 
- Have started editing glyphs to tweak their shapes where slant does too much distortion of weight or stroke. Mainly diagonal strokes (think: A K N M R 2 4 7 & ?) and big curves (not many in this typeface, but they include: D 6 9)
- Kerning classes have all been created; kerning is well underway

### 1 November 2019

Primary design work was basically done. Just a few details here and there to fix. We are now entering the endgame! For the next three weeks or so, we will:

- create kerning classes and do kerning
- create the Slant axis, slanted glyphs, and add form change for just a very few (/a for certain, maybe /f)
- fix bugs and address any issues discovered

98.5% done glyph design work

### 14 October 2019

Made significant org/name changes to the former Contrast axis, now called “Y Opaque” ('YOPQ' axis tag). Instead of going from 0 – 100 (low to high) it goes from 18 to 124 (high to low contrast) representing the thickness of capital horizontal strokes, in thousandths of an em, at the default Medium weight. The default style is still low contrast, which is 124, at the “high” end of the horizontal stroke-thickness scale.

77% done glyph design work.

### 18 September 2019

Added UFO sources, and first variable TTF built from UFO + FontMake (with latest FontMake and Python) rather than from exporting from FontLab. Although FontLab VI uses UFO + FontMake internally for its variable font generation, it uses an older version of FontMake. The UFO + FontMake approach makes it easier for future development to be made with any UFO-compatible font editor. See https://github.com/tphinney/science-gothic/issues/91 for details.

49% done glyph design work.

### 5 September 2019

Second variable font build. About 200 meaningful characters, including very nearly complete support for both English and Russian. 37% done glyph design work.

Around this time we had the last few contributions from Igor Freiberger. Thanks!

### 29 August 2019

Added first built variable font! Thought it was buggy, but turns out that is just Illustrator. Font is lovely in Axis-Praxis. https://recordit.co/g9KnZq2Dbv . Also added separate fonts for instances (ouch 104 fonts!). And the .designspace file. ~ 26% done glyph design work.

### 15 August 2019
16% done glyph design work.

### 10 August 2019

Added recipes to build auto layers.


### 8 August 2019

Added folder structure!

Masters folder:
- added variable font-in-progress in VFJ format (FontLab JSON text format)
- added Readme about formats etc.

### 7 August 2019

Added OFL.txt Open Font License and info

Added FontLab .enc encoding file

### 6 August 2019
Renamed the project to Science Gothic!

### 10 July 2019
Started the repo

## Acknowledgements

If you make modifications be sure to add your name (N), optional email (E), web-address (if you have one) (W) and description (D).
This list is in alphabetical order after Thomas.

    N: Thomas Phinney, Font Detective LLC
    W: https://www.thomasphinney.com
    W: https://thefontdetective.com
    D: Admin, Design Lead, Designer

    N: Brandon Buerkle
    W: https://www.societyoffonts.com/
    D: Designer

    N: Igor Freiberger
    D: Designer (for a few early weeks of the project)

    N: Vassil Kateliev
    W: http://www.kateliev.com/
    D: Designer, Python scripting, Cyrillic
    

## License

Science Gothic fonts and their source files are licensed to others under the open source SIL Open Font License v1.1 (<http://scripts.sil.org/OFL>) with no Reserved Font Name. To view the specific terms and conditions please refer to [OFL.txt](https://github.com/tphinney/science-gothic/OFL.txt)

Additional non-font source files are licensed to others under the Apache 2.0 open source license (<https://www.apache.org/licenses/LICENSE-2.0>).

## Language Coverage & Glyph Set

This typeface has extended Latin and extended Cyrillic, with over 1200 glyphs. [FontLab .enc encoding file](https://github.com/tphinney/science-gothic/blob/master/Science%20Gothic.enc).
