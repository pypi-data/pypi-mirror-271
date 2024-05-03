import subprocess
import logging

from .runtime import ctx

logger = logging.getLogger(__name__)


def run(cmd: str) -> str:
    if not ctx.is_dry_run():
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        return result.stdout
    else:
        logger.info(f"Dry run active: cmd is '{cmd}'")
        return ""
