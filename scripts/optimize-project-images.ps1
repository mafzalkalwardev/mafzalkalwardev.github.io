# Recompress oversized project PNGs for faster page loads (max width 960).
$ErrorActionPreference = "Stop"
$cmd = Get-Command ffmpeg -ErrorAction SilentlyContinue
$ffmpeg = if ($cmd) { $cmd.Source } else { $null }
if (-not $ffmpeg) {
  $ffmpeg = "C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
}
if (-not (Test-Path $ffmpeg)) { throw "ffmpeg not found" }

$dir = Join-Path $PSScriptRoot "..\assets\projects" | Resolve-Path
$files = Get-ChildItem $dir -Filter *.png | Where-Object { $_.Length -gt 200KB }
Write-Host "Optimizing $($files.Count) images over 200KB..."
foreach ($f in $files) {
  $tmp = Join-Path $env:TEMP ("opt-" + $f.Name)
  & $ffmpeg -y -i $f.FullName -vf "scale='min(960,iw)':-2" -compression_level 9 $tmp 2>$null
  if ((Test-Path $tmp) -and ((Get-Item $tmp).Length -gt 0) -and ((Get-Item $tmp).Length -lt $f.Length)) {
    $before = [math]::Round($f.Length / 1KB, 1)
    Move-Item -Force $tmp $f.FullName
    $after = [math]::Round((Get-Item $f.FullName).Length / 1KB, 1)
    Write-Host ("  {0}: {1}KB -> {2}KB" -f $f.Name, $before, $after)
  } else {
    Remove-Item $tmp -ErrorAction SilentlyContinue
    Write-Host ("  skip {0}" -f $f.Name)
  }
}
