import pytest
from schema.circuit_schema import GateModel, CircuitModel


# ----------------------------
# GateModel tests
# ----------------------------

def test_gate_h_valid():
    g = GateModel(type="h", target=0)
    assert g.type == "h"
    assert g.target == 0
    assert g.control is None
    assert g.theta is None


def test_gate_rx_requires_theta():
    with pytest.raises(ValueError, match="rx gate requires 'theta'"):
        GateModel(type="rx", target=0)


def test_gate_rz_accepts_theta():
    g = GateModel(type="rz", target=1, theta=1.0)
    assert g.type == "rz"
    assert g.theta == 1.0


def test_gate_h_rejects_theta():
    with pytest.raises(ValueError, match="h gate must not have 'theta'"):
        GateModel(type="h", target=0, theta=1.0)


def test_gate_cx_requires_control():
    with pytest.raises(ValueError, match="cx gate requires 'control'"):
        GateModel(type="cx", target=1)


def test_gate_cx_control_target_must_differ():
    with pytest.raises(ValueError, match="cx gate control and target must be different"):
        GateModel(type="cx", control=0, target=0)


def test_gate_cx_valid():
    g = GateModel(type="cx", control=0, target=1)
    assert g.type == "cx"
    assert g.control == 0
    assert g.target == 1
    assert g.theta is None


# ----------------------------
# CircuitModel tests
# ----------------------------

def test_circuit_valid_with_allowed_gates():
    raw = {
        "qubits": 2,
        "allowed_gates": ["h", "cx", "rz"],
        "gates": [
            {"type": "h", "target": 0},
            {"type": "cx", "control": 0, "target": 1},
            {"type": "rz", "target": 1, "theta": 1.0},
        ],
        "depth_limit": 50
    }
    model = CircuitModel.model_validate(raw)
    assert model.qubits == 2
    assert len(model.allowed_gates) == 3
    assert len(model.gates) == 3
    assert model.depth_limit == 50


def test_circuit_rejects_gate_not_in_allowed_gates():
    raw = {
        "qubits": 2,
        "allowed_gates": ["h", "cx"],   # rz not allowed
        "gates": [{"type": "rz", "target": 0, "theta": 1.0}],
    }
    with pytest.raises(ValueError, match="Gate\\(s\\) not allowed by allowed_gates"):
        CircuitModel.model_validate(raw)


def test_circuit_default_allowed_gates_allows_rx():
    raw = {
        "qubits": 1,
        "gates": [{"type": "rx", "target": 0, "theta": 0.5}],
    }
    model = CircuitModel.model_validate(raw)
    assert model.qubits == 1
    assert model.gates[0].type == "rx"


def test_circuit_qubits_must_be_positive():
    raw = {
        "qubits": 0,
        "gates": []
    }
    with pytest.raises(Exception):
        CircuitModel.model_validate(raw)


def test_circuit_qubits_max_64():
    raw = {
        "qubits": 65,
        "gates": []
    }
    with pytest.raises(Exception):
        CircuitModel.model_validate(raw)


def test_circuit_rejects_invalid_gate_structure():
    raw = {
        "qubits": 2,
        "gates": [{"type": "rz", "target": 0}]  # missing theta
    }
    with pytest.raises(ValueError, match="rz gate requires 'theta'"):
        CircuitModel.model_validate(raw)