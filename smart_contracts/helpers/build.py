import logging
from pathlib import Path

import beaker

logger = logging.getLogger(__name__)


def build(output_dir: Path, app: beaker.Application) -> Path:
    output_dir = output_dir.resolve()
    output_dir.mkdir(exist_ok=True, parents=True)
    logger.info(f"Exporting {app.name} to {output_dir}")
    specification = app.build()
    specification.export(output_dir)
    return output_dir / "application.json"
