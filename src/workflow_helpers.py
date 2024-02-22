#!/usr/bin/env python
##
## Helpers to orchestrate YAML-defined omnibenchmarks
##
## Started 05 Feb 2024
##
## Izaskun Mallona

# import dag
import os.path as op
import sys

def clone_repo(module_name):
    return('todo')

def get_benchmark_definition():
    return(config)

def get_benchmark_stages():
    return(config['stages'])

def get_modules_by_stage(stage):
    for st in config['stages'].keys():
        if st == stage:
             return([x['name'] for x in config['stages'][st]['members']])

def get_modules():
    m = []
    for st in config['stages'].keys():
        m.append([x['name'] for x in config['stages'][st]['members']])
    return(sum(m, []))

def get_module_parameters(stage, module):
    params = None
    for member in config['stages'][stage]['members']:
        if member['name'] is module and 'parameters' in member.keys():
            params = member['parameters']
    return(params)

def get_module_excludes(stage, module):
    excludes = None
    for member in config['stages'][stage]['members']:
        if member['name'] is module and 'exclude' in member.keys():
            excludes = member['exclude']
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
        for i in range(len(implicit)):
            for in_deliverable in implicit[i].keys():                
                in_stage =  implicit[i][in_deliverable]

                # beware stage needs to be substituted
                curr_output = get_stage_outputs(stage = in_stage)[in_deliverable]
     
                explicit[i][in_deliverable] = curr_output
    
    return(explicit)

def get_stage_explicit_input_dirnames(stage):
    explicit = get_stage_explicit_inputs(stage)
    de = explicit
    if explicit is not None:
        for i in range(len(explicit)):
            for in_deliverable in explicit[i].keys():
                de[i][in_deliverable] = op.dirname(explicit[i][in_deliverable])
    
    return(de)

def is_initial(stage):
    if 'initial' in config['stages'][stage].keys() and config['stages'][stage]['initial']:
        return(True)
    else:
        return(False)
    
def is_terminal(stage):
    if 'terminal' in config['stages'][stage].keys() and config['stages'][stage]['terminal']:
        return(True)
    else:
        return(False)

def get_initial_datasets():
    for stage in get_benchmark_stages():
        if is_initial(stage):
            return(get_modules_by_stage(stage))

def get_initial_dataset_paths(dataset):
    filled = []
    for stage in config['stages'].keys():
        if 'initial' in config['stages'][stage].keys() and config['stages'][stage]['initial']:
             outs = list(get_stage_outputs(stage).values())
    for i in range(len(outs)):
        filled.append([outs[i].format(stage = 'out', mod = dataset, params = 'default', id = dataset)])
             
    return(sum(filled, []))

# dirty, fix
def write_module_flag_for_dirty_module_wildcards(module):
    ## creates an empty file
    open(op.join('out', f"{module}.flag".format(module = module)), 'a')
        

def tokenize_parameters():
    print('todo')

def exclude_items_from_explicit_outputs():
    print('todo')
    
def nest_deliverable_paths():
    print('todo')
