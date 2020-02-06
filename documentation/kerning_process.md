# Science Gothic Kerning Process

## Overview

Science Gothic makes heavy use of class kerning, as you would expect from a font with so many glyphs per master, and 36 masters. We are lucky that the shapes are mostly pretty square, plus a few diagonals. It means Science Gothic has fewer unique shapes needing kerning than most typefaces do. It has about 115 kerning classes.

We are making careful use of reasonably predictable relationships between masters. Throughout, once each master is kerned, its kerning is always copied to its Slant (S) counterpart. If updates are made, the copy-to-slant-master is repeated. The :CtrEtc masters also start with the kerning of their non-Contrast counterparts, and only those classes that have significant differences are re-kerned. This primarily affects just a few glyphs such as K and k.

The process concept is:

1. Completely kern the :Medium master (class kerning, plus exceptions if needed) in FontLab 7
1. Copy kerning to :Slant and :Ctr (just the two masters). No edits at this time.
1. Copy the kerning from :Medium to :Lt and :Blk
    - :Lt edit kerning
    - :Blk edit kerning
1. Copy kerning to :LtS :BlkS :LtCtr :BlkCtr
1. Edit Ctr masters
    - :LtCtr
    - :BlkCtr

1. Copy the kerning from the :Medium master to :Cnd and :Exp:, then edit each of them.
    - :Cnd (after copying, scale it to ~ 40% for negative kerning and ~ 80% for positive kerning); edit
    - :Exp (after copying it, scale 175% for negative kerning, 125% for positive kerning); edit
1. Copy kerning to :CndS and :ExpS
1. Copy the kerning to corner masters, possibly with some auto-adjust, then edit them.
    - Copy :Cnd to :LtCnd, edit
    - Copy :Exp to :LtExp, edit

1. TBD whether the :BlkCnd should start with kerning copied from :Blk, or with :Cnd; whether :BlkExp should start with :Blk, or with :Exp

1. Make any final adjustments where :EtcCtr masters differ in unpredictable ways from other masters. One set of obvious and expected cases is for glyphs that have multiple diagonals on the same side; another is thin horizontals in the Blk weight (/K /k /ampersand /Z /z /f /f.slnt /t /E /F /T /one /six /nine /one.tnum /exclam /exclamdown /exclamdown.case parens, brackets, braces, etc.). For /K /k, the positioning of the one diagonal to the other may be different in the :BlkEtcCtr masters compared to other masters. 
