from __future__ import annotations

import logging
from pathlib import Path


def setup_logging(log_dir: str = "logs", level: int = logging.INFO) -> Path:
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    file_path = log_path / "trading_bot.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(file_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    return file_path

