from manim import *


class Gate(Group):
    def __init__(self, label=""):
        super().__init__()
        self.label = label
        self.text = Text(label).shift(DOWN * 2)

    # Method to glue a component to the gate
    def glue(self, component):
        # Add the component to the group so it stays with the gate
        self.add(component)

class AndGate(Gate):
    def __init__(self, label=""):
        super().__init__(label)
        # define the components of the AND gate
        self.and_uphor = Line(start=[0, 1, 0], end=[-1, 1, 0])
        self.and_lowhor = Line(start=[0, -1, 0], end=[-1, -1, 0])
        self.and_ver = Line(start=[-1, 1, 0], end=[-1, -1, 0])
        self.and_arc = Arc(radius=1.0, start_angle=-PI / 2, angle=PI)

        # define the wire attachment points
        self.input_point_a = [-1, 0.7, 0]  # left upper input
        self.input_point_b = [-1, -0.7, 0] # left lower input
        self.output_point = [1, 0, 0]      # right output

        # add all components to the group
        self.add(self.and_uphor, self.and_lowhor, self.and_ver, self.and_arc, self.text)

    # getters for the wire attachment points
    def get_input_point_a(self):
        return self.input_point_a

    def get_input_point_b(self):
        return self.input_point_b

    def get_output_point(self):
        return self.output_point

    # getter for animating Create() on the AND gate
    def get_create_animations(self):
        return [
            Create(self.and_uphor),
            Write(self.text),
            Create(self.and_arc),
            Create(self.and_lowhor),
            Create(self.and_ver)
        ]
    
class OrGate(Gate):
    def __init__(self, label=""):
        super().__init__(label)
        self.or_uparc = ArcBetweenPoints(start=[-1, -1, 0], end=[1, 0, 0], angle=PI / 4)
        self.or_lowarc = ArcBetweenPoints(start=[-1, 1, 0], end=[1, 0, 0], angle=-PI / 4)
        self.or_leftarc = ArcBetweenPoints(start=[-1, 1, 0], end=[-1, -1, 0], angle=-PI / 3)

        # define the wire attachment points
        self.input_point_a = [-0.88, 0.7, 0]  # left upper input
        self.input_point_b = [-0.88, -0.7, 0] # left lower input
        self.output_point = [1, 0, 0]         # right output

        # add all components to the group
        self.add(self.or_uparc, self.or_lowarc, self.or_leftarc, self.text)

    # getters for the wire attachment points
    def get_input_point_a(self):
        return self.input_point_a

    def get_input_point_b(self):
        return self.input_point_b

    def get_output_point(self):
        return self.output_point

    # getter for animating Create() on the OR gate
    def get_create_animations(self):
        return [
            Create(self.or_uparc),
            Write(self.text),
            Create(self.or_lowarc),
            Create(self.or_leftarc)
        ]