import sys
import os
sys.path.append(os.path.abspath(".."))
from LogicGates import *

from manim import *

class Test(Scene):
    config.background_color = BLACK
    def construct(self):
        andgate1 = AndGate(label="AND")
        self.play(andgate1.create())
        self.wait(0.2)

        wire1 = Wire(start=andgate1.get_output(), end=[2, 0, 0])
        wire2 = Wire(start=andgate1.get_input_a(), end=[-2, 0, 0]) 
        wire3 = Wire(start=andgate1.get_input_b(), end=[-2, 0, 0])
        andgate1.glue(wire1)
        andgate1.glue(wire2)
        andgate1.glue(wire3)

        self.play(Create(wire1), Create(wire2), Create(wire3))
        self.wait(0.2)

        self.play(andgate1.animate.shift([-4, 1, 0]))
        self.play(andgate1.animate.scale(0.5))
        orgate1 = OrGate(label="OR")
        self.play(orgate1.create())
        self.wait(0.2)

        self.play(andgate1.uncreate())
        self.wait(0.2)

        self.play(orgate1.uncreate())
        self.wait(0.2)

class PropagationTest(Scene):
    def construct(self):
        and_gate = AndGate("AND")
        inputA = Wire(start=and_gate.get_input_a(), end=[-2, 0, 0])
        inputB = Wire(start=and_gate.get_input_b(), end=[-2, 0, 0])
        output = Wire(start=and_gate.get_output(), end=[2, 0, 0])

        and_gate.add_input_wire(inputA)
        and_gate.add_input_wire(inputB)
        and_gate.add_output_wire(output)

        self.play(and_gate.create())
        self.play(Create(inputA), Create(inputB), Create(output))

        inputA.set_state(1)
        inputB.set_state(0)
        and_gate.propagate(self)
        self.wait(1)

        inputB.set_state(1)
        and_gate.propagate(self)
        self.wait(1)

        inputA.set_state(0)
        and_gate.propagate(self)
        self.wait(1)

        inputB.set_state(0)
        and_gate.propagate(self)
        self.wait(1)

        self.play(and_gate.uncreate())
        self.wait(2)