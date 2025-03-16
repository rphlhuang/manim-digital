from manim import *
from .gate import Gate

class AndGate(Gate):
    def __init__(self, label=""):
        super().__init__(label)
        self.and_uphor = Line(start=[0, 1, 0], end=[-1, 1, 0])
        self.and_lowhor = Line(start=[0, -1, 0], end=[-1, -1, 0])
        self.and_ver = Line(start=[-1, 1, 0], end=[-1, -1, 0])
        self.and_arc = Arc(radius=1.0, start_angle=-PI / 2, angle=PI)
        self.input_a = [-1, 0.7, 0]
        self.input_b = [-1, -0.7, 0]
        self.output = [1, 0, 0]
        self.add(self.and_uphor, self.and_lowhor, self.and_ver, self.and_arc, self.text)

    def get_input_a(self):
        return self.input_a

    def get_input_b(self):
        return self.input_b

    def get_output(self):
        return self.output

    def shift(self, *vectors):
        super().shift(*vectors)
        shift_vector = vectors[0]
        self.input_a = [sum(x) for x in zip(self.input_a, shift_vector)]
        self.input_b = [sum(x) for x in zip(self.input_b, shift_vector)]
        self.output = [sum(x) for x in zip(self.output, shift_vector)]
        return self

    def create(self):
        base_animations = [
            Create(self.and_uphor),
            Write(self.text),
            Create(self.and_arc),
            Create(self.and_lowhor),
            Create(self.and_ver)
        ]
        return base_animations + self.get_glued_create_animations()

    def propagate(self):
        if self.input_wires and self.output_wire:
            result = all(wire.state for wire in self.input_wires)
            self.output_wire.set_state(int(result))
