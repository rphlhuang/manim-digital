from manim import *
import os
import sys

# Add parent directory to path to allow running from examples folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LogicGates import DFlipFlop, Wire, VerilogParser, WaveformGroup, simulate_verilog

class DFFTutorialScene(Scene):
    def construct(self):
        sv_file = os.path.join(os.path.dirname(__file__), "dff.sv")
        latch_v = os.path.join(os.path.dirname(__file__), "sr_latch.v")
        vcd_temp = os.path.join(os.path.dirname(__file__), "dff_sim.vcd")
        vcd_file = simulate_verilog(sv_file, vcd_output=vcd_temp)
        
        # 1. Title
        title_text = Text("Introduction to Sequential Logic", font_size=40, weight=BOLD, font="sans-serif")
        subtitle_text = Text("The D Flip-Flop", font_size=32, color=YELLOW, font="sans-serif")
        title_group = VGroup(title_text, subtitle_text).arrange(DOWN)
        
        self.play(Write(title_group))
        self.wait(1)
        self.play(title_group.animate.to_edge(UP).scale(0.8))
        
        # 2. Structural Latch via Verilog Parser
        latch_text = Text("Low Level: SR Latch built from Gates", font_size=28, font="sans-serif").next_to(title_group, DOWN, buff=0.5)
        self.play(Write(latch_text))
        
        # Create diagram using VerilogParser
        parser = VerilogParser(latch_v)
        gates = parser.generate_gates()
        
        # Manually distribute the SR Latch gates 
        gates['o1'].move_to(UP * 1.5 + LEFT * 1)
        gates['n1'].move_to(UP * 1.5 + RIGHT * 2)
        gates['o2'].move_to(DOWN * 1.5 + LEFT * 1)
        gates['n2'].move_to(DOWN * 1.5 + RIGHT * 2)
        
        circuit = parser.route_wires()
        circuit.scale(0.5).shift(UP * 0.5)
        
        self.play(*parser.create(), run_time=2)
        self.wait(2)
        
        self.play(FadeOut(latch_text), FadeOut(circuit))

        # 3. Block Level Diagram
        block_text = Text("Block Level: The D-FlipFlop", font_size=28, font="sans-serif").to_edge(UP).shift(DOWN * 0.5)
        self.play(Write(block_text))
        
        dff = DFlipFlop()
        dff.scale(0.8).shift(RIGHT * 3 + UP * 0.5)
        
        self.play(*dff.create())
        self.wait(1)

        # 4. Waveforms
        wave_text = Text("Waveform Simulation", font_size=28, font="sans-serif").next_to(block_text, DOWN, buff=0.5)
        self.play(Write(wave_text))
        
        # Plotted signals from vcd: clk, d, q_beh
        waveforms = WaveformGroup(vcd_file, signals_to_plot=["clk", "d", "q_beh"], width=6, height_per_signal=0.5)
        waveforms.scale(0.8).shift(LEFT * 3)
        
        self.play(waveforms.create())
        self.wait(3)

        # Outro
        outro = Text("Notice how Q only updates when CLK rises!", font_size=24, color=GREEN, font="sans-serif").next_to(waveforms, DOWN)
        self.play(Write(outro))
        self.wait(3)
        
        self.play(FadeOut(Group(*self.mobjects)))
