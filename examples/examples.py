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
        and_gate = AndGate()
        or_gate = OrGate().shift([4, -1, 0])
        inputA = Wire(start=and_gate.get_input_a(), end=[-2, 0, 0])
        inputB = Wire(start=and_gate.get_input_b(), end=[-2, 0, 0])
        output = Wire(start=and_gate.get_output(), end=[2, 0, 0], abs_end=False)


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

class NetTest(Scene):
    def construct(self):
        wire1 = Wire(start=[0, 0, 0], end=[2, 0, 0])
        wire2 = Wire(start=[2, 0, 0], end=[4, 0, 0])
        wire3 = Wire(start=[2, 0, 0], end=[2, 2, 0], allow_diagonal=True)

        net = Net()
        net.add_wire(wire1)
        net.add_wire(wire2)
        net.add_wire(wire3)

        self.play(net.create())

        wire1.set_state(1)
        self.wait(1)
        net.propagate()

        self.wait(2)

class ThroughTest(Scene):
    def construct(self):

        and_gate = AndGate("AND")

        # net 1
        wire1a = Wire(start=[-5, 0.7, 0], end=[-3, 0.7, 0], abs_end=True)
        wire1b = Wire(start=[-3, 0.7, 0], end=and_gate.get_input_a(), abs_end=True)
        net1 = Net()
        net1.add_wire(wire1a)
        net1.add_wire(wire1b)

        # net 2
        wire2 = Wire(start=[-3, -0.7, 0], end=and_gate.get_input_b(), abs_end=True)
        net2 = Net()
        net2.add_wire(wire2)

        # net 3
        wire_out = Wire(start=and_gate.get_output(), end=[3, 0, 0])
        net3 = Net()
        net3.add_wire(wire_out)

        and_gate.add_input_wire(wire1b)
        and_gate.add_input_wire(wire2)
        and_gate.add_output_wire(wire_out)

        # play create
        self.play(and_gate.create())
        self.wait(0.5)
        self.play(net1.create(), net2.create(), net3.create())
        self.wait(0.5)

        # propagate logic
        wire1a.set_state(1)
        wire2.set_state(0)
        net1.propagate_through(wire1a)
        self.wait(0.75)

        wire2.set_state(1)
        net2.propagate_through(wire2)
        self.wait(0.75)

        wire1a.set_state(0)
        net1.propagate_through(wire1a)
        self.wait(0.75)

        wire2.set_state(0)
        net2.propagate_through(wire2)
        self.wait(1)

        # play uncreate
        self.play(and_gate.uncreate())
        self.wait(1)
        self.play(net1.uncreate(), net2.uncreate(), net3.uncreate())
        self.wait(2)
