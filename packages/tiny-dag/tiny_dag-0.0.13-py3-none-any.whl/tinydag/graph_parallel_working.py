import logging
import multiprocessing
import os
import time
from copy import copy
from os.path import join
from typing import List, Union, Optional

from tinydag.exceptions import InvalidGraphError, MissingInputError
from tinydag.node import Node
from tinydag.utils import load_pickle, save_pickle

logger = logging.getLogger(__name__)

try:
    import graphviz as graphviz
    from graphviz import Digraph
except ImportError:
    logger.warning("Cannot import graphviz")


class Graph:
    """
    Minimal implementation of computational (directed, acyclic) graph.

    User provides the graph structure (nodes) and input data for the graph. Every node waits until input data for that
    node is ready. Eventually, the graph executes every node in the graph and returns output of every node as the
    result.

    Example:

    def add(a, b): return {"output": a + b}
    def mul(a, b): return {"output": a * b}
    def div(a, b): return {"output": a / b}
    def add_subtract(a, b): return {"add_output": a + b, "subtract_output": a - b}

    nodes = [
        Node(["add1/output", "x"], add, "add2", ["output"]),
        Node(["add1/output", "add2/output"], mul, "mul", ["output"]),
        Node(["x", "y"], add, "add1", ["output"]),
        Node(["x", "z"], add_subtract, "add_subtract", ["add_output", "subtract_output"]),
        Node(["mul/output", "add_subtract/add_output"], div, "div", ["output"]),
    ]
    graph = Graph(nodes)

    Defines a graph with following connections:

    x, y -> add1
    x, z -> add_subtract
    add1/output, x -> add2
    add1/output, add2/output -> mul
    mul/output, add_subtract/add_output -> div

    User needs to provide x, y and z as input data for this graph when doing calculation.

    Cache can be used to save and load cached results.
    """

    def __init__(self,
                 nodes: List[Node],
                 cache_dir="cache") -> None:
        """
        :param nodes: List of nodes defining the graph.
        :param cache_dir: Directory to save and read cached files.
        :raises InvalidGraphError if the node names are not unique.
        """
        self._check_node_names_are_unique(nodes)
        self.nodes = nodes
        self.required_user_inputs = self._get_required_user_inputs()
        logger.debug(f"Required user input: {self.required_user_inputs}")

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.cache_dir = cache_dir

    def render(self,
               path: str = "graph.gv",
               view: bool = True) -> Optional["Digraph"]:
        """
        Render graph. This will only work if graphviz is available.
        :param path: Path to save fig.
        :param view: Show graph fig.
        :return: graphviz Digraph is graphviz is available, otherwise None.
        """

        try:
            dot = graphviz.Digraph()
            for node in self.nodes:
                dot.node(node.name, node.name, shape='box', style='filled', fillcolor='lightblue')
                for output in node.outputs:
                    dot.node(output, output, shape='oval', style='filled', fillcolor='lightgreen')
                    dot.edge(node.name, output)
                for node_input in node.inputs:
                    if node_input in self.required_user_inputs:
                        dot.node(node_input, node_input, shape='ellipse', style='filled', fillcolor='lightpink')
                    else:
                        dot.node(node_input, node_input, shape='oval', style='filled', fillcolor='lightgreen')
                    dot.edge(node_input, node.name)
            dot.render(path, view=view)
            return dot
        except Exception as e:
            logger.warning(f"Graph cannot be rendered, caught error: {e}")
            return None

    def check(self) -> None:
        """
        Check if the graph structure is valid.
        :raises InvalidGraphError if the graph structure is not valid.
        """
        input_data = {name: None for name in self.required_user_inputs}
        self._execute(input_data, False)

    def calculate(self,
                  input_data: Optional[dict] = None,
                  from_cache: Optional[List[str]] = None,
                  to_cache: Optional[List[str]] = None) -> dict:
        """
        Execute every node in the graph.
        :param input_data: Input data for the graph, where keys are names used in the graph definition.
        :param from_cache: List of node names to read from cache.
        :param to_cache: List of node names to save to cache.
        :return: Output of every node, with node outputs as keys.
        :raises MissingInputError if the input_data doesn't contain all the required data.
        :raises InvalidGraphError if the graph structure is not valid.
        :raises InvalidNodeFunctionOutput if the node function output is not valid.
        :raises FileNotFoundError if cache file we want to read doesn't exist.
        """
        self._check_input_data(input_data)
        return self._execute(input_data, True, from_cache, to_cache)

    def __add__(self, nodes: Union[List[Node], Node]) -> "Graph":
        if isinstance(nodes, list):
            nodes = self.nodes + nodes
        else:
            nodes = self.nodes + [nodes]
        return Graph(nodes)

    def __repr__(self) -> str:
        repr_str = "\n"
        for node in self.nodes:
            name = node.name
            repr_str += f"Node: {name}\n"
            repr_str += "├─ Inputs:\n"
            for input_node in node.inputs:
                repr_str += f"│  ├─ {input_node}\n"
            repr_str += "└─ Outputs:\n"
            for output_node in node.outputs:
                repr_str += f"   ├─ {output_node}\n"
        return repr_str

    def _check_input_data(self, input_data: Optional[dict]) -> None:
        if len(self.required_user_inputs) > 0:
            for item in self.required_user_inputs:
                if item not in input_data:
                    raise MissingInputError(f"Input data is missing {item}")

    def _get_required_user_inputs(self) -> List[str]:
        required_inputs, node_outputs = [], []
        for node in self.nodes:
            required_inputs += node.inputs
            node_outputs += node.outputs
        return list(set(required_inputs) - set(node_outputs))

    def _execute(self,
                 input_data: Optional[dict] = None,
                 run: Optional[bool] = True,
                 from_cache=None,
                 to_cache=None) -> dict:

        if from_cache is None:
            from_cache = []
        if to_cache is None:
            to_cache = []

        # Create a multiprocessing Manager
        manager = multiprocessing.Manager()

        # Create a shared dictionary for inputs
        inputs = manager.dict(input_data) if input_data is not None else manager.dict()

        nodes_to_execute = [i for i in range(len(self.nodes))]
        t_graph_start = time.time()

        queue = multiprocessing.Queue()

        # Function to execute a single node
        def execute_node(node_index):
            node = self.nodes[node_index]
            logger.debug(f"Launched task for node {node}, process id {multiprocessing.current_process().pid}")
            while True:
                logger.debug(f"Trying to execute node {node}")
                node_input_data = self._get_node_input_data(node, inputs)
                if len(node_input_data) < len(node.inputs):
                    logger.debug(f"Cannot find all the inputs for the node {node}.")
                    time.sleep(0.1)
                    continue  # All the input data cannot be found for this node yet, so skip this node
                else:
                    break

            logger.debug(f"Found all the inputs for the node {node}.")
            if run:
                results = self._get_node_results(node, node_input_data, from_cache, to_cache)
                if results is not None:
                    inputs.update(results)
            else:
                for output in node.outputs:
                    inputs[output] = None
            logger.debug(f"Node {node} executed successfully")
            logger.debug(f"Add node {node} output to inputs, inputs now contains {inputs.keys()}")
            queue.put(node_index)  # Signal completion with node index

        processes = []
        for node_index in nodes_to_execute:
            process = multiprocessing.Process(target=execute_node, args=(node_index,))
            process.start()
            processes.append(process)

        # Wait for all nodes to finish processing
        while True:
            completed_node_index = queue.get()  # Receive signal of completed node index
            logger.debug(f"Completed node index {completed_node_index}")
            if completed_node_index is not None:
                nodes_to_execute.remove(completed_node_index)
                if len(nodes_to_execute) == 0:
                    break

        logger.debug("All nodes executed successfully")
        t_graph_end = time.time()
        logger.debug(f"Graph execution took {1000 * (t_graph_end - t_graph_start): 0.2f} ms")

        results = self._create_output(inputs)

        return results

    def _create_output(self, inputs: dict) -> dict:
        results = {}
        for node in self.nodes:
            for output in node.outputs:
                results[output] = inputs[output]
        return results

    def _get_node_results(self, node: Node,
                          node_input_data: list,
                          from_cache: List[str],
                          to_cache: List[str]) -> Optional[dict]:
        path = join(self.cache_dir, node.name)
        if node.name in from_cache:
            results = load_pickle(path)
            logger.info(f"Node {node.name} results read from cache: {path}")
        else:
            results = node.run(node_input_data)
        if node.name in to_cache:
            save_pickle(path, results)
            logger.info(f"Node {node.name} results wrote to cache: {path}")
        return results

    @staticmethod
    def _check_node_names_are_unique(nodes: List[Node]) -> None:
        node_names = [n.name for n in nodes]
        if len(set(node_names)) < len(node_names):
            raise InvalidGraphError("All the nodes need to have unique name!")

    @staticmethod
    def _get_node_input_data(node: Node, inputs: dict) -> list:
        input_data = []
        for i in node.inputs:
            if i in inputs:
                input_data.append(inputs[i])
            else:
                logger.debug(f"Cannot find input {i} for node {node}.")
                break  # We cannot execute node without full input, so no need to continue
        return input_data
