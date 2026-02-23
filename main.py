import json
import sys
from pathlib import Path

from schema.circuit_schema import CircuitModel
from converter.json_to_qiskit import build_circuit
from validation.circuit_validator import sanity_check


def run(json_path: str) -> None:
    path = Path(json_path)
    raw = json.loads(path.read_text(encoding="utf-8"))

    # 1) Schema validation (LLM output constraints included)
    circuit_model = CircuitModel.model_validate(raw)

    # 2) Build circuit
    qc = build_circuit(circuit_model)

    # 3) Sanity checks
    sanity_check(qc, depth_limit=circuit_model.depth_limit)

    # 4) Output
    print("\n--- Circuit Summary ---")
    print(f"Qubits in Circuit : {qc.num_qubits}")
    print(f"Circuit Depth     : {qc.depth()}")
    print(f"Operations        : {len(qc.data)}\n")

    print(qc.draw(output="text"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py llm_output/valid_sample.json")
        raise SystemExit(1)
    run(sys.argv[1])