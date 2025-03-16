# LogicGates/__init__.py

from .wire_net import Wire, Net
from .gate import Gate
from .and_gate import AndGate
from .or_gate import OrGate

__all__ = ["Wire", "Net", "Gate", "AndGate", "OrGate"]
