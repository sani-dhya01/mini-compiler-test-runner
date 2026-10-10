#!/usr/bin/env python3
"""Compile small C++ tests with multiple optimization levels and compare results."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "tests"
BUILD_DIR = ROOT / ".build"
DEFAULT_LEVELS = ["O0", "O2"]


def choose_compiler(requested: str | None) -> str | None:
    if requested:
        return shutil.which(requested)
    return shutil.which("g++") or shutil.which("clang++")


def compile_test(compiler: str, source: Path, level: str, output: Path):
    command = [compiler, "-std=c++17", f"-{level}", str(source), "-o", str(output)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return False, result.stderr.strip() or f"compiler exited with {result.returncode}"
    return True, ""


def run_binary(binary: Path):
    try:
        result = subprocess.run(
            [str(binary)], capture_output=True, text=True, timeout=5
        )
        return {
            "status": "ok" if result.returncode == 0 else "runtime-failure",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "returncode": None,
            "stdout": "",
            "stderr": "Program exceeded the 5-second timeout.",
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare C++ test results across optimization levels."
    )
    parser.add_argument(
        "--compiler", help="Compiler executable, e.g. g++ or clang++"
    )
    parser.add_argument(
        "--levels", nargs="+", default=DEFAULT_LEVELS,
        choices=["O0", "O1", "O2", "O3", "Os", "Og"],
        help="Optimization levels to compare (default: O0 O2)",
    )
    args = parser.parse_args()

    compiler = choose_compiler(args.compiler)
    if not compiler:
        print("ERROR: No C++ compiler found. Install g++ or clang++, or pass --compiler.")
        return 2

    tests = sorted(TEST_DIR.glob("*.cpp"))
    if not tests:
        print(f"No .cpp tests found in {TEST_DIR}")
        return 2

    BUILD_DIR.mkdir(exist_ok=True)
    print(f"Compiler: {compiler}")
    print(f"Optimization levels: {', '.join('-' + x for x in args.levels)}")
    print("Note: mismatches are investigation signals, not proof of a compiler bug.\n")

    total = 0
    failed = 0

    for source in tests:
        total += 1
        print(f"[{source.name}]")
        observations = {}

        for level in args.levels:
            binary = BUILD_DIR / f"{source.stem}_{level}"
            try:
                ok, message = compile_test(compiler, source, level, binary)
            except subprocess.TimeoutExpired:
                ok, message = False, "Compilation exceeded the 30-second timeout."

            if not ok:
                observations[level] = {"status": "compile-failure", "detail": message}
                print(f"  -{level}: COMPILE FAILURE: {message.splitlines()[0]}")
                continue

            result = run_binary(binary)
            observations[level] = result
            if result["status"] == "ok":
                print(f"  -{level}: exit={result['returncode']}, output={result['stdout'].strip()!r}")
            else:
                print(f"  -{level}: {result['status'].upper()}: {result['stderr'].strip()!r}")

        valid = [
            (level, result) for level, result in observations.items()
            if result["status"] == "ok"
        ]
        signatures = {(result["returncode"], result["stdout"]) for _, result in valid}
        has_failure = any(result["status"] != "ok" for result in observations.values())
        mismatch = len(signatures) > 1

        if mismatch:
            print("  RESULT: OUTPUT MISMATCH — inspect this test and reproduce it.")
        elif has_failure:
            print("  RESULT: TEST/BUILD FAILURE — inspect the details above.")
        else:
            print("  RESULT: PASS — all tested builds produced the same output and exit code.")

        if mismatch or has_failure:
            failed += 1
        print()

    print(f"Summary: {total - failed}/{total} tests passed; {failed} test(s) need investigation.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
