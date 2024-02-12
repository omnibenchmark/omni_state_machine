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

def get_module_parameters(stage, module):
    params = None
    for member in config['stages'][stage]['members']:
        if member['name'] is module and 'parameters' in member.keys():
            params = [stage, member, member['parameters']]
    return(params)

def get_module_excludes(stage, module):
    excludes = None
    for member in config['stages'][stage]['members']:
        if member['name'] is module and 'exclude' in member.keys():
            excludes = [stage, member, member['exclude']]
    return(excludes)

def get_stage_implicit_inputs(stage):
    if 'initial' in config['stages'][stage].keys() and config['stages'][stage]['initial']:
        return(None)
    return(config['stages'][stage]['inputs'])

def get_stage_outputs(stage):
     if 'terminal' in config['stages'][stage].keys() and config['stages'][stage]['terminal']:
         return(None)
     L = config['stages'][stage]['outputs']
     return(dict(pair for d in L for pair in d.items()))

def get_stage_explicit_inputs(stage):
    implicit = get_stage_implicit_inputs(stage)
    explicit = implicit
    if implicit is not None:
        i = 0
        while i < len(implicit):
            for key in implicit[i].keys():                
                in_stage =  implicit[i][key]
                in_deliverable = key

                # beware stage needs to be substituted
                curr_output = get_stage_outputs(stage = in_stage)[in_deliverable]
     
                explicit[i][key] = curr_output
            i = i + 1

    return(explicit)

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
