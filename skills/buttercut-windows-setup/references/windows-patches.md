# ButterCut Windows compatibility patches

ButterCut is officially Mac-only. Three of its files assume Unix semantics and
must be patched (or worked around) for the pipeline to run on Windows. Apply each
exactly. They are idempotent — if the "new" text is already present, skip it.

> ⚠️ Patches #1 and #2 live inside the cloned repo's `lib/`. ButterCut's
> `update-buttercut` skill overwrites `lib/`, so reapply them after any update.

---

## Patch 1 — `lib/buttercut/media_tools.rb` (binary detection)

**Why:** On Windows the binary is `ffmpeg.exe`, but ButterCut checks
`File.executable?(File.join(dir, "ffmpeg"))` with the bare name, which never
matches. Result: ButterCut reports "ffmpeg not found in dependencies/ or on PATH"
even though FFmpeg is installed, breaking transcription and contact sheets.

Replace this block:

```ruby
  DEPENDENCIES_DIR = File.expand_path('../../dependencies', __dir__)

  def self.ffmpeg = resolve('ffmpeg')
  def self.ffprobe = resolve('ffprobe')

  def self.resolve(name)
    local = File.join(DEPENDENCIES_DIR, name)
    return local if File.executable?(local)
    return name if on_path?(name)

    raise MissingBinary,
          "#{name} not found in ButterCut's dependencies/ directory or on PATH — run the setup skill to install it"
  end

  def self.on_path?(name)
    ENV.fetch('PATH', '').split(File::PATH_SEPARATOR).any? do |dir|
      !dir.empty? && File.executable?(File.join(dir, name))
    end
  end
end
```

with:

```ruby
  DEPENDENCIES_DIR = File.expand_path('../../dependencies', __dir__)

  # On Windows an executable is `ffmpeg.exe`, not `ffmpeg`, so a bare-name
  # File.executable? check never matches. Try each Windows executable suffix
  # (plus the bare name) so resolution works on Windows and Unix alike.
  EXE_SUFFIXES = Gem.win_platform? ? ['.exe', '.com', '.bat', '.cmd', ''] : ['']

  def self.ffmpeg = resolve('ffmpeg')
  def self.ffprobe = resolve('ffprobe')

  def self.resolve(name)
    EXE_SUFFIXES.each do |ext|
      local = File.join(DEPENDENCIES_DIR, "#{name}#{ext}")
      return local if File.executable?(local)
    end
    return name if on_path?(name)

    raise MissingBinary,
          "#{name} not found in ButterCut's dependencies/ directory or on PATH — run the setup skill to install it"
  end

  def self.on_path?(name)
    ENV.fetch('PATH', '').split(File::PATH_SEPARATOR).any? do |dir|
      next false if dir.empty?

      EXE_SUFFIXES.any? { |ext| File.executable?(File.join(dir, "#{name}#{ext}")) }
    end
  end
end
```

---

## Patch 2 — `lib/buttercut/transcribe_job.rb` (PATH separator)

**Why:** It builds the WhisperX subprocess PATH by joining with a hard-coded `:`,
which is the Unix separator. On Windows the separator is `;`, so the joined PATH
is corrupted and the subprocess can't find its tools.

Replace:

```ruby
    env = { 'PATH' => [MediaTools::DEPENDENCIES_DIR, ENV.fetch('PATH', '')].join(':') }
```

with:

```ruby
    env = { 'PATH' => [MediaTools::DEPENDENCIES_DIR, ENV.fetch('PATH', '')].join(File::PATH_SEPARATOR) }
```

---

## Patch 3 — speechbrain crash (handled outside site-packages)

**Why:** See the header of `scripts/whisperx_run.py`. speechbrain's inspect-guard
checks for `/inspect.py` (forward slash) and never fires on Windows, so a routine
`inspect.getmodule()` during Pyannote VAD triggers an import of the optional `k2`
module, which has no Windows build → crash.

**Do NOT edit speechbrain in site-packages** (pip would overwrite it, and editing
package-manager files is discouraged). Instead the fix is delivered as the
launcher `scripts/whisperx_run.py`, which monkeypatches speechbrain's LazyModule
at runtime before WhisperX runs. Copy `scripts/whisperx_run.py` and
`scripts/whisperx.cmd` into `~/.buttercut/` and put `~/.buttercut` on PATH so
ButterCut's bare `whisperx` call resolves to the shim.

