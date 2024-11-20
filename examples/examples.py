import sys
import os
sys.path.append(os.path.abspath(".."))
from LogicGates import *

from manim import *



class Test(Scene):
    config.background_color = BLACK
    def construct(self):
        andgate1 = AndGate(label="AND")
        self.play(*andgate1.get_create_animations())
        self.wait(0.2)
        wire1 = Line(start=andgate1.get_output_point(), end=[2, 0, 0])
        andgate1.glue(wire1)
        self.play(Create(wire1))
        self.wait(0.2)
        self.play(andgate1.animate.shift([-4, 1, 0]))
        self.play(andgate1.animate.scale(0.5))

        orgate1 = OrGate(label="OR")
        self.play(*orgate1.get_create_animations())
        self.wait(0.2)