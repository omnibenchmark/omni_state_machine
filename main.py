from src.helpers import *
from src.converter import BenchmarkConverter, YamlConverter


if __name__ == "__main__":
    config = load_yaml_file('data/Benchmark_001.yaml')
    benchmark = load_benchmark('data/Benchmark_001.yaml')
    converter = YamlConverter(config)
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

