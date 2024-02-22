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

## benchmark seeding (datasets and wildcard generation) ##############################################

# print(list(get_stage_outputs('out').values()))
# print('D1 will contain', get_initial_dataset_paths('D1'))
# print('D2 will contain', get_initial_dataset_paths('D2'))

datasets = get_initial_datasets()
for dataset in datasets:
    dpaths = get_initial_dataset_paths(dataset)
    for dpath in dpaths:
        if not op.exists(op.dirname(dpath)):
            os.makedirs(op.dirname(dpath))

rule all:
    input:
        op.join('log', 'done.txt'),
        op.join('out', 'methods', 'M1', 'default', 'methods_M1_default_D1_another.txt'),
        op.join('out', 'methods', 'M2', 'default', 'methods_M2_default_D1_another.txt')

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

for dataset in datasets:
    print(dataset)
    rule:
        name: f"{dataset}".format(dataset = dataset)
        input:
            op.join('log', 'system_profiling.txt')
        output:
            get_initial_dataset_paths(dataset)
        shell:
            """
            echo no wildcards here Im afraid! > {output[0]}
            echo {wildcards} > {output[1]}
            echo {wildcards} > {output[2]}
            """

## wildcards propagation ###############################################################################

for stage in get_benchmark_stages():
    for module in get_modules_by_stage(stage):
        write_module_flag_for_dirty_module_wildcards(module)
        
        ei = get_stage_implicit_inputs(stage)
        eo = get_stage_outputs(stage)

        rule:
            name: f"{module}_flagger".format(module = module)
            output: temp(op.join('out', f"{module}.flag".format(module = module)))
            script: write_module_flag_for_dirty_module_wildcards(module)
                
        rule:
            name: 'flat_module_maker' # not hierarchical/nested yet
            input:
                op.join('out', "{module}.flag")
            output:
                op.join('out', "{stage}", "{module}", "{params}",
                        "{stage}_{module}_{params}_{id}_another.txt")
            params:
                test = 'empty',
                another = 'empty too'
            threads: 2
            script:
                op.join('src', 'do_something.py')

rule done:
    input:
        expand(op.join('out', "{module}.flag"), module = get_modules())  
    output:
        op.join('log', 'done.txt')
    shell:
        "date > {output}"
        
## sandbox
## not tested yet
# wildcard_constraints:
#     dataset='/'.join([re.escape(x) for x in get_initial_datasets()])
