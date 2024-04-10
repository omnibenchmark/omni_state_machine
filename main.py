from src.helpers import *
from src.converter import LinkMLConverter
from src.model.benchmark import Benchmark

if __name__ == "__main__":
    benchmark_yaml = load_benchmark('data/Benchmark_001.yaml')
    converter = LinkMLConverter(benchmark_yaml)
    benchmark = Benchmark(converter)
    print(benchmark.get_definition())

    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]
        stage_name = stage['name']
        print('Stage', stage_name)

        modules_in_stage = converter.get_modules_by_stage(stage)
        print('  ', stage_name, 'with modules', modules_in_stage.keys(), '\n')
        print('  Implicit inputs:\n', converter.get_stage_implicit_inputs(stage))
        print('  Explicit inputs:\n', [converter.get_stage_explicit_inputs(i)
                                       for i in converter.get_stage_implicit_inputs(stage)])
        print('  Outputs\n', converter.get_stage_outputs(stage))
        print('------')

        for module_id in modules_in_stage:
            module = modules_in_stage[module_id]
            module_name = module['name']
            print('  Module', module_name)
            print('    Repo:', converter.get_module_repository(module))
            print('    Excludes:', converter.get_module_excludes(module))
            print('    Params:', converter.get_module_parameters(module))
        print('------')

    print('------')

    nodes = benchmark.get_nodes()
    print('All nodes:', nodes)

    execution_paths = benchmark.get_execution_paths()
    print('All execution paths:', execution_paths)

    outputs_paths = sorted(benchmark.get_output_paths())
    print('All output paths:', outputs_paths)

    # benchmark.plot_graph()

    # print(benchmark.get_available_parameter('P2'))
    # print(benchmark.get_explicit_outputs('data'))
    # print(benchmark.get_explicit_inputs('methods'))
