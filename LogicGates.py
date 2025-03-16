from manim import *

AND_GATE_PROPAGATION_DELAY = 0.1
OR_GATE_PROPAGATION_DELAY = 0.1
EPSILON = 0.00001

# Wire: Line, but with end defaulting to be relative to start
class Wire(Line):
    def __init__(self, start, end, abs_end=False, allow_diagonal=False, allow_any_angle=False):
        # default to relative end point
        end_point = [sum(x) for x in zip(start, end)]
        if abs_end:
            actual_start = [end[i] + start[i] for i in range(len(end))]
            end_point = end
            start = actual_start

        # restrict to horizontal, vertical, or 45-degree increments
        dx = end_point[0] - start[0]
        dy = end_point[1] - start[1]

        if not allow_diagonal and not allow_any_angle:
            if dx > EPSILON and dy > EPSILON:
                raise ValueError(f"""Wire can only be horizontal or vertical unless allow_diagonal or allow_any_angle is True.
                Currently, dx = {dx}, dy = {dy}, with points {start} and {end_point}.""")
        elif (abs(dx) != abs(dy)) and (dx != 0) and (dy != 0) and not allow_any_angle:
            raise ValueError(f"""Wire must be horizontal, vertical, or at 45-degree increments, unless allow_any_angle is True.
            Currently, dx = {dx}, dy = {dy}, with points {start} and {end_point}.""")

        super().__init__(start=start, end=end_point)
        self.state = 0  # logical low and high
        self.abs_start = start
        self.abs_end = end_point
        self.connected_gate_input = None  # gate this wire is an input to
        self.connected_gate_output = None  # gate this wire is an output from

    def set_state(self, state):
        self.state = state
        self.update_color()

    def update_color(self):
        self.set_color(RED if self.state else WHITE)

    def connect_to_gate_input(self, gate):
        self.connected_gate_input = gate

    def connect_to_gate_output(self, gate):
        self.connected_gate_output = gate

# Net: Group of Wire objects that share a common state
class Net(Group):
    def __init__(self):
        super().__init__()
        self.wires = []

    def add_wire(self, wire):
        if not isinstance(wire, Wire):
            raise ValueError("Only Wire objects can be added to a Net.")
        self.wires.append(wire)
        self.add(wire)

    def create(self):
        return [Create(wire) for wire in self.wires]

    def propagate(self, input_wire):
        # propagate the state from the input_wire to all wires in the Net
        if input_wire not in self.wires:
            raise ValueError("The selected input wire is not part of this Net.")
        for wire in self.wires:
            wire.set_state(input_wire.state)

    def propagate_through(self, input_wire):
        # propagate the state through the Net and cascade to connected Gates
        self.propagate(input_wire)
        for wire in self.wires:
            # cascade propagation through gates if connected
            if wire.connected_gate_input:
                print(f"Propagating wire {wire.abs_start}, {wire.abs_end}, through {wire.connected_gate_input}")
                wire.connected_gate_input.propagate_through()

    def uncreate(self):
        return [Uncreate(wire) for wire in self.wires]


# Gate: abstract logic gate
class Gate(Group):
    def __init__(self, label=""):
        super().__init__()
        self.label = label
        self.text = Text(label).shift(DOWN * 2)
        self.input_wires = []  # list to track input wires
        self.output_wire = None  # single output wire

    # method to glue a component to the gate
    def glue(self, component):
        self.add(component)

    # method to attach an input wire
    def add_input_wire(self, wire):
        self.input_wires.append(wire)
        self.add(wire)
        wire.connect_to_gate_input(self)

    # method to attach the output wire
    def add_output_wire(self, wire):
        self.output_wire = wire
        self.add(wire)
        wire.connect_to_gate_output(self)

    # method to collects Create animations for all wires that have been attached
    def get_glued_create_animations(self):
        animations = []
        for wire in self.input_wires:
            animations.append(Create(wire))
        if self.output_wire:
            animations.append(Create(self.output_wire))
        return animations

    # method to uncreate all components of the gate (including glued components)
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
                pass  # skip components that don't support these animations
        return animations
    
    def propagate(self):
        pass

    def propagate_through(self):
        self.propagate()  # first, propagate within the gate
        if self.output_wire:
            # if the output wire is connected to another Net, propagate further
            if hasattr(self.output_wire, "connected_net"):
                self.output_wire.connected_net.propagate_through()

