from typing import List

import graphviz
from graphviz import Digraph

from tinydag.node import Node


def render(nodes: List[Node],
           user_input: List[str],
           path: str = "graph.gv",
           view: bool = True) -> Digraph:
    dot = graphviz.Digraph()
    for node in nodes:
        dot.node(node.name, node.name, shape='box', style='filled', fillcolor='lightblue')
        for output in node.outputs:
            dot.node(output, output, shape='oval', style='filled', fillcolor='lightgreen')
            dot.edge(node.name, output)
        for node_input in node.inputs:
            if node_input in user_input:
                dot.node(node_input, node_input, shape='ellipse', style='filled', fillcolor='lightpink')
            else:
                dot.node(node_input, node_input, shape='oval', style='filled', fillcolor='lightgreen')
            dot.edge(node_input, node.name)
    dot.render(path, view=view)
    return dot
