# SCRIPT:   Science Gothic Build Variable Font 
# VER:      2.4
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2022-2024    (http://www.kateliev.com)
#------------------------------------------------------------
# No warranties. By using this you agree
# that you use it at your own risk!

#------------------------------------------------------------
# PROJECT: Science Gothic - Variable Font (Google)
# BY: Thomas Phinney <thomas@thefontdetective.com>
# HOME: https://github.com/tphinney/science-gothic/issues
#------------------------------------------------------------

# - Arguments -----------------------------------------------
do_build=true   # -b -> build the font
do_test=true    # -t -> test the ttfs
do_post=true   # -p -> posptocess the ttfs

while getopts "f:isbpt" opt; do
  case $opt in
    f)  designspace=$OPTARG ;;  # get designspace to process
    b)  do_build=false ;;       # do not build the font
    t)  do_test=false ;;        # do not test the ttfs
    p)  do_post=false ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
  esac
done

# - Configuration -------------------------------------------
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
path_stylespace=$script_dir/"../../lib/ScienceGothic[YOPQ,slnt,wdth,wght].stylespace"

# -- Tools
py_tables=$script_dir/"../Python/sg-fix-unwanted-tables.py"

# -- Preferred naming patterns
pref_variable_output="variable_ttf"  # Preferred fontmake output folder name
pref_backup_folder="backup"          # Preferred backup folder name

# - Init
path_current_run=$PWD
file_designspace_in=$(basename $designspace)
path_designspace_in=$(dirname $designspace)
path_fontmake_out=$path_designspace_in/$pref_variable_output

# - Init ----------------------------------------------------
date

# - Process -------------------------------------------------
# -- Generate variable fonts
if [ $do_build == true ];
then
    echo "\nBUILD >>> Generating Variable Font: $file_designspace_in"
    fontmake -m "$designspace" -o variable --output-dir "$path_fontmake_out" --verbose WARNING --keep-overlaps
    mv $path_fontmake_out ${path_fontmake_out/-VF/""}
fi

# -- Process output variable fonts
if [ $do_post == true ];
then
    echo "\nPOST >>> Processing Variable Fonts: $path_fontmake_out"
    # -- Process files
    for path_ttf in $(find $path_fontmake_out -type f -name "*.ttf");
        do
            echo "\nPOST >>> Fixing Stylespace: $path_ttf"
            statmake --designspace "$designspace" --stylespace "$path_stylespace" "$path_ttf"

            echo "\nPOST >>> Fixing Unwanted Tables: $path_ttf"
            python3 "$py_tables" "$path_ttf"
            
            echo "\nPOST >>> Fixing Hinting: $path_ttf"
            gftools-fix-nonhinting.py $path_ttf $path_ttf

            #!!! Removed. Consult: https://github.com/googlefonts/science-gothic/issues/331
            #echo "\nPOST >>> Fixing DSIG table: $path_ttf"
            #gftools fix-dsig.py --autofix $path_ttf

            #echo "\nPOST >>> Validating fonts: $path_ttf"
            #ftxvalidator $path_ttf

        done

    # -- Cleanup
    rm $path_fontmake_out/*backup-fonttools* -f
fi

# -- Run Google QA on the resulting .ttfs
if [ $do_test == true ]; 
then
    echo "BUILD >>> Running Google-Fonts QA on: $path_fontmake_out"
    cd "$path_fontmake_out"
    fontbakery check-googlefonts *.ttf --html "sg-build-report.html" --full-lists
    cd "$path_current_run"
fi

# - End -----------------------------------------------------
date
