# SCRIPT:   Science Gothic Build Variable Font 
# VER:      2.0
# -----------------------------------------------------------
# (C) Vassil Kateliev, 2022-2024   (http://www.kateliev.com)
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
    [switch]$notest = $false,
    [switch]$nopost = $false
) 

# - Configuration
# -- Preffered naming patterns
$pref_variable_output = 'fonts'      # Preffered fontmake output folder name
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
    Get-ChildItem -Path $path_fontmake_out -Filter '*-VF*' -Recurse | Rename-Item -NewName {$_.name -replace '-VF', ''}
}

# -- Postprocess output variable fonts
if (-not $nopost) {
    Write-output "`nPOST >>> Processing Variable Fonts: $path_fontmake_out"
    $list_path_ttf = @(Get-ChildItem -Path $path_fontmake_out -Include *.ttf -Recurse)

    foreach ($path_ttf in $list_path_ttf) {

        Write-output "`nPOST >>> Fixing Unwanted Tables: $path_ttf"
        python (Get-Command gftools-fix-unwanted-tables.py).Path $path_ttf

        Write-output "`nPOST >>> Fixing Hinting: $path_ttf"
        gftools fix-nonhinting.py $path_ttf $path_ttf

        Write-output "`nPOST >>> Fixing DSIG table: $path_ttf"
        gftools fix-dsig.py --autofix $path_ttf

        Write-output "`nPOST >>> Validating fonts: $path_ttf"
        ftxvalidator $path_ttf

    }
    

    # -- Cleanup
    Get-ChildItem -Path $path_fontmake_out -Filter '*backup-fonttools*' -Recurse | foreach {$_.delete()}
    Get-ChildItem -Path $path_fontmake_out -Filter '*-VF*' -Recurse | Rename-Item -NewName {$_.name -replace '-VF', ''}
}


# -- Run Google QA on the resulting .ttfs
if (-not $notest) {
    Write-output "`nTEST >>> Running Google-Fonts QA on: $path_fontmake_out"
    cd $path_fontmake_out
    fontbakery check-googlefonts *.ttf --html $designspace.replace("``","").replace(".designspace", ".html")
    cd $path_current_run
}

    