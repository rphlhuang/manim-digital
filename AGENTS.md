# manim-digital: Agent Summary & TODOs

## Project Summary
`manim-digital` is a library built on top of Manim (Community Version) that implements combinational and sequential digital logic components for animations. It provides foundational classes like `Wire` (for logical paths), `Net` (for grouping and propagating state across connected wires), and `Gate` hierarchies (currently supporting `AndGate`, `OrGate`, and `NotGate`). 
The library's main feature is allowing users to intuitively stitch together logic gates, animate their creation/uncreation, and propagate logical states (1 being HIGH/red, 0 being LOW/white) dynamically through the visual circuit during the animation.

## Refactoring Ideas
1. **Abstract Ports/Pins**: Currently, `Wire` objects connect directly to gates via `gate.get_input_a()`, etc. Refactoring to introduce explicit `Port` or `Pin` classes for inputs and outputs would improve modularity and make it easier to validate connections.
2. **Automatic State Propagation**: The current implementation requires manual calls to `set_state()` and `propagate_through()` at every step. Implementing an event-driven listener pattern or a topological sort-based graph evaluation would allow the circuit to update automatically when an input changes.
3. **Module Consolidation**: Rather than exposing everything flatly or having separate files, restructure the repo into `core` (for Wire, Net, Gate base), `combinational` (AND, OR, etc.), and eventually `sequential` modules.

## TODO List
- [ ] Implement additional foundational combinational gates (NAND, NOR, XOR, XNOR).
- [ ] Refactor the connection system to use explicit `InputPort` and `OutputPort` classes instead of directly binding `Wire` to `Gate`.
- [ ] Implement an automatic, reactive state propagation system so users don't have to manually propagate state changes.
- [ ] Add basic sequential logic components (e.g., D-Flip-Flop, SR-Latch, Clock signal generator).
- [ ] Create a `Circuit` wrapper class to streamline Manim animation generation (e.g., auto-grouping and ordering component animations).
