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



## seed the benchmark with datasets

stages = get_benchmark_stages()
datasets = get_initial_datasets()
# print('initial datasets', get_initial_datasets())

# seed_datasets = get_stage_output_filenames(stage = 'data', dataset = 'D1')

print(list(get_stage_outputs('data').values()))
print('D1 will contain', get_initial_dataset_paths('D1'))
print('D2 will contain', get_initial_dataset_paths('D2'))

datasets = get_initial_datasets()
for dataset in datasets:
    dpaths = get_initial_dataset_paths(dataset)
    for dpath in dpaths:
        if not op.exists(op.dirname(dpath)):
            os.makedirs(op.dirname(dpath))

rule all:
    input:
        op.join('log', 'system_profiling.txt'),
        [get_initial_dataset_paths(x) for x in get_initial_datasets()],
        expand(op.join('log', "{id}.txt"), id = get_initial_datasets())

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


## not tested yet
# wildcard_constraints:
#     dataset='/'.join([re.escape(x) for x in get_initial_datasets()])

## this is an awful lot of hardcoding
for dataset in datasets:
    print(dataset)
    rule:
        name: f"{dataset}".format(dataset = dataset)
        input:
            op.join('log', 'system_profiling.txt')
        output:
            a = f"{{stage}}/{{mod}}/{{params}}/{{id}}.txt.gz".format(stage = 'data',
                                                                 params = 'default',
                                                                 mod = dataset,
                                                                 id = dataset),
            b = f"{{stage}}/{{mod}}/{{params}}/{{id}}_params.txt".format(stage = 'data',
                                                                     params = 'default',
                                                                     mod = dataset,
                                                                     id = dataset),
            c = f"{{stage}}/{{mod}}/{{params}}/{{id}}.meta.json".format(stage = 'data',
                                                                     params = 'default',
                                                                     mod = dataset,
                                                                     id = dataset)
        shell:
            """
            echo no wildcards here Im afraid! > {output.a}
            echo {wildcards} > {output.b}
            echo {wildcards} > {output.c}
              
            """

rule wildcard_awareness:
    input:
        [get_initial_dataset_paths(x) for x in get_initial_datasets()]
    output:
        op.join('log', "{id}.txt")
    shell:
        """
        echo {wildcards} > {output} ## only id
        """
