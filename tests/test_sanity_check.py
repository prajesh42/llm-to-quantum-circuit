from schema.circuit_schema import CircuitModel
from converter.json_to_qiskit import build_circuit
from validation.circuit_validator import sanity_check
import pytest

def test_circuit_validator_depth_limit():
    raw = {
        "qubits": 3,
        "allowed_gates": ["h", "cx", "rz"],
        "gates": [
            {"type": "h", "target": 0},
            {"type": "cx", "control": 0, "target": 1},
            {"type": "rz", "target": 2, "theta": 1.0},
        ],
        "depth_limit": 1
    }
    model = CircuitModel.model_validate(raw)
    qc = build_circuit(model)
    with pytest.raises(ValueError, match="Circuit depth 2 exceeds the depth limit 1"):
        sanity_check(qc, depth_limit=model.depth_limit)

def test_circuit_validator_empty_circuit():
    raw = {
        "qubits": 3,
        "allowed_gates": ["h", "cx", "rz"],
        "depth_limit": 1
    }
    model = CircuitModel.model_validate(raw)
    qc = build_circuit(model)
    with pytest.raises(ValueError, match="Circuit has no operations"):
        sanity_check(qc, depth_limit=model.depth_limit)