# Mini Compiler Test Runner

A small beginner-friendly project that uses Python to compile and run C++ programs with multiple optimization settings, then compares their observable results.

> This is a learning tool, not a formal compiler verifier. A difference between builds is a signal to investigate, not proof of a compiler bug. Test programs should avoid undefined behavior.

## What it does

- Compiles each `.cpp` test with `-O0` and `-O2` (or another selected optimization level).
- Runs each compiled executable with a timeout.
- Compares exit codes and standard output.
- Reports compilation errors, runtime errors, timeouts, and output mismatches.
- Includes small tests for arithmetic, loops, branches, and boundary values.

## Requirements

- Python 3.9 or newer
- A C++ compiler available from the terminal: `g++` or `clang++`
- macOS, Linux, or Windows with a suitable compiler installed

Check your tools:

```bash
python3 --version
g++ --version
# Or, if using Clang:
clang++ --version
```

On macOS, `clang++` is usually available after installing Apple's Command Line Tools:

```bash
xcode-select --install
```

## Run it

From this project directory:

```bash
python3 src/runner.py
```

Use a specific compiler:

```bash
python3 src/runner.py --compiler clang++
```

Use different optimization levels:

```bash
python3 src/runner.py --levels O0 O1 O2 O3
```

The default compiler is `g++` if available, otherwise `clang++`. If neither is found, the runner prints an actionable error.

## Add your own test

1. Create a `.cpp` file in `tests/`.
2. Make it print a deterministic result to standard output.
3. Avoid undefined behavior (for example, signed integer overflow, reading uninitialized variables, or out-of-bounds array access).
4. Run the test runner again.

Example:

```cpp
#include <iostream>
int main() {
    int total = 0;
    for (int i = 1; i <= 10; ++i) total += i;
    std::cout << total << '\n';
    return 0;
}
```

## Project structure

```text
mini-compiler-test-runner/
├── README.md
├── .gitignore
├── tests/
│   ├── arithmetic.cpp
│   ├── branches.cpp
│   ├── boundary_values.cpp
│   └── loops.cpp
└── src/
    └── runner.py
```

## Current limitations

- Compares output and exit codes only; it does not prove semantic equivalence.
- Does not automatically generate random programs or minimize failing inputs.
- Does not inspect assembly or LLVM IR.
- A mismatch should be reproduced and investigated before drawing conclusions.

## Skills demonstrated

Python subprocess automation, C++ compilation, test harness design, exit-code and output checking, command-line interfaces, and basic compiler optimization experimentation.
