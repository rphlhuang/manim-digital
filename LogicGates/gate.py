from manim import *

class Gate(Group):
    def __init__(self, label=""):
        super().__init__()
        self.label = label
        self.text = Text(label).shift(DOWN * 2)
        self.input_wires = []  # list to track input wires
        self.output_wire = None  # single output wire

    def glue(self, component):
        self.add(component)

    def add_input_wire(self, wire):
        self.input_wires.append(wire)
        self.add(wire)
        wire.connect_to_gate_input(self)

    def add_output_wire(self, wire):
        self.output_wire = wire
        self.add(wire)
        wire.connect_to_gate_output(self)

    def uncreate(self):
        animations = []
        for component in self.submobjects:
            try:
                if isinstance(component, Text):
                    animations.append(Unwrite(component))
                else:
                    animations.append(Uncreate(component))
            except AttributeError:
                print(f"Warning: {component} cannot be uncreated or unwritten.")
        return animations

    def get_glued_create_animations(self):
        animations = [Create(wire) for wire in self.input_wires]
        if self.output_wire:
            animations.append(Create(self.output_wire))
        return animations

    def propagate(self):
        pass

    def propagate_through(self):
        self.propagate()
