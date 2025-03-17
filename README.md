# manim-digital
A Manim library that implements combinational and sequential digital logic components. It provides classes to represent wires, nets (groups of wires), and logic gates (such as AND and OR). The library supports state propagation and dynamic animations of connected components. Inspired by Daniel Wu's [LogicGates.py](https://github.com/Daniel20010822/Manim-animation/blob/main/LogicGates.py).


https://github.com/user-attachments/assets/fcfd61ef-fd94-423b-a332-e7529de6cb7c


## Getting Started
- Install Manim (Community Version): https://docs.manim.community/en/stable/installation.html
    - Note: LaTeX modules will take a while to install, and are not required for this library.
    - On Mac, pipx is recommended.
- Run `manim -pqh example.py` in examples/ to render the video in high quality (-qh), and instantly play back (-p)

# Docs

- **Wire** (inherits from `Line`)
  - Represents a circuit wire with a logical state (0 or 1) and visual appearance (white for 0, red for 1).
  - Tracks whether it’s connected as a gate input or output.
- **Net** (inherits from `Group`)
  - Manages a collection of Wire objects that share a common state.
  - Handles state propagation across wires within the net.
- **Gate** (abstract base, inherits from `Group`)
  - Provides common functionality for logic gates including attaching wires, animating creation/uncreation, and cascading state propagation.
  - Child classes: **AndGate**, **OrGate**, **NotGate**.
- **AndGate** (inherits from `Gate`)
  - Implements an AND gate: the output is high only when all input wires are high.
- **OrGate** (inherits from `Gate`)
  - Implements an OR gate: the output is high when any input wire is high.
- **NotGate** (inherits from `Gate`)
  - Implements a NOT gate: the output is the inversion of the single input wire’s state.

## Key Functions and Arguments

### Wire
- **Constructor**:  
  `Wire(start, end, abs_end=False, allow_diagonal=False, allow_any_angle=False)`  
  - `start`: Starting coordinate (or offset when `abs_end=True`).
  - `end`: Relative offset or absolute coordinate (if `abs_end=True`).
  - `abs_end`: When `True`, treats `end` as an absolute coordinate and `start` as an offset from it.
- **Methods**:
  - `set_state(state)`: Sets the wire's logical state (0 or 1) and updates its color.
  - `update_color()`: Changes the wire’s color (red for high, white for low).
  - `connect_to_gate_input(gate)`: Marks this wire as connected to a gate input.
  - `connect_to_gate_output(gate)`: Marks this wire as connected to a gate output.

### Net
- **Constructor**:  
  `Net()`
- **Methods**:
  - `add_wire(wire)`: Adds a Wire object to the net.
  - `create()`: Returns animations (`Create`) for all wires in the net.
  - `propagate(input_wire)`: Sets all wires in the net to the state of the given input wire.
  - `propagate_through(input_wire)`: Cascades state propagation through the net and any connected gates.
  - `uncreate()`: Returns animations (`Uncreate`) for all wires in the net.

### Gate (Abstract Base)
- **Constructor**:  
  `Gate(label="")`
  - `label`: The gate’s label.
- **Methods**:
  - `glue(component)`: Adds a component (e.g., a visual element) to the gate.
  - `add_input_wire(wire)`: Attaches a wire as an input (and marks it as such).
  - `add_output_wire(wire)`: Attaches a wire as the output (and marks it as such).
  - `get_glued_create_animations()`: Returns animations for all wires attached (glued) to the gate.
  - `uncreate()`: Returns animations to remove the gate and its attached wires.
  - `propagate()`: (Abstract) Logic for updating the gate’s output based on its inputs.
  - `propagate_through()`: Cascades propagation from the gate through connected nets/gates.

### AndGate (inherits from Gate)
- **Constructor**:  
  `AndGate(label="")`
- **Additional Attributes**:  
  Defines its geometry (lines, arcs) and wire attachment points.
- **Methods**:
  - `create()`: Returns Create animations for the gate’s components plus attached wires.
  - `propagate()`: Implements the AND logic—output is high only if all input wires are high.

### OrGate (inherits from Gate)
- **Constructor**:  
  `OrGate(label="")`
- **Additional Attributes**:  
  Defines its geometry (arcs, etc.) and wire attachment points.
- **Methods**:
  - `create()`: Returns Create animations for the gate’s components plus attached wires.
  - `propagate()`: Implements the OR logic—output is high if any input wire is high.

### NotGate (inherits from Gate)
- **Constructor**:  
  `NotGate(label="NOT")`
- **Additional Attributes**:  
  Uses a triangle and a circle (inversion bubble) to represent the NOT gate.
  - Defines an input point (typically on the left) and an output point (at the inversion bubble).
- **Methods**:
  - `create()`: Returns Create animations for the NOT gate’s components plus attached wires.
  - `propagate()`: Implements the NOT logic—output is the inversion of its single input wire’s state.

---

## Typical Workflow

- Create a manim `Scene` for each video clip (all your code must go within `construct()`):

```python
class ExampleScene(Scene):
    def construct(self):
```

- Create gate objects and shift them into position:

```python
and_gate = AndGate(label="AND").shift([-4, -1, 0])
```

- Create wires and attach them to the gate:

```python
and_i_1 = Wire(start=[-1, 0, 0], end=and_gate.get_input_a(), abs_end=True)
and_i_2 = Wire(start=[-1, 0, 0], end=and_gate.get_input_b(), abs_end=True)
and_o = Wire(start=and_gate.get_output(), end=[1, 0, 0], abs_end=False)
```

- Attach wires to gate:

```python
and_gate.add_input_wire(and_i_1)
and_gate.add_input_wire(and_i_2)
and_gate.add_output_wire(and_o)
```

- Add wires to net so logic propagation can happen to all wires in net:

```python
and_i_1_w = Net(and_i_1)
and_i_2_w = Net(and_i_2)
and_o_w = Net(and_o)
```

- Animate the creation of the gate (which automatically creates the wires we attached earlier):

```python
self.play(and_gate.create()) # .create() functions return a list of Animations 
                             # that must be played using Scene.play()
```

- Set the state of your wires and propagate them through:

```python
and_i_1.set_state(1)
and_i_2.set_state(0)
and_i_1_w.propagate_through(and_i_1)
self.wait(1)
```

- Animate the "uncreation" of the gate (which automatically uncreates the wires we attached earlier)

```python
self.play(and_gate.uncreate())
self.wait(0.75) # manim is greedy with the animation cut-off point;
                # make sure you pause at the end of every animation
```

---

## Future Additions
- Additional gate types (e.g., XOR, NAND, NOR).
- Extended logic propagation through complex circuits.
- Customization of gate appearances and behaviors.
- Sequential logic components (e.g. latches, flip-flops)
    - with timing? :O
