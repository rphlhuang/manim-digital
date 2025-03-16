from manim import *
from .gate import Gate

class OrGate(Gate):
    def __init__(self, label=""):
        super().__init__(label)
        self.or_uparc = ArcBetweenPoints(start=[-1, -1, 0], end=[1, 0, 0], angle=PI / 4)
        self.or_lowarc = ArcBetweenPoints(start=[-1, 1, 0], end=[1, 0, 0], angle=-PI / 4)
        self.or_leftarc = ArcBetweenPoints(start=[-1, 1, 0], end=[-1, -1, 0], angle=-PI / 3)
        self.input_a = [-0.88, 0.7, 0]
        self.input_b = [-0.88, -0.7, 0]
        self.output = [1, 0, 0]
        self.add(self.or_uparc, self.or_lowarc, self.or_leftarc, self.text)

    def shift(self, *vectors):
        super().shift(*vectors)
        shift_vector = vectors[0]
        self.input_a = [sum(x) for x in zip(self.input_a, shift_vector)]
        self.input_b = [sum(x) for x in zip(self.input_b, shift_vector)]
        self.output = [sum(x) for x in zip(self.output, shift_vector)]
        return self

    def get_input_a(self):
        return self.input_a

    def get_input_b(self):
        return self.input_b

    def get_output(self):
        return self.output

    def create(self):
        base_animations = [
            Create(self.or_uparc),
            Write(self.text),
            Create(self.or_lowarc),
            Create(self.or_leftarc)
        ]
        return base_animations + self.get_glued_create_animations()

    def propagate(self):
        if self.input_wires and self.output_wire:
            result = any(wire.state for wire in self.input_wires)
            self.output_wire.set_state(int(result))
