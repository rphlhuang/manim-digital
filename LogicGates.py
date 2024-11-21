from manim import *

AND_GATE_PROPAGATION_DELAY = 0.1
OR_GATE_PROPAGATION_DELAY = 0.1

# Wire: Line, but with end defaulting to be relative to start
class Wire(Line):
    def __init__(self, start, end, abs_end=False, allow_diagonal=False, allow_any_angle=False):
       
        # default to relative end point
        end_point = [sum(x) for x in zip(start, end)]
        # use absolute end point if specified
        if abs_end:
            end_point = end

        # restrict to horizontal, vertical, or 45-degree increments
        dx = end_point[0] - start[0]
        dy = end_point[1] - start[1]

        if not allow_diagonal and not allow_any_angle:
            if dx != 0 and dy != 0:
                raise ValueError("Wire can only be horizontal or vertical unless allow_diagonal or allow_any_angle is True. Got start = {}, end = {}, dx = {}, dy = {}".format(start, end_point, dx, dy))
        elif (abs(dx) != abs(dy)) and (dx != 0) and (dy != 0) and not allow_any_angle:
            raise ValueError("Wire must be horizontal, vertical, or at 45-degree increments, unless allow_any_angle is True. Got start = {}, end = {}, dx = {}, dy = {}".format(start, end_point, dx, dy))

        super().__init__(start=start, end=end_point)
        self.state = 0  # logical low and high
        self.abs_start = start
        self.abs_end = end_point
        self.update_color()

    def set_state(self, state):
        self.state = state
        self.update_color()

    def update_color(self):
        self.set_color(RED if self.state else WHITE)

    def propagate(self):
        # propagate state to connected wires
        if hasattr(self, "connected_wires"):
            print("    connected_wires:", self.connected_wires)
            for wire in self.connected_wires:
                wire.set_state(self.state)
                wire.update_color()

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
        wire.connected_wires = self.get_connected_wires(wire)

        self.update_all_connections()

    def update_all_connections(self):
        # Update the connected_wires attribute for all wires
        for wire in self.wires:
            wire.connected_wires = self.get_connected_wires(wire)

    def get_connected_wires(self, wire):
        # find wires that share start or end points
        connected = []
        for other_wire in self.wires:
            print(f"    Checking {wire} against {other_wire}")
            if wire == other_wire:
                continue
            if (wire.abs_start == other_wire.abs_start or
                wire.abs_start == other_wire.abs_end or
                wire.abs_end == other_wire.abs_start or
                wire.abs_end == other_wire.abs_end):
                connected.append(other_wire)
        return connected
    
    def create(self):
        return [Create(wire) for wire in self.wires]

    def propagate(self):
        # propagate state across the entire net
        for wire in self.wires:
            print(f"Propagating state {wire.state} across wire {wire}")
            wire.propagate()

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

    # method to attach the output wire
    def add_output_wire(self, wire):
        self.output_wire = wire
        self.add(wire)

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

    # getter for animating Create() on the AND gate
    def create(self):
        return [
            Create(self.and_uphor),
            Write(self.text),
            Create(self.and_arc),
            Create(self.and_lowhor),
            Create(self.and_ver)
        ]
    
    def propagate(self, scene):
        scene.wait(AND_GATE_PROPAGATION_DELAY)
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
        ]
    
    def propagate(self, scene):
        scene.wait(OR_GATE_PROPAGATION_DELAY)
        if self.input_wires and self.output_wire:
            result = any(wire.state for wire in self.input_wires)
            self.output_wire.set_state(int(result))

# TODO: make group of wires class: Net, add methods to set state of all wires. add atrributes to Wires to track begin and end points
# TODO: add more gates (e.g. XOR, NAND, NOR, etc.)
# TODO: add flip-flops, registers, etc.
# TODO: make gates customizable (e.g. NOT bubbles, flipped, etc.)
# TODO: logic propagation