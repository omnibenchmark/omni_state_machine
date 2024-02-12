#!/usr/bin/env python
##
## Helpers to orchestrate YAML-defined omnibenchmarks
##
## Started 05 Feb 2024
##
## Izaskun Mallona

import dag

def get_benchmark_definition():
    return(config)

def get_benchmark_stages():
    return(config['stages'])

def get_modules_by_stage(stage):
    for st in config['stages'].keys():
        if st == stage:
             return(config['stages'][st]['members'])

def clone_repo(module_name):
    return('todo')

def get_parameters_by_module(module):
    return('todo')


## needs to expand by (initial) dataset names
def create_rule_for_module(rule_name, stage_name, module_name):
    for i in range(len(config['stages'][stage_name]['members'])):
        if config['stages'][stage_name]['members'][i]['name'] == rule_name:
            curr = config['stages'][stage_name]['members'][i]
    
    output_fn = f"results/{stage_name}/{module_name}/{name}_output.txt"

    if not config['stages']['stage'].initial:
        input_fn = f"data/{input_param}.txt"

        command = f"echo {rule_name} {input_fn} > {output_fn}"

    ## this should depend on the 'after' clauses    
    if not config['stages']['stage'].initial:
        input_fns = config['stages']['1_preprocess']['inputs']

    return Rule(
        name = rule_name,
        input = input(input_fns),
        output = output(output_fn),
        shell = command
    )
