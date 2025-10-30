# core/memory.py
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

PROJECTS_FILE = Path("data") / "projects.json"

def load_projects() -> Dict[str, Any]:
    if not PROJECTS_FILE.exists():
        return {}
    with PROJECTS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_projects(projects: Dict[str, Any]) -> None:
    PROJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PROJECTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
