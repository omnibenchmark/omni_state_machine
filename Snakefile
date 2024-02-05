#!/usr/bin/env snakemake -s
##
## Snakefile to orchestrate YAML-defined omnibenchmarks
##
## Started 05 Feb 2024
##
## Izaskun Mallona

from snakemake import rules
import os.path as op

configfile: op.join('data', 'minibenchmark.yaml')

def get_benchmark_definition():
    return(config)

def get_benchmark_stages():
    return(config['stages'])

def get_modules_by_stage(stage):
    for st in config['stages'].keys():
        if st == stage:
             return(config['stages'][st]['members'])

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
