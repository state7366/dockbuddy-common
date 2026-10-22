# dockbuddy-common

DockBuddy 的通用科学计算/系统工具底座，从 `pipeline/common.py` 抽出，与 DockBuddy 的路径/阶段/对接逻辑解耦。

## 安装

```bash
pip install dockbuddy-common \
  --index-url https://pypi.cnb.cool/vcinex/bioinfo/-/packages/simple
```

## 工具

| 函数 | 说明 |
|---|---|
| `normalize_pdb_id(pdb_id)` | PDB ID 大写归一化 |
| `default_seed()` | 默认随机种子（42，`DOCK_SEED` 可覆盖） |
| `resolve_device("auto")` | 解析 torch device（GPU 优先） |
| `openmm_platform()` | OpenMM 平台（默认 CPU，可切 GPU） |
| `env_float(name, default)` | 读环境变量浮点 |
| `run_cmd(cmd, ...)` | 跨平台执行子进程 |
| `attach_file_log` / `detach_file_log` | 文件日志挂载/卸载 |

零硬依赖（torch/openmm 懒加载）。
