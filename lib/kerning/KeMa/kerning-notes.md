# Science Gothic
## Kerning Production Notes

## First run 2020-07-07
**KRN**
_Note using Sublime and RegEx `^.*_punct.*_lc.*` to search for lines containing both search terms and delete those lines_
- SG-Regular-Class2Class-Redux-.krn _#reduced number of pairs_
- SG-Regular-Class2Class-Redux-2.0.krn _#further reduced pairs_

**CLA**
- SG-Classes.cla _#Fixed class ordering. Ultra slow results with many memory errors from KeMa._
- SG-Classes-Short.cla _#Very vast results. Only one important glyph in class_

**Design/Set**
- 10/10 _#Good results_

**Srength**
- 100 _#Good results_
- 150 _#1.5 x negative kernign, but does not reduce positive in contrary 1.5 x positive values which is has_

**TO FIX:**
- Too many positive pairs - investigate
- Remove  `KPX @any_sc _sc_h_2` and `KPX _sc_h_2 @any_sc`. Leave only UC 2 SC
- Some glyphs that have no classes need to be added to KRN. V v v.sc and etc.

## Check 2020-07-24

**Design/Set**
- 96/96 _#Good results_

**Srength**
- 200 _#Close to original kerning_

**TO FIX:**
[ ] Problems with some glyphs @ Blk Cnd, Blk Exp where :
    [ ] T hyphen and T hyphen.case as well as guilemmot stuff is colliding
    [x] Better switch to 100% kerning at the Blk Cnd or fix by hand
[x] Some incosistances between pairs in all masters. Match is needed
[x] Some diacritical groups look strange like T o is OK but T odieresis is wrong?!
[ ] Slanted masters do not show good results with KeMa. Need to copy kerning from the uprights.

## Check 2020-07-29
Search all T combos ```_uc_T.*\b.*_lc.*```
[x] Viatnamese horn problems. Check metrics or re-kern

## Check 2020-08-03
[x] r|punctuation an >> rdiac|punctuation; [x]
[x] uni0413, uni0433; 
[x] E|all e.sc|all; 
[x] F|all f.sc|all;
[x] all|punct_case_dash
[x] .*uc_T.*.;
[x] uc_T|sc_h; uc_T|sc_hdiac;
[x] uc_T|_sc_t;_

## Check 2020-08-05
**Regex Patterns**
```
.*.lc_r.*.punct.*|.*.punct.*.lc_r.*
.*.uc_T.*.sc_t.*|.*.sc_t.*.uc_T.*
.*.uc_T.*.sc_h.*|.*.sc_h.*.uc_T.*
_uc_E.*|_uc_F.*
.*_dash_3.*._uc*.*|.*_uc*.*.*_dash_3
.*uni0413.*|.*uni0433.*
.*uni0413.*_uc.*|.*_uc_T.*_uc.*
.*uni0413.*_lc.*|.*_uc_T.*_lc.*
.*uni0413.*_sc.*|.*_uc_T.*_sc.*
```