"""Repository-wide pytest configuration."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
SRC_STR = str(SRC_PATH)
if SRC_STR not in sys.path:
    sys.path.insert(0, SRC_STR)

_spec = importlib.util.spec_from_file_location(
    "cubedynamics", SRC_PATH / "cubedynamics" / "__init__.py"
)
if _spec is None or _spec.loader is None:  # pragma: no cover - defensive
    raise ImportError("Unable to locate cubedynamics package for tests")

_cubedynamics = importlib.util.module_from_spec(_spec)
sys.modules["cubedynamics"] = _cubedynamics
_spec.loader.exec_module(_cubedynamics)

assert hasattr(_cubedynamics, "pipe"), "cubedynamics import missing pipe attribute"
