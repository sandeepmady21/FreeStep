#!/usr/bin/env python3
"""Compile and execute the shipped C++ core and actual Arduino adapter.

No duplicated Python controller model. Host GPIO/I2C stubs do not prove hardware
safety, sensor accuracy, stopping distance, or suitability for a person.
"""
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parent
compiler = shlex.split(os.environ.get("CXX", "c++"))
if not compiler or not shutil.which(compiler[0]):
    raise SystemExit("Install a C++17 compiler (clang++ or g++) to run native tests.")
with tempfile.TemporaryDirectory(prefix="freestep-test-") as tmp:
    for name in ("controller_test", "adapter_test"):
        output = Path(tmp) / name
        subprocess.run(compiler + ["-std=c++17", "-Wall", "-Wextra", "-Werror",
                       "-fsanitize=address,undefined", "-fno-omit-frame-pointer",
                       "-I" + str(root / "tests/stubs"),
                       str(root / "tests" / (name + ".cpp")), "-o", str(output)], check=True)
        subprocess.run([str(output)], check=True)
