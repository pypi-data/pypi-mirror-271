import shutil
from pathlib import Path

from .runtime import ctx


def copy(src: Path, dst: Path):
    if not ctx.is_dry_run():
        shutil.copy(src, dst)


def make_archive(archive_name: Path, format: str, src: Path):
    if not ctx.is_dry_run():
        shutil.make_archive(str(archive_name), format, src)


def unpack_archive(src: Path, dst: Path):
    if not ctx.is_dry_run():
        shutil.unpack_archive(src, dst)
