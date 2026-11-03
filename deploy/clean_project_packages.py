"""Remove stale project package files/metadata before an offline image upgrade."""

import shutil
import sysconfig
from pathlib import Path

site = Path(sysconfig.get_paths()["purelib"])
for package in (
    "tributo",
    "tributo_knova",
    "tributo_broker_redis",
    "tributo_algorithms_boosting",
    "ray_clickhouse",
):
    shutil.rmtree(site / package, ignore_errors=True)
    for metadata in site.glob(f"{package}-*.dist-info"):
        shutil.rmtree(metadata)
