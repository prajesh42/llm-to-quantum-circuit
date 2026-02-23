from schema.circuit_schema import CircuitModel
from converter.json_to_qiskit import build_circuit

def test_build_circuit_empty_gates():
    raw = {
        "qubits": 2,
        "allowed_gates": ["h", "cx", "rz"],
        "gates": []
    }
    model = CircuitModel.model_validate(raw)
    qc = build_circuit(model)
    assert qc.num_qubits == 2
    assert qc.depth() == 0

def test_build_circuit_with_gates():
    raw = {
        "qubits": 3,
        "allowed_gates": ["h", "cx", "rz"],
        "gates": [
            {"type": "h", "target": 0},
            {"type": "cx", "control": 0, "target": 1},
            {"type": "rz", "target": 2, "theta": 1.0},
        ],
        "depth_limit": 50
    }
    model = CircuitModel.model_validate(raw)
    qc = build_circuit(model)
    assert qc.num_qubits == 3
    assert qc.depth() == 3

def test_build_circuit_with_gates():
    raw = {
        "qubits": 3,
        "allowed_gates": ["h", "cx", "rz"],
        "gates": [
            {"type": "h", "target": 0},
            {"type": "cx", "control": 0, "target": 1},
            {"type": "rz", "target": 2, "theta": 1.0},
        ],
        "depth_limit": 50
    }
    model = CircuitModel.model_validate(raw)
    qc = build_circuit(model)
    assert qc.num_qubits == 3
    assert qc.depth() == 2

def test_build_circuit_gate_order():
    raw = {
        "qubits": 2,
        "allowed_gates": ["h", "cx", "rz"],
        "gates": [
            {"type": "h", "target": 0},
            {"type": "cx", "control": 0, "target": 1},
            {"type": "rz", "target": 1, "theta": 1.0},
        ]
    }
    model = CircuitModel.model_validate(raw)
    qc = build_circuit(model)
    inst_h = qc.data[0]
    inst_cx = qc.data[1]
    inst_rz = qc.data[2]
    assert inst_h.operation.name == "h"
    assert inst_cx.operation.name == "cx"
    assert inst_rz.operation.name == "rz"
    