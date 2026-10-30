import os
import subprocess
import sys
from pathlib import Path


SERVE = Path(__file__).resolve().parents[1] / "serve.py"

SCRIPT = """
import importlib.metadata
import runpy
import sys
import types

importlib.metadata.version = lambda name: sys.argv[1]
for name in ("vllm", "vllm.entrypoints", "vllm.entrypoints.cli",
             "vllm.entrypoints.cli.main", "modeling",
             "modeling.modeling_monkeyocrv2_vllm_011",
             "modeling.modeling_monkeyocrv2_vllm"):
    module = types.ModuleType(name)
    module.__path__ = []
    sys.modules[name] = module
sys.modules["vllm.entrypoints.cli.main"].main = lambda: None
runpy.run_path(sys.argv[2])
"""


def test_supported_and_unsupported_versions():
    for version, supported in (("0.11.2", True), ("0.11.0", True),
                               ("0.25.1", True), ("0.12.0", False),
                               ("0.10.2", False)):
        result = subprocess.run(
            [sys.executable, "-c", SCRIPT, version, str(SERVE)],
            capture_output=True, text=True, env=os.environ.copy(),
        )
        assert (result.returncode == 0) == supported, result.stderr
