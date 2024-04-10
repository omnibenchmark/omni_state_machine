import networkx as nx
import matplotlib.pyplot as plt

from src.model.node import BenchmarkNode

def expend_stage_nodes(converter, stage, output_folder):
    nodes = []

    input_dirname = output_folder if converter.is_initial(stage) else '{pre}'
    stage_outputs = converter.get_stage_outputs(stage).values()
    outputs = [x.replace('{input_dirname}', input_dirname) for x in stage_outputs]

    inputs_for_stage = converter.get_stage_implicit_inputs(stage)
    if not inputs_for_stage or len(inputs_for_stage) == 0:
        inputs_for_stage = [None]

    modules_in_stage = converter.get_modules_by_stage(stage)
    for module_id in modules_in_stage:
        module = modules_in_stage[module_id]
        parameters = converter.get_module_parameters(module)
        if not parameters or len(parameters) == 0:
            parameters = [None]

        for param_id, param in enumerate(parameters):
            for run_id, inputs in enumerate(inputs_for_stage):
                run_id = None if len(inputs_for_stage) <= 1 else run_id
                inputs = converter.get_stage_explicit_inputs(inputs).values() if inputs else None
                inputs = [x.replace('{input_dirname}', '{pre}') for x in inputs] if inputs else None
                node = BenchmarkNode(converter, stage, module, param, inputs, outputs, param_id, run_id)
                nodes.append(node)

    return nodes


def build_dag_from_definition(converter, output_folder):
    g = nx.DiGraph()
    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]
        nodes = expend_stage_nodes(converter, stage, output_folder)
        g.add_nodes_from(nodes)

    for stage_id in stages:
        stage = stages[stage_id]
        after_stage_ids = converter.get_after(stage)
        if after_stage_ids and len(after_stage_ids) > 0:
            for departure_stage_id in after_stage_ids:
                departure_stage = stages[departure_stage_id]
                departure_stage_nodes = expend_stage_nodes(converter, departure_stage, output_folder)
                current_stage_nodes = expend_stage_nodes(converter, stage, output_folder)

                for departure_stage_node in departure_stage_nodes:
                    for current_stage_node in current_stage_nodes:
                        g.add_edge(departure_stage_node, current_stage_node)

    return g


def find_initial_and_terminal_nodes(graph):
    initial_nodes = [node for node, in_degree in graph.in_degree() if in_degree == 0]
    terminal_nodes = [node for node, out_degree in graph.out_degree() if out_degree == 0]
    return initial_nodes, terminal_nodes


def list_all_paths(graph, source, target):
    all_paths = list(nx.all_simple_paths(graph, source=source, target=target))
    return all_paths


def contains_all(path, modules):
    path_modules = [node.module_id for node in path]
    return all(module in path_modules for module in modules)


def exclude_paths(paths, path_exclusions):
    updated_paths = []
    for path in paths:
        should_exclude = False
        for module, excluded_modules in path_exclusions.items():
            for excluded_module in excluded_modules:
                if contains_all(path, [module, excluded_module]):
                    should_exclude = True

        if not should_exclude:
            updated_paths.append(path)

    return updated_paths


def plot_graph(g, output_file, scale_factor=1.0, node_spacing=0.1, figure_size=(12, 12)):
    layout = nx.circular_layout(g, scale=scale_factor)

    plt.figure(figsize=figure_size)

    nx.draw_networkx_edges(g, layout, edge_color='#AAAAAA')
    nx.draw_networkx_nodes(g, layout, nodelist=g.nodes(), node_size=100, node_color='#fc8d62')
    nodes = [node for node in g.nodes]
    for l in layout:
        layout[l][1] -= node_spacing

    nx.draw_networkx_labels(g, layout, labels=dict(zip(nodes, nodes)), font_size=10)

    # Save the figure to an image file
    plt.savefig(output_file)
