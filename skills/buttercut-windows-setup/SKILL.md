---
name: buttercut-windows-setup
description: Installs or repairs ButterCut — the AI video rough-cut agent at github.com/barefootford/buttercut — on Windows. ButterCut is officially Mac-only and its built-in /setup skill (Homebrew/bash) does NOT run on Windows; this skill automates the verified Windows port instead. Use it whenever the user wants to install, set up, configure, reinstall, or repair ButterCut on a Windows PC, or hits Windows-specific ButterCut errors. Trigger on phrases like "instalar buttercut", "install buttercut", "configurar/setup buttercut no windows", "buttercut não acha o ffmpeg / ffmpeg not found", "whisperx travando/crashing no buttercut", "k2 module not found", "as skills do buttercut não aparecem", or pasting the buttercut GitHub URL on a Windows machine. Prefer THIS skill over ButterCut's own /setup whenever the OS is Windows.
---

# ButterCut on Windows — install & repair

ButterCut is an AI agent that ingests footage into "libraries", transcribes it
with WhisperX, builds single-track rough cuts from the transcripts, and exports a
timeline as XML (FCPXML / Premiere / DaVinci Resolve). It does **not** render
final video or do color/effects — the user finishes in **DaVinci Resolve** on
Windows (Final Cut is Mac-only).

The project is **officially Mac-only**; its `/setup` skill uses Homebrew, bash and
`xcode-select`, none of which exist on Windows. This skill is the tested Windows
equivalent. Several ButterCut files also assume Unix semantics and must be patched
— see `references/windows-patches.md` (read it before applying patches).

Work top to bottom. Each step says *why*, so you can adapt when a machine differs.
Track progress with a todo list. Re-running the whole skill on an existing install
is safe — every step is idempotent and doubles as a repair pass.

## Conventions used below

- `$BC` = the cloned repo directory (ask the user where to put it; default
  `C:\code\buttercut`). Avoid paths with accents if possible, but spaces/accents
  do work.
