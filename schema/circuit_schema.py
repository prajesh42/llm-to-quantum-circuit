from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator

#Gate types supported in the prototype
GateType = Literal["h", "x", "rx", "ry", "rz", "cx"]

#Defines the structure for the gate
class GateModel(BaseModel):
    type: GateType
    target: int
    control: Optional[int] = None
    theta: Optional[float] = None

    #validates the gate parameters based on gate type
    @model_validator(mode="after")
    def validate_gate_fields(self) -> "GateModel":
        #control is required only for cx gate
        if self.type == "cx":
            if self.control is None:
                raise ValueError("cx gate requires 'contorl'")
            if self.control == self.target:
                raise ValueError("cx gate control and target must be different")

        #theta is required only for rotation gates    
        if self.type in {"rx", "ry", "rz"}:
            if self.theta is None:
                raise ValueError(f"{self.type} gate requires 'theta'")
        else:
            if self.theta is not None:
                raise ValueError(f"{self.type} gate must not have 'theta'")

        return self
    
#Defines the structure of the circuit
class CircuitModel(BaseModel):
    qubits: int = Field(..., ge=1, le=64)
    gates: List[GateModel] = Field(default_factory=list)

    allowed_gates: List[GateType] = Field(default_factory=lambda: ["h", "x", "rx", "ry", "rz", "cx"])
    depth_limit: int = Field(default=200, ge=1, le=10_000)

    #validates allowed gates for the given circuit
    @model_validator(mode="after")
    def validate_allowed_gate_set(self) -> "CircuitModel":
        allowed = set(self.allowed_gates)
        used = {g.type for g in self.gates}
        not_allowed = used - allowed
        if not_allowed:
            raise ValueError(f"Gate(s) not allowed by allowed_gates: {sorted(not_allowed)}")
        return self
