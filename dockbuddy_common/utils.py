# -*- coding: utf-8 -*-
"""utils.py —— 通用科学计算/系统工具(从 DockBuddy common.py 抽出的纯工具底座)。

纯标准库 + 可选依赖(torch/openmm 懒加载), 与 DockBuddy 的路径/阶段/对接工具解耦。
"""
from __future__ import annotations

import logging
import os
import shlex
import subprocess
from typing import Dict, List, Optional, Tuple

LOG = logging.getLogger("dockbuddy_common")


def normalize_pdb_id(pdb_id: str) -> str:
    """PDB ID 归一化为大写去空白(空串原样返回)。"""
    return (pdb_id or "").strip().upper()


def default_seed() -> int:
    """默认随机种子(42, 环境变量 DOCK_SEED 可覆盖)。"""
    try:
        return int(os.environ.get("DOCK_SEED", "42"))
    except ValueError:
        return 42


def env_float(name: str, default: float) -> float:
    """读环境变量浮点; 空/非数字回退缺省。"""
    raw = os.environ.get(name) or ""
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        LOG.warning("环境变量 %s=%r 非数字, 回退缺省 %g", name, raw, default)
        return default


def resolve_device(explicit: str = "") -> str:
    """解析 torch device: 显式 'cuda'/'cpu' 用之; 空/'auto' 自动探测(GPU 优先)。"""
    if explicit and explicit != "auto":
        return explicit
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
    except ImportError:
        pass
    return "cpu"


def openmm_platform():
    """OpenMM 计算平台: 默认 CPU; DOCK_OPENMM_PLATFORM/OPENMM_DEFAULT_PLATFORM 可切 GPU。"""
    import openmm as mm
    name = (os.environ.get("DOCK_OPENMM_PLATFORM")
            or os.environ.get("OPENMM_DEFAULT_PLATFORM") or "CPU")
    try:
        return mm.Platform.getPlatformByName(name)
    except Exception:  # noqa: BLE001
        return mm.Platform.getPlatformByName("CPU")


def run_cmd(cmd: List[str], timeout: Optional[float] = None, check: bool = False,
            env: Optional[Dict[str, str]] = None, cwd: Optional[str] = None,
            shell: bool = False) -> subprocess.CompletedProcess:
    """跨平台执行子进程(默认不强制 shell)。"""
    LOG.debug("run_cmd: %s", " ".join(shlex.quote(c) for c in cmd))
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                          check=check, env=env, cwd=cwd, shell=shell)


def attach_file_log(log_path: str, logger_names: Tuple[str, ...] = ("dockpipeline",)):
    """把日志文件附加到指定 logger(幂等), 返回 handler 供 detach_file_log 卸载。"""
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", datefmt="%H:%M:%S")
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(fmt)
    handler._dock_log_path = os.path.abspath(log_path)  # type: ignore[attr-defined]
    for name in logger_names:
        lg = logging.getLogger(name)
        if any(isinstance(h, logging.FileHandler) and
               getattr(h, "_dock_log_path", None) == handler._dock_log_path
               for h in lg.handlers):
            continue
        lg.addHandler(handler)
    return handler


def detach_file_log(handler, logger_names: Tuple[str, ...] = ("dockpipeline",)) -> None:
    """卸载 attach_file_log 附加的句柄。"""
    if handler is None:
        return
    for name in logger_names:
        try:
            logging.getLogger(name).removeHandler(handler)
        except ValueError:
            pass
    try:
        handler.close()
    except Exception:  # noqa: BLE001
        pass
