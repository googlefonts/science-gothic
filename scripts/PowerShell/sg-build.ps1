# SCRIPT:   Science Gothic Build Variable Font 
# VER:      1.2
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

# - Take parameters from CLI
param (
    [Parameter(Mandatory=$true)][string]$designspace,
    [switch]$nobuild = $false,
    [switch]$notest = $false
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
$pref_variable_output = 'variable_ttf'      # Preffered fontmake output folder name
$pref_backup_folder = 'backup'              # Preffered backup folder name

# - Init
$path_current_run = Get-Location
$file_designspace_in = (Split-Path -Path $designspace -Leaf).Replace("``","")
$path_designspace_in = (Split-Path -Path $designspace -Parent).Replace("``","")
$path_fontmake_out = (Join-Path -Path $path_designspace_in -Child $pref_variable_output).Replace("``","")
$path_backup = (Join-Path -Path $path_designspace_in -Child $pref_backup_folder).Replace("``","")

# - Process
# -- Generate variable fonts
if (-not $nobuild) {
    Write-output "`nBUILD >>> Generating Variable Font: $file_designspace_in"
    fontmake -m $designspace -o variable --output-dir $path_fontmake_out --verbose WARNING --keep-overlaps
}

# -- Run Google QA on the resulting .ttfs
if (-not $notest) {
    Write-output "`nBUILD >>> Running Google-Fonts QA on: $path_fontmake_out"
    cd $path_fontmake_out
    fontbakery check-googlefonts *.ttf --html $designspace.replace("``","").replace(".designspace", ".html")
    cd $path_current_run
}

