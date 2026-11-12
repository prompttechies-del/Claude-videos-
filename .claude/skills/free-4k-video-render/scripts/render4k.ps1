# render4k.ps1 — Windows version of render4k.sh (same flags). Needs ffmpeg/ffprobe on PATH; Node.js for HTML/Remotion.
#   .\render4k.ps1 -Src <path> [-Orientation 16x9|9x16|1x1] [-Fps 30] [-Quality draft|standard|master] [-Gpu auto|nvidia|amd|intel|apple|none] [-Duration 5] [-Comp Main] [-Audio file] [-Out out\x.mp4]
param([Parameter(Mandatory)][string]$Src, [ValidateSet("16x9","9x16","1x1")][string]$Orientation="16x9", [int]$Fps=30,
      [ValidateSet("draft","standard","master")][string]$Quality="standard", [ValidateSet("auto","nvidia","amd","intel","apple","none")][string]$Gpu="auto",
      [double]$Duration=0, [string]$Comp="", [string]$Audio="", [string]$Out="")
$ErrorActionPreference = "Stop"; $Here = Split-Path -Parent $MyInvocation.MyCommand.Path
switch ($Quality) { "draft" {$L=1920;$S=1080;$Crf=26;$Preset="ultrafast"} "standard" {$L=3840;$S=2160;$Crf=18;$Preset="veryfast"} "master" {$L=3840;$S=2160;$Crf=14;$Preset="slow"} }
switch ($Orientation) { "16x9" {$W=$L;$H=$S} "9x16" {$W=$S;$H=$L} "1x1" {$W=$S;$H=$S} }
$item = Get-Item $Src
if ($item.PSIsContainer -and (Test-Path "$Src\package.json") -and (Select-String -Quiet '"remotion"' "$Src\package.json")) { $Type="remotion" }
elseif (-not $item.PSIsContainer -and $item.Extension -match '^\.html?$') { $Type="html" }
elseif ($item.PSIsContainer -and (Get-ChildItem $Src -File | Where-Object { $_.Extension -match '^\.(png|jpe?g)$' })) { $Type="frames" }
else { $Type="video" }
if (-not $Out) { New-Item -ItemType Directory -Force out | Out-Null; $Out = "out\$($item.BaseName)-$Orientation-$Quality.mp4" }
function Works($enc) { & ffmpeg -v error -f lavfi -i color=s=256x256:d=0.2 -c:v $enc -f null - 2>$null; return $LASTEXITCODE -eq 0 }
$Enc = "libx264"
if ($Quality -ne "master") {
  if ($Gpu -eq "auto") { if ((Get-Command nvidia-smi -ErrorAction SilentlyContinue) -and (Works "h264_nvenc")) {$Enc="h264_nvenc"} elseif (Works "h264_qsv") {$Enc="h264_qsv"} elseif (Works "h264_amf") {$Enc="h264_amf"} }
  elseif ($Gpu -eq "nvidia" -and (Works "h264_nvenc")) {$Enc="h264_nvenc"} elseif ($Gpu -eq "intel" -and (Works "h264_qsv")) {$Enc="h264_qsv"} elseif ($Gpu -eq "amd" -and (Works "h264_amf")) {$Enc="h264_amf"} }
$V = switch ($Enc) { "h264_nvenc" {@("-c:v","h264_nvenc","-rc","vbr","-cq",$Crf,"-b:v","0","-preset","p5","-pix_fmt","yuv420p")} "h264_qsv" {@("-c:v","h264_qsv","-global_quality",$Crf)} "h264_amf" {@("-c:v","h264_amf","-rc","cqp","-qp_i",$Crf,"-qp_p",$Crf)}
  default { if ($Quality -eq "master") {@("-c:v","libx264","-crf",$Crf,"-preset",$Preset,"-pix_fmt","yuv420p10le","-profile:v","high10")} else {@("-c:v","libx264","-crf",$Crf,"-preset",$Preset,"-pix_fmt","yuv420p")} } }
Write-Host "> $Type -> ${W}x${H} @ $Fps fps, $Quality, $Enc"
$In = @()
switch ($Type) {
  "frames" { $ext = (Get-ChildItem $Src -File | Where-Object { $_.Extension -match '^\.(png|jpe?g)$' } | Sort-Object Name | Select-Object -First 1).Extension
             $list = "$env:TEMP\frames.txt"; Get-ChildItem $Src -Filter "*$ext" | Sort-Object Name | ForEach-Object { "file '$($_.FullName)'`nduration $([math]::Round(1/$Fps,6))" } | Set-Content $list
             $In = @("-f","concat","-safe","0","-i",$list) }
  "video"  { $In = @("-i",$Src) }
  "html"   { $frames = "$env:TEMP\r4k_frames"; Remove-Item -Recurse -Force $frames -ErrorAction SilentlyContinue
             $pw = if ($Orientation -eq "9x16") {1080} else {1920}; $ph = if ($Orientation -eq "16x9") {1080} elseif ($Orientation -eq "9x16") {1920} else {1080}; if ($Orientation -eq "1x1") {$pw=1080}
             $nd = Join-Path $env:USERPROFILE ".cache\free-4k\node_modules"; if (-not (Test-Path "$nd\playwright-core")) { npm install --silent --prefix (Split-Path $nd) playwright-core | Out-Null; npx --prefix (Split-Path $nd) playwright-core install chromium | Out-Null }
             $env:FREE4K_NODE = $nd; $da = @(); if ($Duration -gt 0) { $da = @("--duration",$Duration) }
             node "$Here\html2frames.mjs" --src $Src --out $frames --w $pw --h $ph --scale ([int]($W/$pw)) --fps $Fps @da
             $In = @("-framerate",$Fps,"-i","$frames\f%06d.jpg"); $Duration = 0 }
  "remotion" { $tmp = (Resolve-Path .).Path + "\out\remotion.mp4"; Push-Location $Src; $sc = if ($Quality -eq "draft") {1} else {2}
             npx remotion render src/index.ts $Comp $tmp --scale=$sc --crf=12 --log=error; Pop-Location; $In = @("-i",$tmp) }
}
$Vf = "[0:v]split[a][b];[a]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},boxblur=40[bg];[b]scale=${W}:${H}:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=$Fps,setsar=1[v]"
$A = @("-an"); if ($Audio) { $In += @("-i",$Audio); $A = @("-map","1:a:0","-af","loudnorm=I=-14:TP=-1.5:LRA=11","-c:a","aac","-b:a","192k","-shortest") }
$T = @(); if ($Duration -gt 0) { $T = @("-t",$Duration) }
& ffmpeg -v error -stats -y @In -filter_complex $Vf -map "[v]" @A @T @V -movflags +faststart $Out
if ($Quality -eq "master") { & ffmpeg -v error -y -i $Out -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le -c:a pcm_s16le ($Out -replace '\.mp4$','-prores.mov') }
& python "$Here\verify.py" $Out --w $W --h $H --fps $Fps
