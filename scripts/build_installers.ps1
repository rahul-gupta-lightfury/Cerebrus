param(
    [Parameter(Mandatory = $false)][string]$TagVersion = "0.0.0",
    [Parameter(Mandatory = $false)][string]$OutputDir = "installer_output"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Write-Section($text) {
    Write-Host "`n== $text ==" -ForegroundColor Cyan
}

Write-Section "Preparing staging layout"
python -m cerebrus.installers.builder --output $OutputDir

$resolvedOutput = Resolve-Path $OutputDir
$stagingRoot = Join-Path $resolvedOutput "Cerebrus"
$version = $TagVersion.TrimStart('v')
if (-not $version) {
    $version = "0.0.0"
}

Write-Section "Ensuring WiX Toolset"
$heat = "${env:ProgramFiles(x86)}\WiX Toolset v3.11\bin\heat.exe"
$candle = "${env:ProgramFiles(x86)}\WiX Toolset v3.11\bin\candle.exe"
$light = "${env:ProgramFiles(x86)}\WiX Toolset v3.11\bin\light.exe"
if (-not (Test-Path $heat)) {
    choco install wixtoolset --yes --no-progress
}

$heat = "${env:ProgramFiles(x86)}\WiX Toolset v3.11\bin\heat.exe"
$candle = "${env:ProgramFiles(x86)}\WiX Toolset v3.11\bin\candle.exe"
$light = "${env:ProgramFiles(x86)}\WiX Toolset v3.11\bin\light.exe"

Write-Section "Generating WiX sources"
$componentsWxs = Join-Path $resolvedOutput "components.wxs"
& $heat dir $stagingRoot -dr INSTALLFOLDER -cg CerebrusComponents -sfrag -srd -var var.StagingDir -out $componentsWxs

$productWxs = @"
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="Cerebrus" Language="1033" Version="$(var.ProductVersion)" Manufacturer="Cerebrus" UpgradeCode="0446F967-2C20-4EFD-AEDC-479F38A94F2F">
    <Package InstallerVersion="500" Compressed="yes" InstallScope="perMachine"/>
    <MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed."/>
    <MediaTemplate/>
    <Feature Id="FeatureMain" Title="Cerebrus" Level="1">
      <ComponentGroupRef Id="CerebrusComponents"/>
    </Feature>
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFiles64Folder">
        <Directory Id="INSTALLFOLDER" Name="Cerebrus" />
      </Directory>
    </Directory>
  </Product>
</Wix>
"@
$productWxsPath = Join-Path $resolvedOutput "product.wxs"
Set-Content -Path $productWxsPath -Value $productWxs -Encoding UTF8

Write-Section "Building MSI"
& $candle -dStagingDir=$stagingRoot -dProductVersion=$version -out (Join-Path $resolvedOutput "") $productWxsPath $componentsWxs
& $light -ext WixUIExtension -out (Join-Path $resolvedOutput "Cerebrus-$version.msi") (Join-Path $resolvedOutput "product.wixobj") (Join-Path $resolvedOutput "components.wixobj")

Write-Section "Building Burn bootstrapper (.exe)"
$bundleWxs = @"
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi" xmlns:bal="http://schemas.microsoft.com/wix/BalExtension">
  <Bundle Name="Cerebrus" Version="$(var.ProductVersion)" Manufacturer="Cerebrus" UpgradeCode="77F1E6F2-05B4-4F98-97B4-41C1AE101A5A" Compressed="yes">
    <BootstrapperApplicationRef Id="WixStandardBootstrapperApplication.RtfLicense" />
    <Chain>
      <MsiPackage SourceFile="$(var.MsiPath)" DisplayInternalUI="yes" Vital="yes" />
    </Chain>
  </Bundle>
</Wix>
"@
$bundleWxsPath = Join-Path $resolvedOutput "bundle.wxs"
Set-Content -Path $bundleWxsPath -Value $bundleWxs -Encoding UTF8

& $candle -ext WixBalExtension -dProductVersion=$version -dMsiPath="$(Join-Path $resolvedOutput "Cerebrus-$version.msi")" -out (Join-Path $resolvedOutput "") $bundleWxsPath
& $light -ext WixBalExtension -out (Join-Path $resolvedOutput "Cerebrus-$version.exe") (Join-Path $resolvedOutput "bundle.wixobj")

Write-Section "Artifacts"
Get-ChildItem $resolvedOutput -Filter "Cerebrus-$version.*" | ForEach-Object { Write-Host "Created $_" }
