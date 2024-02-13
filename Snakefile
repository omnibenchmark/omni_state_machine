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

for stage in get_benchmark_stages():
    print('Stage', stage)

    print('  ', stage, 'with modules', get_modules_by_stage(stage), '\n')
    print('  Implicit inputs:\n', get_stage_implicit_inputs(stage))
    print('  Explicit inputs:\n', get_stage_explicit_inputs(stage))
    print('  Outputs\n', get_stage_outputs(stage))
    print('------')

    for module in get_modules_by_stage(stage):
        print('  Module', module)
        print('    Excludes:', get_module_excludes(stage,  module))
        print('    Params:',  get_module_parameters(stage, module))
    print('------')

# print(get_initial_datasets())
# print(get_stage_output_filenames('data'))

rule all:
    input:
        expand(get_stage_output_filenames('data'),
               stage = 'data',
               mod = get_initial_datasets(),
               params = 'default')

## seed the benchmark with datasets

stages = get_benchmark_stages()
datasets = get_initial_datasets()

print('datasets are', datasets)

for stage in stages:
    if is_initial(stage):
        # o = get_stage_output_filenames(stage)
        o = expand("{stage}/{mod}/{params}/{stage}.txt.gz",
                   params = 'default',
                   stage = 'data',
                   mod = get_initial_datasets())
        
        for mod in get_modules_by_stage(stage):
            rule:
                name: f"{stage}_{mod}"
                output: o
                shell:
                    """
                    mkdir -p {wildcards.stage}/{wildcards.mod}/{wildcards.params}

                    echo {wildcards.stage} and {wildcards.mod} > \
                      {wildcards.stage}/{wildcards.mod}/{wildcards.params}/{wildcards.stage}.txt.gz
 
                    """
# checkpoint initial_nodes:
#     output:
#         # lambda wildcards: get_stage_output_filenames(wildcards.stage)
#         directory()
#     run:
#         fake_something_to_do(wildcards.stage, wildcards.module)
    
        
