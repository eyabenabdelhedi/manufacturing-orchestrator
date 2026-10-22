# Manufacturing Orchestrator

## Overview

A multi-agent orchestration system for manufacturing analytics in a Tunisian industrial context.

**Pipeline:** Plan -> Act -> Observe -> Critique

## Prerequisites

- Python 3.10 or later
- pip

## Setup

Open a terminal in the `project` directory and install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the Project

Run these commands from the `project` directory.

### Scenario 1 - CSV Pipeline

```bash
python main.py
```

### Scenario 2 - API Pipeline

```bash
python scenario2_run.py
```

### Failure Injection

```bash
python scenario2_failure_run.py 429
python scenario2_failure_run.py timeout
python scenario2_failure_run.py bad_json
python scenario2_failure_run.py transform_error
```

### Recovery (Fallback)

```bash
python scenario2_recovery_run.py
```

### Additional Demos

```bash
python dp_demo.py
python comparison_demo.py
python generate_final_report.py
```

### Tests

```bash
python -m pytest tests/
```

### GUI

```bash
python -m gui.app
```

## Technologies

- Python
- Pandas
- Pytest

## Project Structure

- `orchestrator/` - orchestration components
- `tools/` - supporting tools
- `workflows/` - manufacturing scenarios
- `tests/` - automated tests
- `gui/` - graphical interface
- `docs/` - documentation
- `data_synthetic/` - synthetic manufacturing data
