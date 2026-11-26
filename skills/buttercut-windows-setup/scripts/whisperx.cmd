@echo off
REM ButterCut WhisperX launcher (Windows). ButterCut's Ruby shells out to a bare
REM `whisperx` on PATH; this shim forwards to the pinned venv via whisperx_run.py,
REM which applies a Windows compatibility patch before invoking the WhisperX CLI.
"%USERPROFILE%\.buttercut\venv\Scripts\python.exe" "%USERPROFILE%\.buttercut\whisperx_run.py" %*
