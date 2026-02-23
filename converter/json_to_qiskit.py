from qiskit import QuantumCircuit
from schema.circuit_schema import CircuitModel

# Builds the quantum circuit based on circuit model
def build_circuit(model: CircuitModel) -> QuantumCircuit:
    qc = QuantumCircuit(model.qubits)

    for gate in model.gates:
        if gate.type == "h":
            qc.h(gate.target)
        elif gate.type == "x":
            qc.x(gate.target)
        elif gate.type == "rx":
            qc.rx(gate.theta, gate.target)
        elif gate.type == "ry":
            qc.ry(gate.theta, gate.target)
        elif gate.type == "rz":
            qc.rz(gate.theta, gate.target)
        elif gate.type == "cx":
            qc.cx(gate.control, gate.target)
        else:
            raise ValueError(f"Unsupported gate: {gate.type}")
    
    return qc