from pathlib import Path
import xml.etree.ElementTree as Et
from typing import Tuple


class Drawio(object):

    def __init__(self, file_path: Path):
        if file_path.is_file():
            tree = Et.parse(file_path)
            self.root = tree.getroot()
        else:
            raise FileNotFoundError("File not exits.")

        self.MAX_LOOP = 2

    def get_graph(self) -> dict:
        nodes, edges, sources, targets = self._get_nodes_and_edges()
        start_node = self._get_start_node(nodes=nodes, sources=sources, targets=targets)
        nodes, loops, loop_check = self._explorer_node_type(nodes)
        # check processes
        self._check_loops(loop_check)
        self._check_same_source_target_edges(edges)
        return {"start_node": start_node,
                "edges": edges,
                "nodes": nodes,
                "loops": loops}

    @staticmethod
    def _check_loops(loops: dict):
        """Check the couple of in-loop and out-loop"""
        for key in loops.keys():
            assert {'in-loop', 'out-loop'} == set(loops[key]), \
                "There are places where in-loop and out-loop do not form a pair."

    @staticmethod
    def _check_same_source_target_edges(edges: dict):
        source_edge_target_list = edges.keys()
        # delete edge id. '2-4-17' -> '2-17'
        source_target = ['-'.join([s.split('-')[0], s.split('-')[-1]]) for s in source_edge_target_list]
        assert len(source_target) == len(set(source_target)), \
            "There exists one or more edges where the source node and target node are the same."

    def _explorer_node_type(self, nodes: dict) -> Tuple[dict, dict, dict]:
        graph_nodes: dict = {}
        loops: dict = {}
        loop_check: dict = {}
        for key in nodes.keys():
            graph_nodes, loops, loop_check = self._transform_node(key, nodes[key], graph_nodes, loops, loop_check)
        return graph_nodes, loops, loop_check

    def _transform_node(self, key: str, node: dict, graph_nodes: dict,
                        loops: dict, loop_check: dict) -> Tuple[dict, dict, dict]:

        # get label
        if 'value' in node['additional-details']:
            label = node['additional-details']['value']
        elif 'label' in node['additional-details']:
            label = node['additional-details']['label']
        else:
            label = ""
        # replace <br> to \n
        label = label.replace("<br>", "\n")


        style = node['additional-details']['style']
        # in-loop
        if (style.startswith('shape=loopLimit;') and
                "in-loop" in node['additional-details'].keys()):

            max_loop = self.MAX_LOOP
            if "max-loop" in node['additional-details']:
                max_loop = node['additional-details']['max-loop']

            graph_nodes[key] = {'node-type': 'in-loop',
                                'loop-id': node['additional-details']['in-loop'],
                                'max-loop': max_loop,
                                'label': label,
                                'additional-details': node['additional-details']
                                }
            loop_check = self._add_value_to_list(loop_check, node['additional-details']['in-loop'], 'in-loop')
            loops = self._add_value_to_dict(loops, node['additional-details']['in-loop'], 'in-loop', key)

        # out-loop
        elif (style.startswith('shape=loopLimit;') and
              "out-loop" in node['additional-details'].keys()):
            graph_nodes[key] = {'node-type': 'out-loop',
                                'loop-id': node['additional-details']['out-loop'],
                                'label': label,
                                'additional-details': node['additional-details']
                                }
            loop_check = self._add_value_to_list(loop_check, node['additional-details']['out-loop'], 'out-loop')
            loops = self._add_value_to_dict(loops, node['additional-details']['out-loop'], 'out-loop', key)

        # exit-loop
        elif (style.startswith('ellipse;') and
              "exit-loop" in node['additional-details'].keys()):
            graph_nodes[key] = {'node-type': 'exit-loop',
                                'loop-id': node['additional-details']['exit-loop'],
                                'label': label,
                                'additional-details': node['additional-details']
                                }

        # decision
        elif style.startswith('rhombus;'):
            graph_nodes[key] = {'node-type': 'decision',
                                'label': label,
                                'additional-details': node['additional-details']
                                }
        # normal(Cases other than the above)
        else:
            graph_nodes[key] = {'node-type': 'normal',
                                'label': label,
                                'additional-details': node['additional-details']
                                }

        return graph_nodes, loops, loop_check

    @staticmethod
    def _get_start_node(nodes: dict, sources: set, targets: set) -> dict:
        start_node_candidates = []
        for node in nodes.keys():
            style = nodes[node]['additional-details']['style']
            if style.startswith('ellipse;'):
                start_node_candidates.append(node)

        start_node_candidates_set = set(start_node_candidates)
        start_node_set = sources & start_node_candidates_set - targets
        if len(start_node_set) != 1:
            # TODO: FlowChart構造エラー
            raise AttributeError("Start Node is not only one.")
        start_node_id = start_node_set.pop()
        return {'id': start_node_id, **nodes[start_node_id]}

    def _get_nodes_and_edges(self) -> Tuple[dict, dict, set, set]:
        """
        NodeとEdgeのリストを以下の形式で出力

        Returns
        -------
        -
            Nodes
            [{'id': '10', 'additional-details': {'node_type': 'mxCell', 'value': '', 'style': 'ellipse;whiteSpace=wrap;
            html=1;aspect=fixed;', 'parent': '1', 'vertex': '1'}},
             {'id': '11', 'additional-details': {'node_type': 'mxCell', 'value': '', 'style': 'rounded=0;whiteSpace=wrap;
             html=1;arcSize=12;strokeOpacity=100;', 'parent': '1', 'vertex': '1'}}]

        -
            Edges
            [{'id': '12', 'source': '10', 'target': '11',
           'additional-details': {'style': 'edgeStyle=none;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;
           entryX=0.5;entryY=0;entryDx=0;entryDy=0;arcSize=12;strokeOpacity=100;',
           'parent': '1', 'edge': '1'}},
           {'id': '17', 'source': '11', 'target': '13',
           'additional-details': {'style': 'edgeStyle=none;html=1;entryX=0.5;
           entryY=0;entryDx=0;entryDy=0;arcSize=12;strokeOpacity=100;',
           'parent': '1', 'edge': '1'}}]

        -
            Source Nodes set
        -
            Target Nodes set


        """
        # Edge情報の取得
        edges, sources, targets = self._get_edges()

        # Edgeと接続されているNode候補を出力
        candidate_node_ids = self._get_source_target_ids_from_edges(edges=edges)

        # Node(Edgeと接続されている部品)情報を取得
        nodes = self._get_nodes(candidate_node_ids)

        return nodes, edges, sources, targets

    def _get_edges(self) -> Tuple[dict, set, set]:
        """
        rootからsouce, targetに接続しているEdge要素を抽出する。
        """
        # エッジ情報を保存するための辞書
        edge_info = {}
        targets = []
        sources = []
        # 各エッジ（mxCell要素）をループ
        for mxCell in self.root.iter('mxCell'):
            # エッジのID、source、targetを取得
            edge_id = mxCell.get('id')
            edge_source = mxCell.get('source')
            edge_target = mxCell.get('target')
            sources.append(edge_source)
            targets.append(edge_target)

            # id, source, target全てが存在するものをエッジとして辞書に保存
            if edge_id and edge_source and edge_target:
                # Getting additional properties
                additional = {}
                for prop in mxCell.keys():
                    if prop not in ['id', 'source', 'target']:
                        additional[prop] = mxCell.get(prop)
                edge_info[f"{edge_source}-{edge_id}-{edge_target}"] = {
                    'id': edge_id,
                    'source': edge_source,
                    'target': edge_target,
                    'additional-details': additional}

        sources_set = set(sources)
        targets_set = set(targets)
        return edge_info, sources_set, targets_set

    @staticmethod
    def _get_source_target_ids_from_edges(edges: dict) -> set:
        # sourceとtargetの値を抜き出す
        sources = {v['source'] for v in edges.values()}
        targets = {v['target'] for v in edges.values()}

        # sourceとtargetの値を結合し、重複を除去
        source_target_nodes = sources.union(targets)
        return source_target_nodes

    def _get_nodes(self, candidate_ids: set) -> dict:
        nodes: dict = {}

        for mxCell in self.root.iter('mxCell'):
            node_id = mxCell.get('id')
            # id=0 exist, so this if statement is needed.
            if node_id is not None and node_id in candidate_ids:
                # その他のプロパティも辞書に保存
                additional: dict = {'node_type': 'mxCell'}
                for prop in mxCell.keys():
                    if prop not in ['id']:
                        additional[prop] = mxCell.get(prop)
                nodes[node_id] = {'additional-details': additional}

        for obj in self.root.iter('object'):
            node_id = obj.get('id')
            additional = {'node_type': 'object/mxCell'}
            # その他のプロパティも辞書に保存
            for obj_prop in obj.keys():
                if obj_prop not in ['id']:
                    additional[obj_prop] = obj.get(obj_prop)
            # 内包しているmxCellのプロパティも辞書に保存
            for obj_mxCell in obj.iter('mxCell'):
                for prop in obj_mxCell.keys():
                    additional[prop] = obj_mxCell.get(prop)

            nodes[node_id] = {'additional-details': additional}

        return nodes

    @staticmethod
    def _add_value_to_list(d, key, value):
        if key not in d:
            # If the key does not exist in the dictionary, create a new list with the value
            d[key] = [value]
        else:
            # If the key exists, append the value to the existing list
            d[key].append(value)
        return d

    @staticmethod
    def _add_value_to_dict(d, key, sub_key, value):
        if key not in d:
            # If the key does not exist in the dictionary, create a new dict with the value
            d[key] = {sub_key: value}
        else:
            # If the key exists, append the value to the existing dict
            d[key][sub_key] = value
        return d
