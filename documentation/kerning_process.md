# Science Gothic Kerning Process

## Overview

Science Gothic makes heavy use of class kerning, as you would expect from a font with so many glyphs per master, and 36 masters. We are lucky that the shapes are mostly pretty square, plus a few diagonals. It means Science Gothic has fewer unique shapes needing kerning, than most typefaces do. It has a little over 100 kerning classes.

We are making careful use of reasonably predictable relationships between masters.

The process concept is:

1. _Completely_ kern the :Medium master (class kerning, and exceptions if needed) in FontLab 7
1. For the :Blk master, do kerning _only_ for special combinations that need to be significantly different from those in the :Medium. This is mostly situations where a glyph like /L or /T that is kerned towards dashes and the like in lighter weights, developes collisions with them in the :BlkEtc. Or especially a /T against lowercase x-height letters, such as /a /e /o /u. So the :Blk master gets minimal kerning, just for these cases where it needs something very different.
1. Copy the kerning from the :Medium master toother masters and edit them:
    - :Lt
    - :Blk
    - :Cnd (after copying, scale it to ~ 40% for negative kerning and ~ 80% for positive kerning)
    - :Exp (after copying it, scale some amount, perhaps 150-200%, TBD)
1. Copy the kerning to the corner masters, possibly with some auto-adjust, and edit them
    - Copy :Cnd to :LtCnd and :BlkCnd
    - Copy :Exp to :LtExp and :BlkExp
1. Copy the kerning from the all the above masters to their :EtcCtr and :EtcSlnt equivalents
1. Make any final adjustments where :EtcCtr masters differ in unpredictable ways from other masters. One set of obvious and expected cases is for glyphs that have multiple diagonals on the same side (/K /k /ampersand /Z /z /f /f.slnt /t /E /F /T /one /six /nine /one.tnum /exclam /exclamdown /exclamdown.case parens, brackets, braces, etc.). In such cases, the positioning of the one diagonal to the other may be different in the :BlkEtcCtr masters compared to other masters. 
