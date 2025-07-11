import subprocess
import shutil

from typing import Optional
from .options import DittoOptions

MISSING_DITTO_ERROR = (
    "'ditto' command not found. Please ensure it is installed and available in PATH."
)

def run_ditto(args: list) -> None:
    if shutil.which('ditto') is None:
        raise FileNotFoundError(MISSING_DITTO_ERROR)

    cmd = ['ditto'] + args
    subprocess.run(cmd, check=True)

class PyDitto:
    @staticmethod
    def copy(src: str, dst: str, options: Optional[DittoOptions] = None) -> None:
        opts = options or DittoOptions()
        args = opts.to_flags(for_mode='copy') + [src, dst]
        run_ditto(args)

    @staticmethod
    def archive(src: str, archive_path: str, options: Optional[DittoOptions] = None) -> None:
        opts = options or DittoOptions()
        args = ['-c', *opts.to_flags(for_mode='archive'), src, archive_path]
        run_ditto(args)

    @staticmethod
    def extract(archive_path: str, dst: str, options: Optional[DittoOptions] = None) -> None:
        opts = options or DittoOptions()
        args = ['-x', *opts.to_flags(for_mode='extract'), archive_path, dst]
        run_ditto(args)

copy = PyDitto.copy
archive = PyDitto.archive
extract = PyDitto.extract
