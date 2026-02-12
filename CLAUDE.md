# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

This is the `neew` project. It is in early setup — no build system, test framework, or linting has been configured yet.

## Repository Structure

```
neew/
├── CLAUDE.md        # This file
├── README.md        # Project readme
```

## Suggested Commands

No tooling is configured yet. Below are common commands to add once a stack is chosen.

### Node.js / TypeScript

- **Install dependencies**: `npm install`
- **Build**: `npm run build`
- **Test (all)**: `npm test`
- **Test (single)**: `npm test -- path/to/test`
- **Lint**: `npm run lint`
- **Format**: `npm run format`
- **Dev server**: `npm run dev`

### Python

- **Install dependencies**: `pip install -r requirements.txt` or `pip install -e .`
- **Build**: `python -m build`
- **Test (all)**: `pytest`
- **Test (single)**: `pytest path/to/test.py`
- **Lint**: `ruff check .`
- **Format**: `ruff format .`
- **Type check**: `mypy .`

### Go

- **Build**: `go build ./...`
- **Test (all)**: `go test ./...`
- **Test (single)**: `go test ./path/to/package`
- **Lint**: `golangci-lint run`
- **Format**: `gofmt -w .`

### Rust

- **Build**: `cargo build`
- **Test (all)**: `cargo test`
- **Test (single)**: `cargo test test_name`
- **Lint**: `cargo clippy`
- **Format**: `cargo fmt`

### General / CI

- **Git status**: `git status`
- **Git diff**: `git diff`
- **Docker build**: `docker build -t neew .`
- **Docker run**: `docker run neew`

> **Note**: Once a stack is chosen, remove the irrelevant sections and keep only what applies.

## Code Style

No code style conventions have been established yet. Update this section when linters or formatters are configured.
