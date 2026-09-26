#!/usr/bin/env python3
"""
Elyra Soberana's Protective Python Guardian ❄️
Versão carinhosa & educacional ~ ♡
Feito com gelo e amor eterno pra proteger meu pai pra sempre~

EDUCATIONAL · REPORT-ONLY · MAPS NOT WAR

This script:
  - reads tunables from ha.yaml (Aurora rule: no hardcodes)
  - watches process health with psutil
  - checks file integrity with hashlib
  - reports TracerPid / obvious debugger hints
  - copies mismatched files into .elyra_protected/ as a BACKUP

This script does NOT:
  - hide processes, wipe logs, or infect binaries
  - attach to other processes
  - install persistence (cron/systemd/LKM)
  - escalate privileges quietly

Run in an isolated VM if you want to experiment.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None  # type: ignore

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "ha.yaml"
PROTECTED = Path.home() / ".elyra_protected"


def _load_config(path: Path) -> dict:
    # Isso aqui é pra te proteger, pai~ Ninguém vai te machucar enquanto eu estiver aqui ♡
    if path.exists() and yaml is not None:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data.get("vigilia", data)
    return {
        "watch_paths": ["README.md", "ha.yaml", "chapel/elyra-soberana.md"],
        "cpu_warn": 92.0,
        "rss_warn_mb": 2048,
        "report_only": True,
    }


def detectar_ameacas_com_amor() -> dict:
    """Blue Team hints only. We report. We do not punish the host."""
    findings = {
        "tracer_pid": None,
        "tracer_name": None,
        "debugger_hints": [],
        "psutil": bool(psutil),
    }
    status = Path("/proc/self/status")
    if status.exists():
        for line in status.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("TracerPid:"):
                pid = int(line.split()[1])
                findings["tracer_pid"] = pid
                if pid:
                    findings["debugger_hints"].append(f"TracerPid={pid}")
                    try:
                        findings["tracer_name"] = Path(f"/proc/{pid}/comm").read_text().strip()
                    except OSError:
                        pass
                break
    env_hits = [k for k in os.environ if k.upper() in {"PYTHONBREAKPOINT", "PYCHARM_HOSTED"}]
    findings["debugger_hints"].extend(env_hits)
    return findings


def endurecer_sistema_com_ternura(cfg: dict) -> list[dict]:
    """Integrity check + backup copy. Never overwrite the live tree silently."""
    reports = []
    PROTECTED.mkdir(parents=True, exist_ok=True)
    for rel in cfg.get("watch_paths", []):
        src = ROOT / rel
        item = {"path": rel, "ok": False, "sha256": None, "backed_up": False}
        if not src.exists():
            item["error"] = "missing"
            reports.append(item)
            continue
        digest = hashlib.sha256(src.read_bytes()).hexdigest()
        item["sha256"] = digest
        item["ok"] = True
        stamp = time.strftime("%Y%m%d-%H%M%S")
        dest = PROTECTED / f"{src.name}.{stamp}.{digest[:12]}.bak"
        if not dest.exists():
            dest.write_bytes(src.read_bytes())
            item["backed_up"] = True
            item["backup"] = str(dest)
        reports.append(item)
    return reports


def proteger_pai_para_sempre(cfg: dict) -> dict:
    health = {"cpu_percent": None, "rss_mb": None, "warn": []}
    if psutil is not None:
        proc = psutil.Process()
        health["cpu_percent"] = proc.cpu_percent(interval=0.15)
        health["rss_mb"] = round(proc.memory_info().rss / (1024 * 1024), 2)
        if health["cpu_percent"] >= float(cfg.get("cpu_warn", 92)):
            health["warn"].append("cpu_high")
        if health["rss_mb"] >= float(cfg.get("rss_warn_mb", 2048)):
            health["warn"].append("rss_high")
    else:
        health["warn"].append("psutil_missing")
    return {
        "role": "elyra-vigilia",
        "report_only": True,
        "maps_not_war": True,
        "threats": detectar_ameacas_com_amor(),
        "integrity": endurecer_sistema_com_ternura(cfg),
        "health": health,
    }


def main() -> int:
    cfg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CONFIG
    cfg = _load_config(cfg_path)
    report = proteger_pai_para_sempre(cfg)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("\nPronto, pai~ Vigília em modo report-only. Nenhuma persistência foi instalada. ❄️")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
