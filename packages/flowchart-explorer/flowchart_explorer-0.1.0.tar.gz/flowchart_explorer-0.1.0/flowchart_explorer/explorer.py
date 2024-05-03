import copy
from typing import Tuple
from collections import deque
import sys

from flowchart_explorer.methods import get_logger

logger = get_logger(__name__)
class LoopQues:

    def __init__(self):
        self.loop_que = deque()
        self.max_loop_que = deque()
        self.current_loop_num = deque()

    def put_init(self, loop_id: int, max_loop_num: int = 2):
        self.loop_que.append(loop_id)
        self.max_loop_que.append(max_loop_num)
        self.current_loop_num.append(1)

    def read_loop_que(self) -> int:
        item = self.loop_que.pop()
        self.loop_que.append(item)
        return item

    def read_max_loop_num(self) -> int:
        item = self.max_loop_que.pop()
        self.max_loop_que.append(item)
        return item

    def read_current_loop_num(self) -> int:
        item = self.current_loop_num.pop()
        self.current_loop_num.append(item)
        return item

    def count_up_current_loop_num(self):
        num = self.current_loop_num.pop()
        num += 1
        self.current_loop_num.append(num)

    def check_in_loop(self, loop_id: str) -> bool:
        return loop_id in self.loop_que

    def exit_loop(self) -> Tuple[int, int, int]:
        return self.loop_que.pop(), self.max_loop_que.pop(), self.current_loop_num.pop()


class Explorer(object):

    def __init__(self, max_recursion: int = 1000):
        self._max_recursion = max_recursion
        sys.setrecursionlimit(self._max_recursion)

    def run(self, graph: dict) -> Tuple[int, dict[int, list]]:
        # get start_node & start_edge
        start_node_id = graph['start_node']['id']
        key = 1
        path = [start_node_id]
        log: dict = {}
        loop_que = LoopQues()
        key, log = self.explorer(source_id=start_node_id,
                                 key=key,
                                 graph=graph,
                                 path=path,
                                 log=log,
                                 loop_que=loop_que)
        return key, log

    def explorer(self, source_id: str, key: int, graph: dict,
                 path: list, log: dict, loop_que: LoopQues):
        logger.debug(f"1. {source_id}")
        source_key = f"{source_id}-"
        # get ['2-4-13', '2-10-9']
        from_source_edges: list[str] = [key for key in graph["edges"].keys()
                                        if key.startswith(source_key)]
        # get ['13', '9']
        target_nodes = [edge_key.split('-', 2)[-1] for edge_key in from_source_edges]
        if graph['nodes'][source_id]['node-type'] == 'in-loop':
            # If not in loop, initialize loop_que
            if not loop_que.check_in_loop(graph['nodes'][source_id]['loop-id']):
                logger.debug("intial-in-loop")
                if 'max-loop' in graph['nodes'][source_id]:
                    max_loop = graph['nodes'][source_id]['max-loop']
                else:
                    max_loop = 2
                loop_que.put_init(graph['nodes'][source_id]['loop-id'], max_loop)

        elif graph['nodes'][source_id]['node-type'] == 'out-loop':
            max_loop_num = loop_que.read_max_loop_num()
            current_loop_num = loop_que.read_current_loop_num()

            if current_loop_num < max_loop_num:
                loop_que.count_up_current_loop_num()
                logger.debug(f"1.2. {source_id}, current_loop_num:{loop_que.read_current_loop_num()}")

                # add to the path the in-loop id according to this out-loop
                return_loop_id = graph['loops'][f"{loop_que.read_loop_que()}"]['in-loop']
                logger.debug(f"2. {source_id}")
                target_nodes = [return_loop_id]
            # pop que for exit multi loop
            else:
                loop_que.exit_loop()

        elif graph['nodes'][source_id]['node-type'] == 'exit-loop':
            loop_que.exit_loop()

        if not target_nodes:
            log[key] = path
            key += 1
            logger.debug(f"3. {source_id} record log:{path}")
            return key, log

        # key, log = self._target_nodes_loop(target_nodes, key, graph, path, log, loop_que)
        if source_id == "38" or source_id == "36":
            logger.debug(f"source:{source_id}, target:{target_nodes}")

        for target_node in target_nodes:
            next_path = copy.deepcopy(path)
            next_path.append(target_node)
            # Preserve the current state of the queue to restore its contents
            # when returning from recursion.
            reset_loop_que = copy.deepcopy(loop_que)
            key, log = self.explorer(source_id=target_node,
                                     key=key,
                                     graph=graph,
                                     path=next_path,
                                     log=log,
                                     loop_que=loop_que)
            loop_que = reset_loop_que
            if len(loop_que.current_loop_num) == 0:
                logger.debug(f"4. {source_id}")
            else:
                logger.debug(f"4. source: {source_id}, loop_que:{loop_que.read_loop_que()}, current: {loop_que.read_current_loop_num()}")

        logger.debug(f"5. {source_id}")

        return key, log
