# SCRIPT:   Science Gothic Build Variable Font 
# VER:      1.0
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2022         (http://www.kateliev.com)
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

while getopts "f:isbpt" opt; do
  case $opt in
    f)  designspace=$OPTARG ;;  # get designspace to process
    b)  do_build=false ;;       # do not build the font
    t)  do_test=false ;;        # do not test the ttfs
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
  esac
done

# - Configuration -------------------------------------------
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

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
    echo "BUILD >>> Generating Variable Font: $file_designspace_in"
    fontmake -m "$file_designspace_in" -o variable --output-dir "$path_fontmake_out" --verbose WARNING --keep-overlaps
fi

# -- Run Google QA on the resulting .ttfs
if [ $do_test == true ]; 
then
    echo "BUILD >>> Running Google-Fonts QA on: $path_fontmake_out"
    cd "$path_fontmake_out"
    fontbakery check-googlefonts *.ttf --html "gs-split-build-report.html" #"${$designspace%%.*}.html"
    cd "$path_current_run"
fi

# - End -----------------------------------------------------
date
