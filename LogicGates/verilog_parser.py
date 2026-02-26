import re
from manim import *
from .and_gate import AndGate
from .or_gate import OrGate
from .not_gate import NotGate
from .wire_net import Wire, Net
from .dff import DFlipFlop

class VerilogParser:
    """
    A lightweight SystemVerilog structural parser that converts code into a Manim logic circuit diagram.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.inputs = []
        self.outputs = []
        self.wires = []
        self.instances = [] # list of dicts: {'type': 'and', 'name': 'g1', 'ports': ['out', 'in1', 'in2']}
        
        self.gates = {}     # name -> Gate object
        self.manim_wires = []
        self.manim_nets = {} # name -> Net object
        self.input_dots = {}
        self.output_dots = {}
        self.input_labels = {}
        self.output_labels = {}
        
        self.circuit_group = Group()
        self._parse()

    def _parse(self):
        with open(self.filepath, 'r') as f:
            content = f.read()

        # Remove comments
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Extract inputs, outputs, wires
        self.inputs = re.findall(r'\binput\s+(?:wire\s+)?(?:logic\s+)?([a-zA-Z0-9_\s,]+);', content)
        self.inputs = [i.strip() for match in self.inputs for i in match.split(',')]
        
        self.outputs = re.findall(r'\boutput\s+(?:wire\s+)?(?:logic\s+)?([a-zA-Z0-9_\s,]+);', content)
        self.outputs = [i.strip() for match in self.outputs for i in match.split(',')]

        self.wires = re.findall(r'\bwire\s+(?:logic\s+)?([a-zA-Z0-9_\s,]+);', content)
        self.wires = [i.strip() for match in self.wires for i in match.split(',')]

        # Find primitive instantiations
        # e.g., and g1(out, a, b);
        # or sr_latch inst_name (.Q(out), .S(in1), .R(in2)); - we'll handle implicit mapping for primitives
        primitives = ['and', 'nand', 'or', 'nor', 'xor', 'xnor', 'not']
        
        for p in primitives:
            # Matches: and [name] (port1, port2, ...);
            pattern = rf'\b{p}\s+([a-zA-Z0-9_]+)\s*\((.*?)\)\s*;'
            matches = re.findall(pattern, content)
            for m in matches:
                inst_name = m[0]
                ports = [port.strip() for port in m[1].split(',')]
                self.instances.append({
                    'type': p,
                    'name': inst_name,
                    'ports': ports # for standard primitives, ports[0] is output, rest are inputs
                })

        # Find custom instances like dff or sr_latch
        # e.g. dff d1 (.q(Q), .d(D), .clk(CLK));
        custom_inst_pattern = r'\b([a-zA-Z0-9_]+)\s+([a-zA-Z0-9_]+)\s*\((.*?)\)\s*;'
        for m in re.findall(custom_inst_pattern, content):
            mod_type, inst_name, ports_str = m[0], m[1], m[2]
            if mod_type in primitives or mod_type in ['module']:
                continue
                
            ports = []
            if '.' in ports_str:
                # Named mapping: .q(Q), .d(D)
                port_matches = re.findall(r'\.\s*([a-zA-Z0-9_]+)\s*\(\s*([a-zA-Z0-9_]+)\s*\)', ports_str)
                ports_dict = {pm[0]: pm[1] for pm in port_matches}
                self.instances.append({
                    'type': mod_type,
                    'name': inst_name,
                    'ports_dict': ports_dict
                })
            else:
                ports = [p.strip() for p in ports_str.split(',')]
                self.instances.append({
                    'type': mod_type,
                    'name': inst_name,
                    'ports': ports
                })

    def generate_gates(self):
        """
        Creates the Gate instances and returns them, but does NOT position them
        or connect them with wires. The user can manually place them and then 
        call route_wires().
        """
        for inst in self.instances:
            t = inst['type']
            name = inst['name']
            if t == 'and':
                self.gates[name] = AndGate(label=name.upper())
            elif t == 'or':
                self.gates[name] = OrGate(label=name.upper())
            elif t == 'not':
                self.gates[name] = NotGate(label=name.upper())
            elif t.lower() == 'dff':
                self.gates[name] = DFlipFlop(label=name.upper())
            else:
                print(f"Warning: Unsupported primitive or module {t}")
        return self.gates

    def auto_layout(self):
        """
        Original method that does everything: generates, places automatically, 
        and routes.
        """
        self.generate_gates()

        # 2. Determine layers (topological sort)
        layers = {inp: 0 for inp in self.inputs}
        
        # simple iteration to assign layers to gates
        changed = True
        gate_layers = {inst['name']: 1 for inst in self.instances}
        
        iterations = 0
        max_iterations = len(self.instances) * 2
        
        while changed and iterations < max_iterations:
            changed = False
            iterations += 1
            for inst in self.instances:
                name = inst['name']
                t = inst['type']
                
                # identify inputs to this gate
                inputs_to_gate = []
                if 'ports_dict' in inst:
                    for k, v in inst['ports_dict'].items():
                        if k in ['d', 'clk', 's', 'r'] or k.startswith('in'):
                            inputs_to_gate.append(v)
                else:
                    if t in ['and', 'or', 'not', 'nand', 'nor', 'xor', 'xnor']:
                        inputs_to_gate = inst['ports'][1:]
                    
                max_in_layer = 0
                for signal in inputs_to_gate:
                    if signal in layers:
                        max_in_layer = max(max_in_layer, layers[signal])
                    else:
                        # find gate that drives this signal
                        for other_inst in self.instances:
                            if 'ports_dict' in other_inst:
                                for k, v in other_inst['ports_dict'].items():
                                    if v == signal and (k in ['q', 'qbar'] or k.startswith('out')):
                                        max_in_layer = max(max_in_layer, gate_layers[other_inst['name']])
                            elif other_inst['ports'][0] == signal: # output is usually index 0
                                max_in_layer = max(max_in_layer, gate_layers[other_inst['name']])
                                
                if gate_layers[name] != max_in_layer + 1:
                    gate_layers[name] = max_in_layer + 1
                    changed = True

        # Compute signal layers
        for inst in self.instances:
            name = inst['name']
            t = inst['type']
            if 'ports_dict' in inst:
                for k, v in inst['ports_dict'].items():
                    if k in ['q', 'qbar'] or k.startswith('out'):
                        layers[v] = gate_layers[name]
            elif t in ['and', 'or', 'not', 'nand', 'nor', 'xor', 'xnor']:
                out_signal = inst['ports'][0]
                layers[out_signal] = gate_layers[name]

        # 3. Position items
        max_layer = max(gate_layers.values()) if gate_layers else 0
        
        # Position inputs at x = -4
        for i, inp in enumerate(self.inputs):
            dot = Dot(LEFT * 4 + UP * (len(self.inputs)/2 - i) * 1.5)
            lbl = Text(inp, font_size=24, font="sans-serif").next_to(dot, LEFT)
            self.input_dots[inp] = dot
            self.input_labels[inp] = lbl
            
        # Position outputs at x = 4
        for i, outp in enumerate(self.outputs):
            dot = Dot(RIGHT * 4 + UP * (len(self.outputs)/2 - i) * 1.5)
            lbl = Text(outp, font_size=24, font="sans-serif").next_to(dot, RIGHT)
            self.output_dots[outp] = dot
            self.output_labels[outp] = lbl
            
        # Position gates
        if max_layer > 0:
            x_step = 6.0 / max_layer
            layer_counts = {}
            for name, l in gate_layers.items():
                layer_counts[l] = layer_counts.get(l, 0) + 1
                
            layer_indices = {}
            for name, l in gate_layers.items():
                idx = layer_indices.get(l, 0)
                layer_indices[l] = idx + 1
                
                x = -3 + l * x_step
                y = (layer_counts[l] / 2 - idx) * 2.5
                
                if name in self.gates:
                    self.gates[name].move_to(RIGHT * x + UP * y)
                    
        return self.route_wires()
        
    def route_wires(self):
        """
        Takes the currently placed gates and routes wires between them.
        Returns the finalized circuit_group.
        """
        # We need a routing mechanism, but for Manim we just use Wire with abs_end=True
        # Or simple multi-segment lines. We will just use diagonal wires for simplicity, allow_any_angle=True.
        
        # To make it slightly better logic propagation, we need endpoints.
        signal_sources = {} # signal -> coordinate or Gate output method
        
        for inp in self.inputs:
            signal_sources[inp] = self.input_dots[inp].get_center()
            self.manim_nets[inp] = Net()
            
        for inst in self.instances:
            name = inst['name']
            if name not in self.gates: continue
            g = self.gates[name]
            
            if inst['type'] in ['and', 'or', 'not']:
                out_sig = inst['ports'][0]
                signal_sources[out_sig] = g.get_output()
                if out_sig not in self.manim_nets:
                    self.manim_nets[out_sig] = Net()
                    
            elif inst['type'].lower() == 'dff':
                if 'ports_dict' in inst:
                    out_sig = inst['ports_dict'].get('q', None)
                    if out_sig:
                        signal_sources[out_sig] = g.get_output_q()
                        if out_sig not in self.manim_nets:
                            self.manim_nets[out_sig] = Net()
                            
        # Now connect to inputs and outputs
        for inst in self.instances:
            name = inst['name']
            if name not in self.gates: continue
            g = self.gates[name]
            
            if inst['type'] in ['and', 'or', 'not']:
                inputs = inst['ports'][1:]
                for i, inp_sig in enumerate(inputs):
                    if inp_sig in signal_sources:
                        # determine proper input pin
                        if inst['type'] == 'not':
                            in_port = g.get_input()
                        else:
                            in_port = g.get_input_a() if i==0 else g.get_input_b()
                        
                        w = Wire(start=signal_sources[inp_sig], end=in_port, abs_end=True, allow_any_angle=True)
                        g.add_input_wire(w)
                        self.manim_wires.append(w)
                        if inp_sig in self.manim_nets:
                            self.manim_nets[inp_sig].add_wire(w)
                            
            elif inst['type'].lower() == 'dff':
                if 'ports_dict' in inst:
                    d_sig = inst['ports_dict'].get('d', None)
                    clk_sig = inst['ports_dict'].get('clk', None)
                    
                    if d_sig and d_sig in signal_sources:
                        w = Wire(start=signal_sources[d_sig], end=g.get_input_d(), abs_end=True, allow_diagonal=True)
                        g.add_input_wire_d(w)
                        self.manim_wires.append(w)
                        if d_sig in self.manim_nets:
                            self.manim_nets[d_sig].add_wire(w)
                            
                    if clk_sig and clk_sig in signal_sources:
                        w = Wire(start=signal_sources[clk_sig], end=g.get_input_clk(), abs_end=True, allow_diagonal=True)
                        g.add_input_wire_clk(w)
                        self.manim_wires.append(w)
                        if clk_sig in self.manim_nets:
                            self.manim_nets[clk_sig].add_wire(w)
                            
        # Connect to final outputs
        for outp in self.outputs:
            if outp in signal_sources:
                w = Wire(start=signal_sources[outp], end=self.output_dots[outp].get_center(), abs_end=True, allow_diagonal=True)
                self.manim_wires.append(w)
                if outp in self.manim_nets:
                    self.manim_nets[outp].add_wire(w)
                    
        # Group everything
        for g in self.gates.values():
            self.circuit_group.add(g)
        for w in self.manim_wires:
            self.circuit_group.add(w)
        for d in self.input_dots.values():
            self.circuit_group.add(d)
        for l in self.input_labels.values():
            self.circuit_group.add(l)
        for d in self.output_dots.values():
            self.circuit_group.add(d)
        for l in self.output_labels.values():
            self.circuit_group.add(l)
            
        return self.circuit_group

    def create(self):
        anims = []
        for d in self.input_dots.values(): anims.append(Create(d))
        for l in self.input_labels.values(): anims.append(Write(l))
        for d in self.output_dots.values(): anims.append(Create(d))
        for l in self.output_labels.values(): anims.append(Write(l))
        
        for g in self.gates.values():
            anims.extend(g.create())
            
        # some wires are not attached to gate outputs automatically when drawing, wait actually they often are added via add_input_wire which makes gate.create() animate them.
        # But wires going purely to output_dots need explicit creation.
        
        # Actually, it's safer to just return a single AnimationGroup that creates the circuit_group
        # if the custom gate structures allow it. But Gate.create() handles glued wires.
        
        return anims

    def set_input(self, input_name, state):
        if input_name in self.manim_nets:
            for w in self.manim_nets[input_name].wires:
                w.set_state(state)
            # Propagate through the network
            for w in self.manim_nets[input_name].wires:
                if hasattr(w, 'propagate_through'):
                    pass # manim_digital wires need manual propagation or Net.propagate_through
            self.manim_nets[input_name].propagate_through(self.manim_nets[input_name].wires[0] if self.manim_nets[input_name].wires else None)

    def generate_manim_code(self, output_path=None):
        """
        Creates a string containing Manim code that perfectly reconstructs
        the currently routed circuit.
        """
        code = []
        code.append("# --- Auto-Generated Manim Circuit ---")
        code.append("from manim import *")
        code.append("from LogicGates import AndGate, OrGate, NotGate, DFlipFlop, Wire, Net")
        code.append("")
        code.append("class AutoCircuitScene(Scene):")
        code.append("    def construct(self):")
        code.append("        gates = {}")
        code.append("        wires = []")
        code.append("        nets = {}")
        code.append("        circuit = Group()")
        code.append("")
        
        # Gates
        code.append("        # Instantiating Gates")
        for name, g in self.gates.items():
            gate_class = g.__class__.__name__
            code.append(f"        gates['{name}'] = {gate_class}(label='{g.label.text}')")
            center = g.get_center()
            code.append(f"        gates['{name}'].move_to([{center[0]:.2f}, {center[1]:.2f}, 0])")
            code.append(f"        circuit.add(gates['{name}'])")
            code.append("")
            
        # Wires
        code.append("        # Wires and Routing")
        for i, w in enumerate(self.manim_wires):
            start = w.get_start()
            end = w.get_end()
            code.append(f"        w_{i} = Wire(start=[{start[0]:.2f}, {start[1]:.2f}, 0], end=[{end[0]:.2f}, {end[1]:.2f}, 0], abs_end=True, allow_any_angle=True)")
            code.append(f"        wires.append(w_{i})")
            code.append(f"        circuit.add(w_{i})")
            
        code.append("")
        code.append("        # Draw circuit")
        code.append("        self.play(Create(circuit))")
        code.append("        self.wait(1)")
        
        result = "\n".join(code)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(result)
                
        return result
