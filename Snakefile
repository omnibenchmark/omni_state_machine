#!/usr/bin/env snakemake -s
##
## Snakefile to orchestrate YAML-defined omnibenchmarks
##
## Started 05 Feb 2024
##
## Izaskun Mallona

from snakemake import rules
import os.path as op

include: op.join('src', 'workflow_helpers.py')

configfile: op.join('data', 'minibenchmark.yaml')

print(get_benchmark_definition())

print("\nStages are:")
for stage in get_benchmark_stages():
    print('  ', stage, 'with modules', get_modules_by_stage(stage), '\n')

rule all:
    input:
        op.join('out', 'helloworld.txt')

rule hello:
    output:
        op.join('out', 'helloworld.txt')        
    shell:
        """
        mkdir -p out
        date >> {output}
        """
