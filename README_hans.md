# Evaluation Pytest-html

## Installation / first reports

```bash
run in codespace

./start down && ./start
pip install tox
tox
Generated html report: file:///tmp/pytest-of-codespace/pytest-0/test_render_collapsed0/report.html


pip install -e .
pytest --html=report.html --self-contained-html testing/test_unit.py 

pytest --html=report.html --self-contained-html testing/test_hans.py
Generated html report: file:///workspaces/experiment_pytest-html/report.html
```

Negative: dependency in pyproject.toml:

```ini
[tool.hatch.build.hooks.custom]
path = "scripts/npm.py"
```

## Experiments

### Experiment pytest

```json
            "name": "pytest testing/test_hans.py",
            "type": "debugpy",
            "module": "pytest",
            "request": "launch",
            "args": [
                "-s",
                "--html=report.html",
                "--self-contained-html",
                "testing/test_hans.py", "testing/test_sub/test_detailed.py"
            ],
            "console": "integratedTerminal",
            "justMyCode": false
```

Creates `report.html`/ `report_data_pytest.json`

### Experiment `testing/hans_report_pytest.py`

First experiment reengineering the pytest callbacks.

### Experiment `testing/hans_report_raw.py`

```json
            "name": "Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false,
```

Try to create data, without the use of callbacks. Removed dependencies to pytest.

Result: testing/hans_report_raw.html

## Evaluation

* Negative: Tightly coupled to pytest.
* Negative: No standard, no junit.xml
* Negative: Interface quite tricky.
* Positive: Single Page Html
* Negative: Uses javascript.
* Questions: cascading reports? Could not find the code/hint anymore...
* Positive: Small and selfcontained
* Negative: Some logic is hidden in the hooks. As far as I know, a hook may not be called directly.
