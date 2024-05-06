import os
from pathlib import Path
import shutil
from flowchart_explorer.methods import get_logger

from diagrams import Diagram, Edge
from flowchart_explorer.flowchartdiagrams.nodes import (
    StartEnd, InLoop, OutLoop, ExitLoop, Action, Decision)

logger = get_logger(__name__)


class FlowChartPath:

    def __init__(self, name: str = "FlowChart", dir_path: Path = Path("./"), out_format: str = "png"):
        self.name = name
        self.dir_path = dir_path
        self.out_format = out_format

    def draw(self, flow_path: dict[int, list[str]], graph: dict):
        graph_attr = {
            "fontsize": "24",
            "labelloc": "t",
            "bgcolor": "ghostwhite"

        }

        for key in flow_path:
            with Diagram(f"{self.name}", show=False, outformat=self.out_format,
                         filename=f"{self.name}-{key}",
                         direction="TB", graph_attr=graph_attr):
                for i, node_id in enumerate(flow_path[key]):
                    if i == 0:
                        assert graph["start_node"]["id"] == node_id
                        pre_node = StartEnd("Start Node")
                        continue
                    else:
                        node = graph["nodes"][node_id]
                        if node["node-type"] == "in-loop":
                            next_node = InLoop(loop_id=node["loop-id"], label=node["label"])
                        elif node["node-type"] == "out-loop":
                            next_node = OutLoop(loop_id=node["loop-id"])
                        elif node["node-type"] == "exit-loop":
                            next_node = ExitLoop(loop_id=node["loop-id"])
                        elif node["node-type"] == "decision":
                            next_node = Decision(node["label"])
                        else:  # Action
                            next_node = Action(node["label"])
                    pre_node.connect(next_node, Edge(forward=True))
                    pre_node = next_node

        self._move_files(list(flow_path.keys()))

    def _move_files(self, keys: list[int]):
        os.makedirs(self.dir_path, exist_ok=True)
        for key in keys:
            shutil.move(f"{self.name}-{key}.{self.out_format}", self.dir_path)
