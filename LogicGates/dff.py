from manim import *
from .gate import Gate

class DFlipFlop(Gate):
    def __init__(self, label="DFF"):
        super().__init__(label)
        self.rect = Rectangle(width=2, height=3)
        self.d_label = Text("D", font="sans-serif").scale(0.5).move_to(self.rect.get_left() + RIGHT * 0.3 + UP * 0.8)
        self.q_label = Text("Q", font="sans-serif").scale(0.5).move_to(self.rect.get_right() + LEFT * 0.3 + UP * 0.8)
        
        # Clock indicator triangle
        clk_p1 = self.rect.get_left() + DOWN * 0.5 + UP * 0.2
        clk_p2 = self.rect.get_left() + DOWN * 0.5 + DOWN * 0.2
        clk_p3 = self.rect.get_left() + RIGHT * 0.2 + DOWN * 0.5
        self.clk_triangle = Polygon(clk_p1, clk_p2, clk_p3, color=WHITE)

        self.input_d = self.rect.get_left() + UP * 0.8
        self.input_clk = self.rect.get_left() + DOWN * 0.5
        self.output_q = self.rect.get_right() + UP * 0.8

        self.text.move_to(self.rect.get_bottom() + DOWN * 0.5)

        self.add(self.rect, self.d_label, self.q_label, self.clk_triangle, self.text)

        self.wire_d = None
        self.wire_clk = None
        
        self.last_clk_state = 0
        self.q_state = 0

    def get_input_d(self):
        return self.input_d

    def get_input_clk(self):
        return self.input_clk

    def get_output_q(self):
        return self.output_q

    def shift(self, *vectors):
        super().shift(*vectors)
        shift_vector = vectors[0]
        self.input_d = [sum(x) for x in zip(self.input_d, shift_vector)]
        self.input_clk = [sum(x) for x in zip(self.input_clk, shift_vector)]
        self.output_q = [sum(x) for x in zip(self.output_q, shift_vector)]
        return self

    def add_input_wire_d(self, wire):
        self.wire_d = wire
        self.add_input_wire(wire)

    def add_input_wire_clk(self, wire):
        self.wire_clk = wire
        self.add_input_wire(wire)

    def create(self):
        base_animations = [
            Create(self.rect),
            Write(self.d_label),
            Write(self.q_label),
            Create(self.clk_triangle),
            Write(self.text)
        ]
        return base_animations + self.get_glued_create_animations()

    def propagate(self):
        if self.wire_d and self.wire_clk and self.output_wire:
            clk_val = self.wire_clk.state
            d_val = self.wire_d.state

            # Positive edge triggered
            if clk_val == 1 and self.last_clk_state == 0:
                self.q_state = d_val

            self.last_clk_state = clk_val
            self.output_wire.set_state(self.q_state)
