from src.converter import LinkMLConverter
from src.helpers import *
import src.formatter as fmt
from src.model import Benchmark


benchmark_yaml = load_benchmark('data/Benchmark_002.yaml')
converter = LinkMLConverter(benchmark_yaml)
benchmark = Benchmark(converter)
all_paths = sorted(benchmark.get_output_paths())
nodes = benchmark.get_nodes()


def format_output_templates_to_be_expanded(node):
    return fmt.format_output_templates_to_be_expanded(node)


def format_input_templates_to_be_expanded(wildcards):
    return fmt.format_input_templates_to_be_expanded(converter, nodes, all_paths, wildcards)
