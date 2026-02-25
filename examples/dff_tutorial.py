from manim import *
from LogicGates import DFlipFlop, Wire

class DFFTutorialScene(Scene):
    def construct(self):
        # 1. Title
        title_text = Text("Introduction to Sequential Logic", font_size=40, weight=BOLD, font="sans-serif")
        subtitle_text = Text("The D Flip-Flop", font_size=32, color=YELLOW, font="sans-serif")
        title_group = VGroup(title_text, subtitle_text).arrange(DOWN)
        
        self.play(Write(title_group))
        self.wait(2)
        self.play(title_group.animate.to_edge(UP).scale(0.8))
        
        # 2. Concept text
        concept_text = Text(
            "Combinational logic output depends only on current inputs.\n"
            "Sequential logic introduces MEMORY using a CLOCK.",
            font_size=24,
            font="sans-serif",
            t2c={"Combinational logic": ORANGE, "Sequential logic": GREEN, "MEMORY": YELLOW, "CLOCK": BLUE}
        ).next_to(title_group, DOWN, buff=0.5)

        self.play(FadeIn(concept_text))
        self.wait(3)
        self.play(FadeOut(concept_text))

        # 3. Draw the DFF component
        dff = DFlipFlop()
        dff.shift(RIGHT * 2 + DOWN * 0.5)
        
        dff_explanation = Text("D Flip-Flop", font_size=28, font="sans-serif").next_to(dff, UP, buff=0.5)
        self.play(Write(dff_explanation), *dff.create())
        self.wait(1)

        # 4. Inputs and Outputs Setup
        wire_d = Wire(start=LEFT * 3, end=dff.get_input_d(), abs_end=True)
        wire_clk = Wire(start=LEFT * 3, end=dff.get_input_clk(), abs_end=True)
        wire_q = Wire(start=dff.get_output_q(), end=RIGHT * 2)

        dff.add_input_wire_d(wire_d)
        dff.add_input_wire_clk(wire_clk)
        dff.add_output_wire(wire_q)

        d_label = Text("D (Data)", font_size=24, font="sans-serif").next_to(wire_d.abs_start, LEFT)
        clk_label = Text("CLK (Clock)", font_size=24, color=BLUE, font="sans-serif").next_to(wire_clk.abs_start, LEFT)
        q_label = Text("Q (Output)", font_size=24, color=RED, font="sans-serif").next_to(wire_q.abs_end, RIGHT)


        self.play(
            Create(wire_d), Create(wire_clk), Create(wire_q),
            Write(d_label), Write(clk_label), Write(q_label)
        )
        self.wait(1)

        # 5. Animate toggling D back and forth while CLK is 0, showing Q doesn't change
        d_val_text = Text("D changes, but NO clock edge...", font_size=24, color=YELLOW, font="sans-serif").to_edge(DOWN)
        self.play(Write(d_val_text))
        
        for _ in range(2):
            wire_d.set_state(1)
            dff.propagate_through()
            self.wait(1)
            wire_d.set_state(0)
            dff.propagate_through()
            self.wait(1)

        self.play(FadeOut(d_val_text))

        # 6. Set D high, trigger positive clock edge
        d_val_text = Text("D is HIGH. Triggering a rising clock edge!", font_size=24, color=GREEN, font="sans-serif").to_edge(DOWN)
        self.play(Write(d_val_text))
        
        wire_d.set_state(1)
        dff.propagate_through()
        self.wait(0.5)

        wire_clk.set_state(1)  # Positive edge
        dff.propagate_through()
        self.wait(2)
        
        self.play(FadeOut(d_val_text))

        # 7. Bring CLK low, change D, trigger another edge
        wire_clk.set_state(0)
        dff.propagate_through()
        
        d_val_text = Text("Clock is low. Q remembers its state even if D changes.", font_size=24, color=YELLOW, font="sans-serif").to_edge(DOWN)
        self.play(Write(d_val_text))
        
        wire_d.set_state(0)
        dff.propagate_through()
        self.wait(2)
        self.play(FadeOut(d_val_text))

        d_val_text = Text("Triggering another rising edge to capture D=0.", font_size=24, color=GREEN, font="sans-serif").to_edge(DOWN)
        self.play(Write(d_val_text))
        
        wire_clk.set_state(1)  # Positive edge
        dff.propagate_through()
        self.wait(2)
        
        self.play(FadeOut(d_val_text))

        # 8. Outro
        outro_text = Text("D Flip-Flops store 1 bit of data on the rising clock edge!", font_size=32, font="sans-serif").to_edge(DOWN)
        self.play(Write(outro_text))
        self.wait(3)

        self.play(
            FadeOut(title_group),
            FadeOut(dff_explanation),
            Uncreate(wire_d), Uncreate(wire_clk), Uncreate(wire_q),
            FadeOut(d_label), FadeOut(clk_label), FadeOut(q_label),
            FadeOut(outro_text),
            *dff.uncreate()
        )
        self.wait(1)
