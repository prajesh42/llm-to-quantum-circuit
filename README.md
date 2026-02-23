# LLM-to-Quantum Circuit Generator (Prototype)

A small prototype that converts structured LLM JSON outputs into
validated, executable Qiskit circuits. The project emphasizes safety by
validating LLM-generated descriptions (Pydantic schemas + custom checks)
before building a Qiskit circuit.

## Quick Summary

- Input: JSON describing qubit count, allowed gates, and a gate list.
- Validation: Pydantic schema + gate-level and circuit-level checks.
- Output: A Qiskit `QuantumCircuit` ready for simulation or transpilation.

## Features

- Enforces an allowed gate set
- Requires `theta` for rotation gates (e.g., `rz`)
- Requires `control` for `cx` gates
- Validates qubit indices against declared `qubits`
- Configurable depth limits to prevent overly large circuits
- Unit-tested validation and conversion pipeline

## Repository Layout

- `main.py` — CLI entry that loads a JSON file and builds the circuit
- `converter/json_to_qiskit.py` — JSON → Qiskit circuit builder
- `schema/circuit_schema.py` — Pydantic models for LLM JSON outputs
- `validation/circuit_validator.py` — custom validation rules
- `llm_output/` — example inputs (valid and invalid samples)
- `tests/` — pytest unit tests

## Installation

Create and activate a virtual environment and install dependencies. Examples for common platforms:

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Windows (cmd.exe):

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

Linux / macOS (bash / zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional: use Conda instead of venv:

```bash
conda create -n qiskit_env python=3.10
conda activate qiskit_env
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -q
```

## Running

Run the converter on a JSON file (works on Windows, macOS, Linux):

```bash
python main.py llm_output/valid_sample.json
```

Notes:
- Ensure your virtual environment or Conda env is activated before running.
- Try the example inputs provided to see validation behavior:
	- `llm_output/valid_sample.json` should build a circuit successfully.
	- `llm_output/invalid_sample.json` demonstrates validation errors.

Run the unit tests with `pytest`:

```bash
python -m pytest -q
```

If you need to inspect or simulate the produced `QuantumCircuit`, open
the converter output or modify `main.py` to serialize the circuit
(QASM or pickling) for later use with Qiskit simulators or backends.

## Example JSON

```json
{
	"qubits": 2,
	"allowed_gates": ["h", "cx", "rz"],
	"depth_limit": 50,
	"gates": [
		{"type": "h", "target": 0},
		{"type": "cx", "control": 0, "target": 1},
		{"type": "rz", "target": 1, "theta": 1.57}
	]
}
```

## Development notes

- The Pydantic models live in `schema/circuit_schema.py` and should be the
	single source of truth for input shape and types.
- Additional semantic checks are in `validation/circuit_validator.py`.
- `converter/json_to_qiskit.py` expects validated input and focuses only
	on deterministic Qiskit construction.

If you change the schema, update tests in `tests/` accordingly.

## Next steps / Ideas

- Add optional serialization of the produced Qiskit circuit (QASM or
	`QuantumCircuit` pickling).
- Add CLI flags for simulation backend selection and transpile options.
- Integrate an LLM-runner that produces JSON followed by automatic
	validation before any execution step.

## License & Contributing

This repository is a small prototype — open to improvements. If you'd like
to contribute, open an issue or PR with focused changes and tests.

-----------------------------------------------------------------------
