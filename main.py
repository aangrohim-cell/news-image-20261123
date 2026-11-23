"""make.fun bounty news-image-20261123.

The image that sums up the world news of Monday 23 November 2026 is
committed to this repository as entry.png. This entrypoint only copies
those bytes to /output/entry.png. It uses the Python standard library,
touches no network, and writes identical bytes on every run.
"""

import os
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT_DIR.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT_DIR / "entry.png")