- `$HOME\.buttercut` holds the WhisperX virtualenv and launcher (this is fixed —
  ButterCut's `~/.buttercut/...` convention).
- Every fresh PowerShell call starts a new process. After any installer that
  changes PATH, refresh it in-session before using the new tool:
  ```powershell
  $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
  ```

## Step 0 — Pre-flight: what's already here

Check before installing; only install what's missing. Report the table to the user.

```powershell
function chk($n,$c){ try { $v=&$c 2>$null; if($v){"$n: $($v|Select-Object -First 1)"}else{"$n: MISSING"} } catch {"$n: MISSING"} }
chk "winget"  { winget --version }
chk "git"     { git --version }
chk "ruby"    { ruby --version }
chk "bundler" { bundle --version }
chk "python312" { py -3.12 --version }
chk "ffmpeg"  { ffmpeg -version }
# drawtext is required (ButterCut burns timestamps onto contact sheets):
if (ffmpeg -hide_banner -filters 2>$null | Select-String ' drawtext '){"drawtext: PRESENT"}else{"drawtext: MISSING"}
```

`winget` and `git` are prerequisites. If `winget` is missing, stop and tell the
user to install "App Installer" from the Microsoft Store.

## Step 1 — Ruby 3.3 + Python 3.12

ButterCut pins Ruby 3.3.x and **Python 3.12** (WhisperX/pyannote are not yet
compatible with newer Python). Even if a newer Python exists, install 3.12 too —
the WhisperX venv must be built from 3.12.

```powershell
winget install --id RubyInstallerTeam.RubyWithDevKit.3.3 --source winget --accept-package-agreements --accept-source-agreements --silent
winget install --id Python.Python.3.12 --source winget --accept-package-agreements --accept-source-agreements --silent
```

Refresh PATH (see Conventions), then verify `ruby --version` (3.3.x),
`bundle --version`, and `py -3.12 --version` (3.12.x).

## Step 2 — FFmpeg with drawtext

If Step 0 showed FFmpeg present **and** drawtext PRESENT, skip this. Otherwise
install a **full** build (the essentials build omits drawtext):

```powershell
winget install --id Gyan.FFmpeg --source winget --accept-package-agreements --accept-source-agreements --silent
```

Refresh PATH and re-check the drawtext line from Step 0.

## Step 3 — Clone ButterCut

```powershell
git clone https://github.com/barefootford/buttercut.git "$BC"
```

Then install the Ruby gems:

```powershell
Set-Location "$BC"
bundle install
```

## Step 4 — Fix the `.claude/skills` junction

Git can't create the repo's symlink on Windows, so ButterCut's skills won't load.
This is Patch 4 in `references/windows-patches.md`:

```powershell
$cs = Join-Path "$BC" ".claude\skills"
Remove-Item -Recurse -Force $cs -ErrorAction SilentlyContinue
New-Item -ItemType Junction -Path $cs -Target (Join-Path "$BC" "skills") | Out-Null
(Get-ChildItem $cs -Directory).Count   # expect ~12
```

## Step 5 — Apply the Ruby compatibility patches

Read `references/windows-patches.md` and apply **Patch 1** (`media_tools.rb`) and
**Patch 2** (`transcribe_job.rb`) with the Edit tool. Without these, ButterCut
reports "ffmpeg not found" and the WhisperX subprocess PATH is corrupted.

Verify Patch 1 worked:

```powershell
Set-Location "$BC"
ruby -e "require_relative 'lib/buttercut/media_tools'; puts MediaTools.ffmpeg; puts MediaTools.ffprobe"
# expect: ffmpeg / ffprobe  (NOT a MissingBinary error)
```

## Step 6 — WhisperX virtualenv (the long pole)

Create a Python 3.12 venv and install the WhisperX stack. **Pin torch/torchaudio
to 2.5.1+cpu** — newer torchaudio removed `torchaudio.AudioMetaData`, which
pyannote-audio 3.4.0 imports; without the pin the run dies with
`AttributeError: module 'torchaudio' has no attribute 'AudioMetaData'`. The CPU
build is smaller and needs no GPU drivers. This downloads ~1 GB — run it in the
background and continue.

```powershell
$bcHome = Join-Path $env:USERPROFILE ".buttercut"
New-Item -ItemType Directory -Force -Path $bcHome | Out-Null
py -3.12 -m venv (Join-Path $bcHome "venv")
$py = Join-Path $bcHome "venv\Scripts\python.exe"
& $py -m pip install --upgrade pip
& $py -m pip install "torch==2.5.1" "torchaudio==2.5.1" --index-url https://download.pytorch.org/whl/cpu
& $py -m pip install "whisperx==3.4.2" "pyannote-audio==3.4.0"
```

## Step 7 — WhisperX launcher shim + PATH

ButterCut shells out to a bare `whisperx` on PATH. Copy the two bundled launcher
files into `~/.buttercut` (the `whisperx_run.py` applies the speechbrain Windows
fix — Patch 3) and add `~/.buttercut` to the user PATH.

```powershell
$bcHome = Join-Path $env:USERPROFILE ".buttercut"
Copy-Item "<skill-dir>\scripts\whisperx_run.py" $bcHome -Force
Copy-Item "<skill-dir>\scripts\whisperx.cmd"    $bcHome -Force
$userPath = [Environment]::GetEnvironmentVariable("Path","User")
if ($userPath -notlike "*$bcHome*") {
  [Environment]::SetEnvironmentVariable("Path", ($userPath.TrimEnd(';') + ";" + $bcHome), "User")
}
```

(`<skill-dir>` is this skill's own directory.)

## Step 8 — Verify end-to-end

Don't claim success until WhisperX runs through ButterCut's own Ruby. Generate a
real speech clip with Windows TTS (no download), then run the actual job:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
$t = Join-Path $env:USERPROFILE ".buttercut\verify"; New-Item -ItemType Directory -Force $t | Out-Null
$wav = Join-Path $t "v.wav"
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SetOutputToWaveFile($wav); $s.Speak("This is a buttercut windows verification test."); $s.Dispose()
Set-Location "$BC"
ruby lib/buttercut/transcribe_job.rb $wav $t en tiny
# expect: "✓ v.wav transcribed → ...\v.json" and exit 0
Get-Content (Join-Path $t "v.json") -Raw
Remove-Item -Recurse -Force $t
```

If it fails, WhisperX hides its real error (it only re-raises the exit code).
Reproduce directly to see the traceback, then debug:

```powershell
cmd /c "whisperx ""$wav"" --language en --model tiny --compute_type float32 --device cpu --output_format json --output_dir ""$t"" 2>&1"
```

## Step 9 — Report

Tell the user:
- Install verified (transcription works end-to-end).
- **How to use it:** open Claude Code **inside the `$BC` folder** (ButterCut is its
  own working directory) and use its skills: create a library → point it at footage
  → process → build a cut → export XML → import into DaVinci Resolve.
- **Caveats:** (1) the XML export side is not yet validated on Windows — see the
  "Known unresolved caveat" in `references/windows-patches.md`; offer to validate
  when they build their first real cut. (2) Patches 1–2 live in `lib/` and are
  overwritten by ButterCut's `update-buttercut`; reapply them after any update
  (just re-run this skill).

## Default whisper model

When a library is created, ButterCut writes `whisper_model` into
`libraries/settings.yaml`. `tiny` is fast but inaccurate; for real work suggest
`small` or `medium` (slower on CPU but far better transcripts).
