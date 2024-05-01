import importlib.util
import os
import pathlib
import platform
import shutil
import sys
import tempfile
import urllib.request


def _target_platform():
    return (
        f'py{sys.version_info.major}.{sys.version_info.minor}'
        f'-{platform.system().lower()}-{platform.machine().lower()}'
    )


_version = os.getenv('TRITON_WHEEL_VERSION', '3.0.0b2')
_debug = os.getenv('TRITON_XPU_DEBUG_IMPORT') is not None
_platform = _target_platform()
_cache_home = pathlib.Path(os.getenv('XDG_CACHE_HOME') or os.path.expanduser('~/.cache'))
_cache_path = _cache_home / 'triton-xpu' / _version / _platform
_store_path = _cache_path / 'libtriton.so'

if _debug:
    print(f'Version: {_version}, platform: {_platform}')

if not _cache_path.is_dir():
    if _debug:
        print(f'Creating {_cache_path}')
    _cache_path.mkdir(parents=True, exist_ok=True)

if not _store_path.is_file():
    url = f'https://github.com/intel/intel-xpu-backend-for-triton/releases/download/v{_version}/libtriton-{_platform}.zip'
    if _debug:
        print(f'Downloading {url}')
    with tempfile.TemporaryDirectory(dir=_cache_path) as temp_dir:
        temp_path = pathlib.Path(temp_dir)
        temp_file = temp_path / 'libtriton.zip'
        urllib.request.urlretrieve(url, filename=temp_file)
        shutil.unpack_archive(filename=temp_file, extract_dir=temp_path)
        # since temp_dir is a subdirectory on the same filesystem, the replacement below should be
        # atomic,if the destination exists  it will be replaced silently, but let's do the last
        # check.
        if not _store_path.exists():
            os.replace(src=temp_path / 'libtriton.so', dst=_store_path)

if _store_path.is_file():
    if _debug:
        print(f'{_store_path} exists')

_spec = importlib.util.spec_from_file_location("triton._C.libtriton", _store_path)
_libtriton = importlib.util.module_from_spec(_spec)
sys.modules['triton._C.libtriton'] = _libtriton
_spec.loader.exec_module(_libtriton)
