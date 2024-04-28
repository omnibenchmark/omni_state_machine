from src.converter import LinkMLConverter
from src.helpers import *
import src.formatter as fmt
from src.model import Benchmark
from src.validation import Validator, ValidationError

try:
    benchmark_yaml = load_benchmark('data/Benchmark_002.yaml')
    converter = LinkMLConverter(benchmark_yaml)
    validator = Validator()
    converter = validator.validate(converter)
    benchmark = Benchmark(converter)
    all_paths = sorted(benchmark.get_output_paths())
    nodes = benchmark.get_nodes()

except ValidationError as e:
    print("Validation failed: ")
    for error in e.errors:
        print(error)


def format_output_templates_to_be_expanded(node):
    return fmt.format_output_templates_to_be_expanded(node)


def format_input_templates_to_be_expanded(wildcards):
    return fmt.format_input_templates_to_be_expanded(converter, nodes, all_paths, wildcards)
