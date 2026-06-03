"""Runtime path helpers for iml-pptx scripts.

Prefer explicit environment variables, then Codex bundled runtime defaults.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path


RUNTIME_ROOT = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node"
DEFAULT_NODE_MODULES = RUNTIME_ROOT / "node_modules"
DEFAULT_LUCIDE = DEFAULT_NODE_MODULES / "lucide" / "dist" / "esm" / "icons"
DEFAULT_NODE = RUNTIME_ROOT / "bin" / "node"


def _env_path(*names: str) -> Path | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return Path(value).expanduser()
    return None


def resolve_lucide_dir(candidate: str | Path | None = None) -> Path:
    candidates = [
        Path(candidate).expanduser() if candidate else None,
        _env_path("IML_PPTX_LUCIDE_DIR", "LUCIDE_DIR"),
        DEFAULT_LUCIDE,
    ]
    for path in candidates:
        if path and path.exists():
            return path
    searched = ", ".join(str(p) for p in candidates if p)
    raise FileNotFoundError(
        "lucide icon directory not found. Set IML_PPTX_LUCIDE_DIR or pass --lucide-dir. "
        f"Searched: {searched}"
    )


def resolve_node_bin(candidate: str | Path | None = None) -> Path:
    env_candidate = _env_path("IML_PPTX_NODE_BIN", "NODE_BIN")
    path_node = shutil.which("node")
    candidates = [
        Path(candidate).expanduser() if candidate else None,
        env_candidate,
        DEFAULT_NODE,
        Path(path_node) if path_node else None,
    ]
    for path in candidates:
        if path and path.exists():
            return path
    searched = ", ".join(str(p) for p in candidates if p)
    raise FileNotFoundError(
        "node executable not found. Set IML_PPTX_NODE_BIN or pass --node-bin. "
        f"Searched: {searched}"
    )


def resolve_node_modules(candidate: str | Path | None = None) -> Path:
    candidates = [
        Path(candidate).expanduser() if candidate else None,
        _env_path("IML_PPTX_NODE_MODULES", "NODE_PATH"),
        DEFAULT_NODE_MODULES,
    ]
    for path in candidates:
        if path and path.exists():
            return path
    searched = ", ".join(str(p) for p in candidates if p)
    raise FileNotFoundError(
        "node_modules directory not found. Set IML_PPTX_NODE_MODULES or pass --node-modules. "
        f"Searched: {searched}"
    )
