import numpy as np
from manim import *
from .gate import Gate 

class NotGate(Gate):
    def __init__(self, label="NOT"):
        super().__init__(label)
        self.not_tri = Polygon(
            [1 - np.sqrt(3), 1, 0],
            [1 - np.sqrt(3), -1, 0],
            [1, 0, 0],
            color=WHITE
        )
        self.not_cir = Circle(radius=0.2, color=WHITE).move_to([1.2, 0, 0])
        self.input_point = [1 - np.sqrt(3), 0, 0]
        self.output_point = [1.4, 0, 0]
        
        self.add(self.not_tri, self.not_cir, self.text)

    def get_input(self):
        return self.input_point
    
    def get_output(self):
        return self.output_point
    
    def shift(self, *vectors):
        super().shift(*vectors)
        shift_vector = vectors[0]
        self.input_point = [sum(x) for x in zip(self.input_point, shift_vector)]
        self.output_point = [sum(x) for x in zip(self.output_point, shift_vector)]
        return self

    def create(self):
        base_animations = [
            Create(self.not_tri),
            Create(self.not_cir),
            Write(self.text)
        ]
        return base_animations + self.get_glued_create_animations()

    def propagate(self):
        print("NotGate propagate")
        if self.input_wires and self.output_wire:
            result = not self.input_wires[0].state
            self.output_wire.set_state(result)
