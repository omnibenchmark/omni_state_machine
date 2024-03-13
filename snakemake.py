from src.converter import BenchmarkConverter
from src.helpers import *
import src.formatter as fmt


benchmark = load_benchmark('data/Benchmark_001.yaml')
converter = BenchmarkConverter(benchmark)

def format_dataset_templates_to_be_expanded(dataset):
    return fmt.format_dataset_templates_to_be_expanded(converter, dataset)


def format_output_templates_to_be_expanded(stage_id, module_id):
    return fmt.format_output_templates_to_be_expanded(converter, stage_id, module_id)


def format_input_templates_to_be_expanded(stage_id, module_id):
    return fmt.format_input_templates_to_be_expanded(converter, stage_id, module_id)