# AndGate: a group of components that represent an AND gate
#          (inherits from Gate)
class AndGate(Gate):
    def __init__(self, label=""):
        super().__init__(label)
        # define the components of the AND gate
        self.and_uphor = Line(start=[0, 1, 0], end=[-1, 1, 0])
        self.and_lowhor = Line(start=[0, -1, 0], end=[-1, -1, 0])
        self.and_ver = Line(start=[-1, 1, 0], end=[-1, -1, 0])
        self.and_arc = Arc(radius=1.0, start_angle=-PI / 2, angle=PI)

        # define the wire attachment points
        self.input_a = [-1, 0.7, 0]  # left upper input
        self.input_b = [-1, -0.7, 0] # left lower input
        self.output = [1, 0, 0]      # right output

        # add all components to the group
        self.add(self.and_uphor, self.and_lowhor, self.and_ver, self.and_arc, self.text)

    # getters for the wire attachment points
    def get_input_a(self):
        return self.input_a

    def get_input_b(self):
        return self.input_b

    def get_output(self):
        return self.output
    
    # override shift method to shift wire attachment points
    def shift(self, *vectors):
        super().shift(*vectors)
        self.input_a = [sum(x) for x in zip(self.input_a, vectors[0])]
        self.input_b = [sum(x) for x in zip(self.input_b, vectors[0])]
        self.output = [sum(x) for x in zip(self.output, vectors[0])]
        return self

    # getter for animating Create() on the AND gate
    def create(self):
        return [
            Create(self.and_uphor),
            Write(self.text),
            Create(self.and_arc),
            Create(self.and_lowhor),
            Create(self.and_ver)
        ] + self.get_glued_create_animations()
    
    def propagate(self):
        if self.input_wires and self.output_wire:
            result = all(wire.state for wire in self.input_wires)
            self.output_wire.set_state(int(result))

# OrGate: a group of components that represent an OR gate
#         (inherits from Gate)
class OrGate(Gate):
    def __init__(self, label=""):
        super().__init__(label)
        self.or_uparc = ArcBetweenPoints(start=[-1, -1, 0], end=[1, 0, 0], angle=PI / 4)
        self.or_lowarc = ArcBetweenPoints(start=[-1, 1, 0], end=[1, 0, 0], angle=-PI / 4)
        self.or_leftarc = ArcBetweenPoints(start=[-1, 1, 0], end=[-1, -1, 0], angle=-PI / 3)

        # define the wire attachment points
        self.input_a = [-0.88, 0.7, 0]  # left upper input
        self.input_b = [-0.88, -0.7, 0] # left lower input
        self.output = [1, 0, 0]         # right output

        # add all components to the group
        self.add(self.or_uparc, self.or_lowarc, self.or_leftarc, self.text)
    
    # override shift method to shift wire attachment points
    def shift(self, *vectors):
        super().shift(*vectors)
        self.input_a = [sum(x) for x in zip(self.input_a, vectors[0])]
        self.input_b = [sum(x) for x in zip(self.input_b, vectors[0])]
        self.output = [sum(x) for x in zip(self.output, vectors[0])]
        return self

    # getters for the wire attachment points
    def get_input_a(self):
        return self.input_a

    def get_input_b(self):
        return self.input_b

    def get_output(self):
        return self.output

    # getter for animating Create() on the OR gate
    def create(self):
        return [
            Create(self.or_uparc),
            Write(self.text),
            Create(self.or_lowarc),
            Create(self.or_leftarc)
        ] + self.get_glued_create_animations()
    
    def propagate(self):
        if self.input_wires and self.output_wire:
            result = any(wire.state for wire in self.input_wires)
            self.output_wire.set_state(int(result))

# TODO: make group of wires class: Net, add methods to set state of all wires. add atrributes to Wires to track begin and end points
# TODO: add more gates (e.g. XOR, NAND, NOR, etc.)
# TODO: add flip-flops, registers, etc.
# TODO: make gates customizable (e.g. NOT bubbles, flipped, etc.)
# TODO: logic propagation