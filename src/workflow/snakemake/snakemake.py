import argparse
import os

from src.model import Benchmark, BenchmarkNode
from src.workflow.workflow import WorkflowEngine
from src.workflow.snakemake import rules
from snakemake.cli import main as snakemake_cli

from datetime import datetime

# Define includes
INCLUDES = [
    "utils.smk",
    "rule_start_benchmark.smk",
    "rule_node.smk",
    "rule_all.smk",
]


class SnakemakeEngine(WorkflowEngine):
    def __init__(self):
        super().__init__()

    def run_workflow(self, benchmark: Benchmark, cores: int = 1, dryrun: bool = False, work_dir: str = os.getcwd(),
                     **snakemake_kwargs):

        # Serialize Snakefile for workflow
        snakefile = self.serialize_workflow(benchmark, work_dir)

        # Prepare the argv list
        argv = self._prepare_argv(snakefile, cores, dryrun, work_dir, **snakemake_kwargs)

        # Execute snakemake script
        success = snakemake_cli(argv)

        return success

    def serialize_workflow(self, benchmark: Benchmark, output_dir: str = os.getcwd()):
        os.makedirs(output_dir, exist_ok=True)

        benchmark_file = benchmark.get_definition_file()

        # Serialize Snakemake file
        snakefile_path = os.path.join(output_dir, 'Snakefile')
        with open(snakefile_path, 'w') as f:
            self._write_snakefile_header(f)
            self._write_includes(f, INCLUDES)

            # Load benchmark from yaml file
            f.write(f'benchmark = load("{benchmark_file}")\n\n')

            # Create capture all rule
            f.write("all_paths = sorted(benchmark.get_output_paths())\n")
            f.write("create_all_rule(all_paths)\n\n")

            # Create node rules
            f.write("nodes = benchmark.get_nodes()\n")
            f.write("for node in nodes:\n")
            f.write("    create_node_rule(node, benchmark)\n\n")

        return snakefile_path

    def run_node_workflow(self, node: BenchmarkNode, cores: int = 1, dryrun: bool = False, work_dir: str = os.getcwd(),
                          **snakemake_kwargs):

        os.makedirs(work_dir, exist_ok=True)

        # Serialize Snakefile for node workflow
        snakefile = self.serialize_node_workflow(node, work_dir)

        # Prepare the argv list
        argv = self._prepare_argv(snakefile, cores, dryrun, work_dir, **snakemake_kwargs)

        # Execute snakemake script
        success = snakemake_cli(argv)

        return success

    def serialize_node_workflow(self, node: BenchmarkNode, output_dir=os.getcwd()):
        os.makedirs(output_dir, exist_ok=True)

        benchmark_file = node.get_definition_file()

        # Serialize Snakemake file
        snakefile_path = os.path.join(output_dir, 'Snakefile')
        with open(snakefile_path, 'w') as f:
            self._write_snakefile_header(f)
            self._write_includes(f, INCLUDES)

            # Load benchmark from yaml file
            f.write(f'node = load_node("{benchmark_file}", "{node.get_id()}")\n\n')

            # Create capture all rule
            f.write("input_paths = node.get_input_paths()\n")
            f.write("output_paths = node.get_output_paths()\n")
            f.write("all_paths = input_paths + output_paths\n\n")
            f.write("create_all_rule(all_paths)\n\n")

            # Create node rules
            f.write("create_node_rule(node)\n\n")

        return snakefile_path

    def _write_snakefile_header(self, f):
        f.write("#!/usr/bin/env snakemake -s\n")
        f.write("##\n")
        f.write("## Snakefile to orchestrate YAML-defined omnibenchmarks\n")
        f.write("##\n")
        f.write(f"## This Snakefile has been automatically generated on {datetime.now()}\n")
        f.write('\n')

    def _write_includes(self, f, includes):
        includes_path = os.path.dirname(os.path.realpath(rules.__file__))
        for include in includes:
            f.write(f'include: "{os.path.join(includes_path, include)}"\n')

        f.write('\n')

    def _prepare_argv(self, snakefile: str, cores: int, dryrun: bool, work_dir: str, **snakemake_kwargs):
        argv = [
            '--snakefile', snakefile,
            '--cores', str(cores)
        ]

        if dryrun:
            argv.append('--dryrun')

        for key, value in snakemake_kwargs.items():
            if isinstance(value, bool):
                if value:  # Add flag only if True
                    argv.append(f'--{key}')
            else:
                argv.extend([f'--{key}', str(value)])

        return argv
