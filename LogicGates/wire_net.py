from manim import *

EPSILON = 0.00001

class Wire(Line):
    def __init__(self, start, end, abs_end=False, allow_diagonal=False, allow_any_angle=False):
        # default to relative end point
        end_point = [sum(x) for x in zip(start, end)]
        if abs_end:
            actual_start = [end[i] + start[i] for i in range(len(end))]
            end_point = end
            start = actual_start

        # restrict to horizontal, vertical, or 45-degree increments
        dx = end_point[0] - start[0]
        dy = end_point[1] - start[1]

        if not allow_diagonal and not allow_any_angle:
            if abs(dx) > EPSILON and abs(dy) > EPSILON:
                raise ValueError(f"Wire can only be horizontal or vertical unless allow_diagonal or allow_any_angle is True.\nCurrently, dx = {dx}, dy = {dy}, with points {start} and {end_point}.")
        elif (abs(dx) != abs(dy)) and (dx != 0) and (dy != 0) and not allow_any_angle:
            raise ValueError(f"Wire must be horizontal, vertical, or at 45-degree increments, unless allow_any_angle is True.\nCurrently, dx = {dx}, dy = {dy}, with points {start} and {end_point}.")

        super().__init__(start=start, end=end_point)
        self.state = 0  # logical low and high
        self.abs_start = start
        self.abs_end = end_point
        self.connected_gate_input = None  # gate this wire is an input to
        self.connected_gate_output = None  # gate this wire is an output from

    def set_state(self, state):
        self.state = state
        self.update_color()

    def update_color(self):
        self.set_color(RED if self.state else WHITE)

    def connect_to_gate_input(self, gate):
        self.connected_gate_input = gate

    def connect_to_gate_output(self, gate):
        self.connected_gate_output = gate

class Net(Group):
    def __init__(self):
        super().__init__()
        self.wires = []

    def add_wire(self, wire):
        if not isinstance(wire, Wire):
            raise ValueError("Only Wire objects can be added to a Net.")
        self.wires.append(wire)
        self.add(wire)

    def create(self):
        return [Create(wire) for wire in self.wires]

    def propagate(self, input_wire):
        if input_wire not in self.wires:
            raise ValueError("The selected input wire is not part of this Net.")
        for wire in self.wires:
            wire.set_state(input_wire.state)

    def propagate_through(self, input_wire):
        self.propagate(input_wire)
        for wire in self.wires:
            if wire.connected_gate_input:
                print(f"Propagating wire {wire.abs_start} -> {wire.abs_end} through gate {wire.connected_gate_input.label}")
                wire.connected_gate_input.propagate_through()

    def uncreate(self):
        return [Uncreate(wire) for wire in self.wires]
