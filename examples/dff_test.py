from manim import *
from LogicGates import DFlipFlop, Wire

class DFFTestScene(Scene):
    def construct(self):
        dff = DFlipFlop()

        # Inputs
        wire_d = Wire(start=LEFT * 2, end=dff.get_input_d(), abs_end=True)
        wire_clk = Wire(start=LEFT * 2, end=dff.get_input_clk(), abs_end=True)
        
        # Output
        wire_q = Wire(start=dff.get_output_q(), end=RIGHT * 2)

        dff.add_input_wire_d(wire_d)
        dff.add_input_wire_clk(wire_clk)
        dff.add_output_wire(wire_q)

        self.play(*dff.create())

        # Test initial state
        wire_d.set_state(1)
        wire_clk.set_state(0)
        dff.propagate_through()
        self.wait(1)

        # Test no change when D changes and CLK=0
        wire_d.set_state(0)
        dff.propagate_through()
        self.wait(1)

        # Test positive edge trigger
        wire_d.set_state(1)
        wire_clk.set_state(1) # positive edge
        dff.propagate_through()
        self.wait(1)

        # Test D changing while CLK is high (should not change Q)
        wire_d.set_state(0)
        dff.propagate_through()
        self.wait(1)

        # Test negative edge trigger (should not change Q)
        wire_d.set_state(1)
        wire_clk.set_state(0)
        dff.propagate_through()
        self.wait(1)

        self.play(Uncreate(wire_d), Uncreate(wire_clk), Uncreate(wire_q), *dff.uncreate())
        self.wait(1)
