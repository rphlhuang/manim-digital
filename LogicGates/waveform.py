from manim import *
import re

class Waveform(VGroup):
    def __init__(
        self,
        signal_name,
        data,
        max_time=None,
        width=10,
        height=0.75,
        color=YELLOW,
        label_color=WHITE,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.signal_name = signal_name
        self.data = data  # list of (time, val) where val is 0, 1, or 'x'
        self.max_time = max_time if max_time is not None else (data[-1][0] if data else 1)
        self.width_scale = width
        self.height_scale = height
        
        self.waveform_paths = VGroup()
        self.label = Text(signal_name, font_size=24, color=label_color, font="sans-serif")
        
        self.add(self.label)
        self.label.next_to(ORIGIN, LEFT, buff=0.5)
        
        if not data:
            return
            
        points = []
        
        # We need to construct step functions
        current_time = data[0][0]
        current_val = data[0][1]
        
        def get_coords(t, v):
            x = (t / self.max_time) * self.width_scale
            if v == 1 or v == '1':
                y = self.height_scale / 2
            elif v == 0 or v == '0':
                y = -self.height_scale / 2
            else:
                # X or Z state
                y = 0
            return [x, y, 0]

        # initial point
        start_pt = get_coords(0, current_val)
        points.append(start_pt)
        
        for t, v in data:
            if t > current_time:
                # draw horizontally to t
                pt1 = get_coords(t, current_val)
                points.append(pt1)
            
            # then draw vertically to v
            pt2 = get_coords(t, v)
            points.append(pt2)
            
            current_time = t
            current_val = v
            
        if current_time < self.max_time:
            points.append(get_coords(self.max_time, current_val))

        # create lines
        for i in range(len(points)-1):
            line = Line(start=points[i], end=points[i+1], color=color)
            self.waveform_paths.add(line)
            
        # shift waveform_paths to be properly aligned
        self.waveform_paths.next_to(self.label, RIGHT, buff=0.5)
        self.add(self.waveform_paths)
        
    def create(self):
        animations = [Write(self.label)]
        if len(self.waveform_paths) > 0:
            animations.append(Create(self.waveform_paths, run_time=2))
        return animations

import subprocess
import os

def simulate_verilog(sv_file, top_module="testbench", vcd_output="out.vcd"):
    """
    Compiles and simulates a SystemVerilog file using Icarus Verilog.
    Assumes the testbench dumps to `vcd_output`.
    Returns the path to the VCD if successful.
    """
    vvp_file = sv_file.replace(".sv", ".vvp").replace(".v", ".vvp")
    # Compile
    try:
        subprocess.run(["iverilog", "-g2012", "-o", vvp_file, sv_file], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error compiling Verilog: {e.stderr.decode()}")
        raise e
        
    # Simulate
    try:
        subprocess.run(["vvp", vvp_file], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error simulating Verilog: {e.stderr.decode()}")
        raise e
        
    return vcd_output

class VCDParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.signals = {} # mappings of symbol -> name
        self.data = {}    # signal_name -> [(time, val)]
        self.max_time = 0
        self._parse()
        
    def _parse(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
            
        current_time = 0
        in_def = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('$var'):
                parts = line.split()
                if len(parts) >= 5:
                    var_type = parts[1]
                    size = parts[2]
                    symbol = parts[3]
                    name = parts[4]
                    self.signals[symbol] = name
                    self.data[name] = []
            elif line.startswith('$timescale') or line.startswith('$scope') or line.startswith('$date') or line.startswith('$version') or line.startswith('$enddefinitions'):
                continue
            elif line.startswith('#'):
                current_time = int(line[1:].split()[0])
                if current_time > self.max_time:
                    self.max_time = current_time
            elif line.startswith('$dumpvars'):
                continue
            elif line.startswith('$end'):
                continue
            else:
                # Value change
                if line[0] in ['0', '1', 'x', 'z', 'X', 'Z']:
                    val = line[0].lower()
                    symbol = line[1:].strip()
                    if symbol in self.signals:
                        name = self.signals[symbol]
                        self.data[name].append((current_time, val))
                elif line.startswith('b'):
                    parts = line.split()
                    val = parts[0][1:]
                    symbol = parts[1]
                    if symbol in self.signals:
                        name = self.signals[symbol]
                        self.data[name].append((current_time, val))
                        
    def get_signal_data(self, signal_name):
        return self.data.get(signal_name, [])

class WaveformGroup(VGroup):
    def __init__(self, vcd_filepath, signals_to_plot=None, width=10, height_per_signal=0.75, v_buff=0.5, colors=None, **kwargs):
        super().__init__(**kwargs)
        parser = VCDParser(vcd_filepath)
        max_time = parser.max_time
        
        if signals_to_plot is None:
            signals_to_plot = list(parser.data.keys())
            
        if colors is None:
            colors = [YELLOW, GREEN, RED, BLUE, ORANGE, PURPLE]
            
        self.waveforms = []
        for i, sig in enumerate(signals_to_plot):
            data = parser.get_signal_data(sig)
            color = colors[i % len(colors)]
            wf = Waveform(sig, data, max_time=max_time, width=width, height=height_per_signal, color=color)
            self.waveforms.append(wf)
            self.add(wf)
            
        self.arrange(DOWN, buff=v_buff, aligned_edge=LEFT)
        
    def create(self):
        animations = []
        for wf in self.waveforms:
            animations.append(AnimationGroup(*wf.create(), lag_ratio=0.1))
        return AnimationGroup(*animations, lag_ratio=0.2)
