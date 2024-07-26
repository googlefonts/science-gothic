# SCRIPT:   Science Gothic Build Instances
# VER:      1.1
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2024-XXXX   (http://www.kateliev.com)
#------------------------------------------------------------
# No warranties. By using this you agree
# that you use it at your own risk!

#------------------------------------------------------------
# PROJECT: Science Gothic - Variable Font (Google)
# BY: Thomas Phinney <thomas@thefontdetective.com>
# HOME: https://github.com/tphinney/science-gothic/issues
#------------------------------------------------------------

# - Take parameters from CLI
param (
    [Parameter(Mandatory=$true)][string]$designspace,
    [switch]$build = $true,
    [switch]$test = $false,
    [switch]$post = $false
) 

# - Functions
function Resolve-FullPath {
    [cmdletbinding()]
    param
    (
        [Parameter(
            Mandatory=$true,
            Position=0,
            ValueFromPipeline=$true)]
        [string] $path
    )
     
    $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($path)
}

# - Configuration
# -- Preffered naming patterns
$pref_variable_output = 'fonts'      # Preffered fontmake output folder name
$pref_backup_folder = 'backup'       # Preffered backup folder name

# -- Tools
$py_font_rename = Resolve-FullPath "$PSScriptRoot\..\Python\sg-font-filename-shortener.py"

# - Init
$path_current_run = Get-Location
$file_designspace_in = (Split-Path -Path $designspace -Leaf).Replace("``","")
$path_designspace_in = (Split-Path -Path $designspace -Parent).Replace("``","")
$path_fontmake_out = (Join-Path -Path $path_designspace_in -Child $pref_variable_output).Replace("``","")
$path_backup = (Join-Path -Path $path_designspace_in -Child $pref_backup_folder).Replace("``","")

# - Process
# -- Generate variable fonts
if ($build) {
    Write-output "`nBUILD >>> Generating Instances from: $file_designspace_in"
    fontmake -m $designspace -o ttf  -i --output-dir $path_fontmake_out --round-instances --keep-overlaps

    # -- Shorten filenames
    python $py_font_rename $path_fontmake_out
}

# -- Postprocess output variable fonts
if ($post) {
    Write-output "`nPOST >>> Processing Fonts: $path_fontmake_out"
    $list_path_ttf = @(Get-ChildItem -Path $path_fontmake_out -Include *.ttf -Recurse)

    foreach ($path_ttf in $list_path_ttf) {

        #Write-output "`nPOST >>> Fixing Hinting: $path_ttf"
        #gftools fix-nonhinting $path_ttf $path_ttf

    }
}

# -- Run Google QA on the resulting .ttfs
if ($test) {
    Write-output "`nTEST >>> Running Google-Fonts QA on: $path_fontmake_out"
    cd $path_fontmake_out
    fontbakery check-googlefonts *.ttf --html $designspace.replace("``","").replace(".designspace", ".html") --full-lists
    cd $path_current_run
}

    