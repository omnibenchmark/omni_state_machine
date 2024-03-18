import src.formatter as fmt
from src.dag import *
from src.converter import BenchmarkConverter
import re

if __name__ == "__main__":
    benchmark = load_benchmark('data/Benchmark_001.yaml')
    converter = BenchmarkConverter(benchmark)
    print(converter.get_benchmark_definition())

    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]
        stage_name = stage['name']
        print('Stage', stage_name)

        modules_in_stage = converter.get_modules_by_stage(stage)
        print('  ', stage_name, 'with modules', modules_in_stage.keys(), '\n')
        print('  Implicit inputs:\n', converter.get_stage_implicit_inputs(stage))
        print('  Explicit inputs:\n', converter.get_stage_explicit_inputs(stage))
        print('  Outputs\n', converter.get_stage_outputs(stage))
        print('------')

        for module_id in modules_in_stage:
            module = modules_in_stage[module_id]
            module_name = module['name']
            print('  Module', module_name)
            print('    Excludes:', converter.get_module_excludes(module))
            print('    Params:', converter.get_module_parameters(module))
        print('------')

    print('------')
    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]

        modules_in_stage = converter.get_modules_by_stage(stage)
        for module_id in modules_in_stage:
            if not converter.is_initial(stage) and not converter.is_terminal(stage):
                result = fmt.format_output_templates_to_be_expanded(converter, stage_id=stage_id, module_id=module_id, param_id='default')
                print(result)

    G = build_dag_from_definition(converter)
    plot_graph(G, output_file='output_dag.png', scale_factor=1.5, node_spacing=0.2)
    initial_nodes, terminal_nodes = find_initial_and_terminal_nodes(G)

    all_paths = set()
    for initial_node in initial_nodes:
        for terminal_node in terminal_nodes:
            paths = list_all_paths(G, initial_node, terminal_node)

            for path in paths:
                paths = construct_output_paths(converter, prefix='out', nodes=path)
                all_paths.update(paths)

    all_paths = list(all_paths)