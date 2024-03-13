from src.helpers import *
import src.formatter as fmt
from src.converter import BenchmarkConverter


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

    for dataset in converter.get_initial_datasets():
        result = fmt.format_dataset_templates_to_be_expanded(converter, dataset)
        print(result)

    print('------')
    stages = converter.get_benchmark_stages()
    for stage_id in stages:
        stage = stages[stage_id]

        modules_in_stage = converter.get_modules_by_stage(stage)
        for module_id in modules_in_stage:
            if not converter.is_initial(stage) and not converter.is_terminal(stage):
                result = fmt.format_output_templates_to_be_expanded(converter, stage_id=stage_id, module_id=module_id)
                print(result)


