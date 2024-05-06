from diagrams import Node


class StartEnd(Node):
    def __init__(self, label: str = ""):

        attrs = {"shape": "ellipse", "style": "filled",
                 "fixedsize": "false", "fillcolor": "lightskyblue",
                 "fontcolor": "black", "labelloc": "c",
                 "fontname": "MS UI Gothic", "color": "darkgray"}
        super().__init__(label=label, nodeid=None, **attrs)


class Action(Node):
    def __init__(self, label: str = ""):

        attrs = {"shape": "box", "style": "filled",
                 "fixedsize": "false", "fillcolor": "lightskyblue",
                 "fontcolor": "black", "labelloc": "c",
                 "fontname": "MS UI Gothic", "color": "darkgray"}
        super().__init__(label=label, nodeid=None, **attrs)


class Decision(Node):
    def __init__(self, label: str = ""):

        attrs = {"shape": "diamond", "style": "filled",
                 "fixedsize": "false", "fillcolor": "lightskyblue",
                 "fontcolor": "black", "labelloc": "c",
                 "fontname": "MS UI Gothic", "color": "darkgray"}
        super().__init__(label=label, nodeid=None, **attrs)


class InLoop(Node):
    def __init__(self, loop_id: str, label: str = ""):

        attrs = {"shape": "trapezium", "style": "filled",
                 "fixedsize": "false", "fillcolor": "lightskyblue",
                 "fontcolor": "black", "labelloc": "c",
                 "fontname": "MS UI Gothic", "xlabel": f"loopid={loop_id}",
                 "color": "darkgray"}
        super().__init__(label=label, nodeid=None, **attrs)


class OutLoop(Node):
    def __init__(self, loop_id: str, label: str = ""):

        attrs = {"shape": "invtrapezium", "style": "filled",
                 "fixedsize": "false", "fillcolor": "lightskyblue",
                 "fontcolor": "black", "labelloc": "c",
                 "fontname": "MS UI Gothic", "height": "0.75",
                 "xlabel": f"loopid={loop_id}",
                 "color": "darkgray"}
        super().__init__(label="out-loop", nodeid=None, **attrs)


class ExitLoop(Node):
    def __init__(self, loop_id: str, label: str = ""):

        attrs = {"shape": "ellipse", "style": "filled",
                 "fixedsize": "false", "fillcolor": "lightskyblue",
                 "fontcolor": "black", "labelloc": "c",
                 "xlabel": f"loopid={loop_id}",
                 "fontname": "MS UI Gothic", "color": "darkgray"}
        super().__init__(label="exit-loop", nodeid=None, **attrs)
