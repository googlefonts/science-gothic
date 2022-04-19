# About the Master folder

## General

tl;dr: The VFC file is guaranteed to be the most up-to-date source. 

This folder contains font sources for the project in VFC (FontLab 7 native binary file format). We have posted some production sources in UFO (Universal Font Object, an open source text format), but no longer post them regularly due to the huge number of files involved. Additionally, there is a .designspace file, defining axes, masters and coordinates, which can be used with UFO or other formats.

- We no longer post VFJ due to size, it not being documented (which removes the main benefit of its plain-text form), and because FontLab rewrites the whole VFJ in ways that do not allow useful diffs.

## Old File Naming Conventions
(Not used in current files)

- 3a or 4a refers to the number of Variable Font axes supported (3-axis or 4-axis). The difference is whether the slant (oblique) axis is present. This axis is generated mostly automatically by build scripts, with a little human tweaking. A new 4a font will normally be posted no less than once every two weeks (typically weekly).

- 18m or 36m refers to the number of masters present, 18 without slant, or 36 with slant/oblique.
