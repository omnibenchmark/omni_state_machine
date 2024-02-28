#!/usr/bin/env snakemake -s
##
## Snakefile to orchestrate YAML-defined omnibenchmarks
##
## Started 05 Feb 2024
##
## Izaskun Mallona


from snakemake import rules
import os.path as op
import dpath
import json

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


rule all:
    input:
        ## some datasets (these are initial nodes)
        expand('data/{dataset}/{params}/{dataset}_params.txt',
               dataset = ['D1', 'D2'],
               params = 'default'),
        ## some intermediate steps outputs
        expand('{pre}/{stage}/{module}/{params}/{id}.model.out.gz',
               pre = 'out/data/D1/default/process/P2/default',
               stage = 'methods',
               params = 'default',
               module = ['M2', 'M1'],
               id = ['D1', 'D2'])
               

rule start_benchmark:
    output:
        seed = op.join('log', 'system_profiling.txt')
    shell:
        """
        echo '---------------' > {output.seed}
        echo 'DATE' >> {output.seed}
        date >> {output.seed}
        echo '\nOS' >> {output.seed}
        uname -a >> {output.seed}
        echo '\nnproc' >> {output.seed}
        nproc >> {output.seed}
        echo '\ncgroups' >> {output.seed}
        ## to detect docker runs
        cat /proc/1/cgroup >> {output.seed}        
        """

# rule flow -  ------------------------------------------------------------------------------------------

# start dynamic per-stage and per-module rule generator
# for stage in stages:
#     for module in modules:
#         if initial:
#             seed it
#         if intermediate:
#             get input templates, fstringed
#             get output templates, fstringed
#         if terminal:
#             do nothing (now)
# end

for dataset in get_initial_datasets():
    rule:
        name: "materialize_dataset"#.format(dataset = dataset)
        input:
            op.join('log', 'system_profiling.txt')
        output:
            format_dataset_templates_to_be_expanded(dataset)
            # "data/{dataset}/{params}/{dataset}_params.txt"
        script:
            op.join('src', 'do_something.py')

## nested module runner, dynamicly getting input/outputs (paths)
for stage in get_benchmark_stages():
    for module in get_modules_by_stage(stage):        
        if not is_initial(stage) and not is_terminal(stage):
            rule:
                wildcard_constraints:
                    # pre = '(.*\/.*)+',
                    stage = '|'.join([re.escape(x) for x in get_benchmark_stages()]),
                    # params = "default",
                    id = '|'.join([re.escape(x) for x in get_initial_datasets()])
                name: f"{{module}}_run_module".format(module = module)
                output:
                    format_output_templates_to_be_expanded(stage = stage, module = module)
                script:
                    op.join("src", "do_something.py")

# start dynamic gatherer generator
# for stage in stages:
#     if not initial nor terminal:
#         for module in modules:
#             get param ranges
#             get excludes
#             expand rules accordingly

# rule 'all (metrics)' start
# for stage in stages:
#     if stage is terminal:
#         get inputs
#         build rule with that
# rule 'all' end
# end

print(get_stage_implicit_inputs(stage = 'methods'))

## mind stage is the previous stage, and module is the previous module
print(format_input_templates_to_be_expanded(stage = 'metrics', module = 'M1'))
# print(get_stage_explicit_inputs(stage = 'methods'))


# traverse graph
## dv stands for deliverables
dvs = list()
dv = dict()

datasets = get_datasets()

for stage in get_benchmark_stages():
    for module in get_modules_by_stage(stage):
        ii_list = get_stage_implicit_inputs(stage)
        excludes = get_module_excludes(stage, module)
        if excludes is None:
            excludes = ''
        outputs = get_stage_outputs(stage)
        parameters = get_module_parameters(stage, module)
        if parameters is None:
            parameters = 'default'

        if is_initial(stage):
            id = module ## in this case, module names are dataset names
            curr = [ x.format(stage = stage,
                              mod = module,
                              params = parameters,
                              id = id) for x in outputs.values() ]
            
            bnames = [op.basename(x) for x in curr]
            dname = list(set([op.dirname(x) for x in curr]))[0]
            dpath.new(dv, dname, bnames)

        elif not is_terminal(stage):
            ## now intermediate steps are going to have {input_dir} stuffs:
            parent = get_parent_stage(stage)
            generation = get_parent_stage_rank(stage) ## how many stage/module/params the path has
            print(generation)
            for id in list(set(datasets) - set(excludes)):
                glob_pattern = op.join(get_initial_stage_name(), id, '*')
                            
                curr = [ x.format(input_dirname = 'HERE',
                                  stage = stage,
                                  mod = module,
                                  params = parameters,
                                  id = id) for x in outputs.values() ]
                
                bnames = [op.basename(x) for x in curr]
                parent_dirname = dpath.get(dv, glob_pattern)
                print(parent_dirname)
                dname = list(set([op.dirname(x) for x in curr]))
                dpath.new(dv, dname, bnames)
                    
print('----')
print(json.dumps(dv, indent = 4, sort_keys = True))


# def get_deliverables_dictionary_depth(dv):
#     return 1 + (max(map(get_deliverables_dictionary_depth, dv.values())) if dv else 0)

# print(get_parent_stage('methods'))
# print(get_deliverables_dictionary_depth(dv))


# def cut_tree(d, depth = 1):
#     i = 0
#     for key, value in d.items():
#         if (type(value) is dict):
#             cut_tree(value, depth)
#         else:
#             raise(Exception('too deep'))
#         if i == depth:
#             break
#     return([key, value])

# cut_tree(dv, 0)
