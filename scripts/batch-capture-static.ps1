$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
$Cache = Join-Path $Root ".capture-cache"
$Out = Join-Path $Root "assets\projects"
$Capture = "d:\Projects\_github-upload-toolkit\scripts\capture-edge.mjs"
New-Item -ItemType Directory -Force -Path $Cache, $Out | Out-Null

$StaticRepos = @(
  @{ Repo = "logistics-pro-website"; Path = "/index.html" },
  @{ Repo = "apex-transit-llc-website"; Path = "/index.html" },
  @{ Repo = "wooly-wool-storefront"; Path = "/index.html" },
  @{ Repo = "andaaz-e-pakwaan-restaurant"; Path = "/index.html" },
  @{ Repo = "student-report-card-system"; Path = "/index.html" },
  @{ Repo = "restaurant-management-react"; Path = "/index.html" },
  @{ Repo = "simple-learning-dashboard"; Path = "/index.html" },
  @{ Repo = "fake-news-detector"; Path = "/index.html" },
  @{ Repo = "mighty-trucking"; Path = "/index.html" },
  @{ Repo = "kb-transport-llc-website"; Path = "/index.html" },
  @{ Repo = "indus-transports-dispatch-website"; Path = "/index.html" },
  @{ Repo = "one-stop-car-care-website"; Path = "/index.html" }
)

function Get-Slug($name) { $name.ToLower() }

foreach ($item in $StaticRepos) {
  $repo = $item.Repo
  $slug = Get-Slug $repo
  $dest = Join-Path $Cache $repo
  $png = Join-Path $Out "$slug.png"
  if ((Test-Path $png) -and (Get-Item $png).Length -gt 5000) {
    Write-Host "Skip $repo (exists)"
    continue
  }
  if (-not (Test-Path $dest)) {
    Write-Host "Clone $repo"
    gh repo clone "mafzalkalwardev/$repo" $dest -- --depth 1 2>&1 | Out-Null
  }
  $entry = $item.Path.TrimStart("/")
  if (-not (Test-Path (Join-Path $dest $entry))) {
    Write-Host "No $entry for $repo"
    continue
  }
  $port = 8900 + (Get-Random -Maximum 80)
  $job = Start-Job -ScriptBlock {
    param($d, $p)
    Set-Location $d
    npx --yes serve -l $p . 2>&1 | Out-Null
  } -ArgumentList $dest, $port
  Start-Sleep -Seconds 7
  $env:BASE_URL = "http://127.0.0.1:$port"
  $env:OUTPUT_DIR = $Out
  $env:SHOTS = "[{`"file`":`"$slug.png`",`"path`":`"$($item.Path)`",`"viewport`":{`"width`":1440,`"height`":900}}]"
  Write-Host "Capture $repo -> $slug.png"
  node $Capture 2>&1
  Stop-Job $job -ErrorAction SilentlyContinue
  Remove-Job $job -Force -ErrorAction SilentlyContinue
}

# Copy known real screenshots from local clones
$Copies = @(
  @{ Src = "d:\Projects\_github-sync\playwright-website-scraper-pro\docs\screenshots\home.png"; Dst = "playwright-website-scraper-pro.png" },
  @{ Src = "d:\Dispatch Softwares\Auto Dialer\docs\screenshots\dialer-light.png"; Dst = "indus-transport-auto-dialer.png" },
  @{ Src = "d:\Dispatch Softwares\Auto Dialer\docs\screenshots\live-calls-dark.png"; Dst = "google-voice-call-state-detector.png" }
)
foreach ($c in $Copies) {
  if (Test-Path $c.Src) {
    Copy-Item $c.Src (Join-Path $Out $c.Dst) -Force
    Write-Host "Copied $($c.Dst)"
  }
}

Write-Host "Done."
