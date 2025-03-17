import sys
import os
sys.path.append(os.path.abspath(".."))
from LogicGates import *
from manim import *


class ExampleScene(Scene):
    def construct(self):
        title = Text("Logic Gates in Manim").shift([0, 3, 0])

        and_gate = AndGate(label="AND").shift([-4, -1, 0])
        and_i_1 = Wire(start=[-1, 0, 0], end=and_gate.get_input_a(), abs_end=True)
        and_i_2 = Wire(start=[-1, 0, 0], end=and_gate.get_input_b(), abs_end=True)
        and_o = Wire(start=and_gate.get_output(), end=[1, 0, 0], abs_end=False)
        and_gate.add_input_wire(and_i_1)
        and_gate.add_input_wire(and_i_2)
        and_gate.add_output_wire(and_o)
        and_i_1_w = Net(and_i_1)
        and_i_2_w = Net(and_i_2)
        and_o_w = Net(and_o)


        or_gate = OrGate(label="OR").shift([4, -1, 0])
        or_i_1 = Wire(start=[-1, 0, 0], end=or_gate.get_input_a(), abs_end=True)
        or_i_2 = Wire(start=[-1, 0, 0], end=or_gate.get_input_b(), abs_end=True)
        or_o = Wire(start=or_gate.get_output(), end=[1, 0, 0], abs_end=False)
        or_gate.add_input_wire(or_i_1)
        or_gate.add_input_wire(or_i_2)
        or_gate.add_output_wire(or_o)
        or_i_1_w = Net(or_i_1)
        or_i_2_w = Net(or_i_2)
        or_o_w = Net(or_o)

        not_gate = NotGate(label="NOT").shift([0, -1, 0])
        not_i = Wire(start=[-1, 0, 0], end=not_gate.get_input(), abs_end=True)
        not_o = Wire(start=not_gate.get_output(), end=[1, 0, 0], abs_end=False)
        not_gate.add_input_wire(not_i)
        not_gate.add_output_wire(not_o)
        not_i_w = Net(not_i)
        not_o_w = Net(not_o)

        self.play(Write(title), and_gate.create(), or_gate.create(), not_gate.create())
        self.wait(1)

        and_i_1.set_state(1)
        and_i_2.set_state(0)
        and_i_1_w.propagate_through(and_i_1)
        or_i_1.set_state(1)
        or_i_2.set_state(0)
        or_i_1_w.propagate_through(or_i_1)
        not_i.set_state(1)
        not_i_w.propagate_through(not_i)
        self.wait(1)

        and_i_1.set_state(0)
        and_i_2.set_state(1)
        and_i_1_w.propagate_through(and_i_1)
        or_i_1.set_state(0)
        or_i_2.set_state(1)
        or_i_1_w.propagate_through(or_i_1)
        not_i.set_state(0)
        not_i_w.propagate_through(not_i)
        self.wait(1)

        and_i_1.set_state(1)
        and_i_2.set_state(1)
        and_i_1_w.propagate_through(and_i_1)
        or_i_1.set_state(1)
        or_i_2.set_state(1)
        or_i_1_w.propagate_through(or_i_1)
        not_i.set_state(1)
        not_i_w.propagate_through(not_i)
        self.wait(1)

        and_i_1.set_state(0)
        and_i_2.set_state(0)
        and_i_1_w.propagate_through(and_i_1)
        or_i_1.set_state(0)
        or_i_2.set_state(0)
        or_i_1_w.propagate_through(or_i_1)
        not_i.set_state(0)
        not_i_w.propagate_through(not_i)
        self.wait(2)

        self.play(and_gate.uncreate(), or_gate.uncreate(), not_gate.uncreate(), Uncreate(title))
        self.wait(0.75)