# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Litepipe is a lightweight Python library for building data pipelines using operator-overloaded syntax inspired by Apache Beam. Published on PyPI as `litepipe`. Requires Python >= 3.9 and has zero runtime dependencies.

## Commands

```bash
# Run all tests
coverage run -m pytest litepipe/tests

# Run a single test file
pytest litepipe/tests/test_pipeline.py

# Run a single test
pytest litepipe/tests/test_pipeline.py::PipelineTest::test_single_transform
```

## Architecture

The library has two core classes in `litepipe/`:

- **`Transform`** (`transform.py`) — Abstract base class. Subclasses implement `expand(self, input)` which must `yield` outputs. Transforms chain via `|` (pipe) operator (`__or__`) to form a DAG of children. `>>` sets a display label. `__call__` drives execution: applies `expand` to each input element, collects results, then recursively calls children.

- **`Pipeline`** (`pipeline.py`) — Entry point. Use `p | Create([...]) | SomeTransform()` to wire up the DAG. `p.run()` iterates the root transform and collects results into a list. `p.graph` returns a string representation of the transform tree.

Key built-in transforms in `transform.py`:
- `Create(items)` — injects initial data into the pipeline
- `GroupBy` — groups elements by first character (overrides `get_key()` for custom grouping)

### Execution model

Pipelines are lazily evaluated using generators. `Transform.__call__` yields results, and branching (multiple children on one transform) fans out execution. A transform can yield multiple outputs per input to implement fan-out or filtering (yield nothing to drop).

### Testing utility

`litepipe/util/testing.py` exports `assert_equal` for order-independent list comparison — also exposed at package level via `from litepipe import assert_equal`.

### Writing a custom Transform

Subclass `Transform` and implement `expand(self, input)` as a generator. See `litepipe/examples/transforms.py` for patterns (identity, map, filter, fan-out, aggregation after GroupBy).
