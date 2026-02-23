from qiskit import QuantumCircuit

def sanity_check(qc: QuantumCircuit, depth_limit: int) -> None:
    depth = qc.depth()
    # Depth validation
    if depth > depth_limit:
        raise ValueError(f"Circuit depth {depth} exceeds the depth limit {depth_limit}")
    
    # Basic qubit sanity
    if qc.num_qubits <= 0:
        raise ValueError("Circuit has no qubit")
    
    # Ensure circuit has at least 1 operation
    if len(qc.data) == 0:
        raise ValueError("Circuit has no operations (empty circuit)")
