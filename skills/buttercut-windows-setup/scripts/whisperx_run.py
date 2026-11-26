"""ButterCut WhisperX launcher (Windows compatibility shim).

Works around an upstream speechbrain bug that crashes WhisperX on Windows.

speechbrain registers LazyModule proxy objects in sys.modules. When any code
calls inspect.getmodule() (Pyannote's VAD does, during transcription), Python
runs `hasattr(module, '__file__')` over every module, which hits the proxy's
__getattr__ and triggers a real import of the optional `speechbrain.integrations
.k2_fsa` -> `import k2`. `k2` has no Windows build, so this raises and aborts the
whole run.

speechbrain already guards against this: ensure_module() skips the lazy import
when the calling frame is `inspect.py`. But that guard matches the path with a
hard-coded forward slash ("/inspect.py"), so it never fires on Windows, where the
path is "...\\Lib\\inspect.py". We restore the intended behaviour by making the
lazy proxy refuse dunder lookups (what introspection probes) instead of importing.

Install this file at ~/.buttercut/whisperx_run.py and call it from
~/.buttercut/whisperx.cmd so ButterCut's bare `whisperx` PATH lookup uses it.
"""

import speechbrain.utils.importutils as _iu

_orig_getattr = _iu.LazyModule.__getattr__


def _safe_getattr(self, attr):
    # Introspection (inspect.getmodule, importlib, pickling) probes dunder
    # attributes like __file__/__spec__. Answer "not present" instead of
    # forcing the optional lazy import that fails on Windows. Real attribute
    # access (actual classes/functions) is non-dunder and still resolves.
    if attr.startswith("__") and attr.endswith("__"):
        raise AttributeError(attr)
    return _orig_getattr(self, attr)


_iu.LazyModule.__getattr__ = _safe_getattr

from whisperx.__main__ import cli  # noqa: E402

if __name__ == "__main__":
    cli()
