# Science Gothic Kerning Process
DRAFT
Still to be investigated as to workability of the parts that need automation

## Overview

Science Gothic makes heavy use of class kerning, as you would expect from a font with so many glyphs per master, and 36 masters. We are lucky that the shapes are mostly pretty square, plus a few diagonals. It means Science Gothic has fewer unique shapes needing kerning, than most typefaces do. Currently we have a little over 100 kerning classes.

We intend to make careful use of reasonably predictable relationships between masters.

The process concept is:

1. _Completely_ kern the :Medium master (class kerning, and exceptions if needed) in FontLab 7
1. For the :Blk master, do kerning _only_ for special combinations that need to be significantly different from those in the :Medium. This is mostly situations where a glyph like /L or /T that is kerned towards dashes and the like in lighter weights, developes collisions with them in the :BlkEtc. Or especially a /T against lowercase x-height letters, such as /a /e /o /u. So the :Blk master gets minimal kerning, just for these cases where it needs something very different.
1. Until we are _really_ happy with the kerning, we only do the following steps at variable font generation time, .
1. Copy the kerning from the :Medium master to: :LtCnd :LtExp
1. Copy the kerning from the :Medium master to the :BlkCnd :BlkExp ; then copy the kerning from the :Blk master to the :BlkCnd and :BlkExp. In cases where the :Blk is different, it takes priority, but otherwise the far more extensive:Medium kerning comes over.
1. In each of those 4 masters, “scale” the kerning by a constant that differs per master. (This is the part that needs automation. Can this be done with a script? Some other way?) To start with, we might try: **30% for :LtCnd and :BlkCnd; 180% for :LtExp and :BlkExp.**
1. Do a bunch of testing. Revise the scaling percentages until they are as good as they are going to get.
1. Make further tweaks as needed to kerning for individual masters
1. Copy the kerning from the all five of the above masters to their :EtcCtr and :EtcSlnt equivalents
1. Make any final adjustments where :EtcCtr masters differ in unpredictable ways from other masters. One set of obvious and expected cases is for glyphs that have multiple diagonals on the same side, such as /K and /X. In such cases, the positioning of the one diagonal to the other may be different in the :BlkEtcCtr masters compared to other masters.
1. Aside from the :Medium master, all other non-corner masters (:Lt :Cnd :Exp and their slanted counterparts) _will not have kerning done in FontLab at all!_ Instead, Fontlab will automatically add interpolated kerning at export time. (NOTE: need to verify experimentally that this works as expected when it comes to UFO export! No doubt it has been tested with direct variable font export.)