---

## Patch 4 — `.claude/skills` junction (skills won't load otherwise)

**Why:** The repo ships `.claude/skills` as a symlink to `../skills`. Git on
Windows (`core.symlinks=false`) can't create it, leaving a 9-byte placeholder, so
none of ButterCut's skills load in Claude Code.

Fix with a directory junction (no admin needed):

```powershell
$bc = "<path-to-cloned-buttercut>"
Remove-Item -Recurse -Force (Join-Path $bc ".claude\skills")
New-Item -ItemType Junction -Path (Join-Path $bc ".claude\skills") -Target (Join-Path $bc "skills") | Out-Null
```

---

## Patch 5 — shell-string ffprobe/ffmpeg calls (paths with spaces)

**Why:** Several call sites build a shell string with `Shellwords.escape` (POSIX
backslash escaping) and redirect to `/dev/null`. Windows' shell ignores the
backslashes, so any path with a space (e.g. `C:\Users\First Last\...`) splits
into two arguments: `Library.create` dies with
`ffprobe returned non-numeric duration ... Argument '...' provided as input
filename, but '...' was already specified`. Contact sheets and export hit the
same pattern.

**Fix:** replace each backtick call with an `Open3` argument array (no shell),
and add `require 'open3'` next to `require 'shellwords'` in each file:

- `lib/buttercut/library.rb` → `probe_duration`:
  `output, status = Open3.capture2e(MediaTools.ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path)` and check `status.success?`
- `lib/buttercut/contact_sheet.rb` → `probe`: `stdout, _ = Open3.capture2(ffprobe, '-v','error','-select_streams','v:0','-show_format','-show_streams','-of','json', @video_path)`; `run_ffmpeg`: `_o, stderr, status = Open3.capture3(*full)`
- `lib/buttercut/editor_base_core.rb` → `timecode_track_frames` (`Open3.capture3`, stdout only) and `extract_metadata_from_ffprobe` (`Open3.capture2e`, check `status.success?`)

## Patch 6 — contact-sheet `drawtext` font path (drive colon + accents)

**Why:** `contact_sheet.rb#drawtext_filter` puts `fontfile=#{FONT_PATH}` straight
into the filtergraph. On Windows the drive colon (`C:/...`) ends the option
("No option name near '/Users/...'"), and once escaped, ffmpeg's drawtext
**crashes** (exit -1073741819, "Fontconfig error: Cannot load default config
file") when the font path has non-ASCII characters (accented folder names).

**Fix** in `lib/buttercut/contact_sheet.rb`:
- `drawtext_filter`: `"drawtext=fontfile='#{ffmpeg_font_path.gsub(':', '\\:')}'"`
- add a helper that returns `FONT_PATH` when `ascii_only?`, otherwise copies it
  once to `File.join(Dir.tmpdir, 'buttercut-Arimo-Regular.ttf')` and returns that.

## Transcription on Portuguese (and other non-English) libraries

WhisperX's align step loads a wav2vec2 model via `torch.load`, which torch
2.5.1 refuses (CVE-2025-32434 needs torch >= 2.6) → `align_model ... could not
be found`. Without upgrading torch, transcribe with faster-whisper (already in
the venv) using `word_timestamps=True`, write WhisperX-shaped JSON
(`segments[].words[]` + `word_segments`), then run
`ruby lib/buttercut/prepare_audio_script.rb <json> <video>` and
`ruby lib/buttercut/library.rb <lib> complete transcript <clip>`.

---

Find any new shell-string occurrences after an update with:
`rg -n '`[^`]*#\{|Shellwords.escape' lib/buttercut`

---

## Known unresolved caveat — XML export

The export/timeline generator (`lib/buttercut/*` FCPXML/Premiere/Resolve writers)
has **not** been validated on Windows. Its RSpec suite fails on absolute-path
detection and `file://` URL formatting — likely real Windows path bugs that could
break media links in the exported XML. Validate when the user builds their first
real cut: export, open the XML, confirm Resolve relinks the media. Patch the
generator's path/URL handling if links are broken.
