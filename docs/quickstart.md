# Quickstart

Get the Palletizer Full Stack running in under five minutes.

## Prerequisites

You need Python 3.11 or later and `pip`. No additional system dependencies are required for the demo.

## Installation

```bash
git clone https://github.com/iceccarelli/palletizer.git
cd palletizer
pip install -e ".[dev]"
```

## Run the Demo

The built-in demo uses a `DummyRobot` that simulates a 6-axis arm in memory. No real hardware is needed.

```bash
python -m palletizer_full.run
```

You should see log output showing the orchestrator polling sensors, evaluating hazards and executing pick-and-place tasks.

## Run the Tests

```bash
pytest -v
```

All tests should pass. If any fail, please open an issue.

## Next Steps

Once the demo is running, read the [Integration Guide](integration_guide.md) to connect your real robot hardware, or explore the [Architecture Guide](architecture.md) to understand how the system is structured.
