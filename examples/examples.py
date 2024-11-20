import sys
import os
sys.path.append(os.path.abspath(".."))
from LogicGates import *

from manim import *

class Test(Scene):
    config.background_color = BLACK
    def construct(self):
        andgate1 = AndGate(label="AND")
        andgate1.animate_create(self)
        self.wait(0.2)

        wire1 = Line(start=andgate1.get_output_point(), end=[2, 0, 0])
        # TODO: make this depending on input_point_a's y values instead of hard code
        wire2 = Line(start=andgate1.get_input_point_a(), end=[-2, 0.7, 0]) 
        wire3 = Line(start=andgate1.get_input_point_b(), end=[-2, -0.7, 0])
        andgate1.glue(wire1)
        andgate1.glue(wire2)
        andgate1.glue(wire3)

        self.play(Create(wire1), Create(wire2), Create(wire3))
        self.wait(0.2)

        self.play(andgate1.animate.shift([-4, 1, 0]))
        self.play(andgate1.animate.scale(0.5))
        orgate1 = OrGate(label="OR")
        orgate1.animate_create(self)
        self.wait(0.2)

        self.play(andgate1.uncreate_all())
        self.wait(0.2)

        self.play(orgate1.uncreate_all())
        self.wait(0.2)
