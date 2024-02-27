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
        [get_initial_dataset_paths(x) for x in get_datasets()],
        expand('{pre}/{stage}/m2/{params}/{id}.txt',
               pre = 'out/data/D1/default/process/P2/default/methods/M2/default',
               stage = 'metrics',
               params = 'default',
               id = 'D1'),
        expand('{pre}/{stage}/P1/{params}/{id}.txt',
               pre = 'out/data/D2/default',
               stage = 'process',
               params = 'default',
               id = 'D2')
               

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


## the output TEMPLATES should be parsed dynamically too, @todo
for dataset in get_initial_datasets():
    rule:
        name: "{{dataset}}_materialize_dataset".format(dataset = dataset)
        input:
            op.join('log', 'system_profiling.txt')
        output:
            op.join('{{stage}}'.format(stage = get_initial_stage_name()),
                    '{{dataset}}'.format(dataset = dataset),
                    '{params}',
                    '{{dataset}}.txt.gz'.format(dataset = dataset)),
            op.join('{{stage}}'.format(stage = get_initial_stage_name()),
                    '{{dataset}}'.format(dataset = dataset),
                    '{params}',
                    '{{dataset}}_params.txt'.format(dataset = dataset)),
            op.join('{{stage}}'.format(stage = get_initial_stage_name()),
                    '{{dataset}}'.format(dataset = dataset),
                    '{params}',
                    '{{dataset}}.meta.json'.format(dataset = dataset))
        params:
            path =  op.join('{{stage}}'.format(stage = get_initial_stage_name()),
                            '{{dataset}}'.format(dataset = dataset),
                            '{params}')
        script:
            op.join('src', 'do_something.py')
        # shell:
        #     """
        #     mkdir -p {params.path}
        #     echo " {wildcards}" > {output[0]}
        #     echo " {wildcards}" > {output[1]}
        #     echo " {wildcards}" > {output[2]}
        #     """
 

## nested module runner, dynamicly getting input/outputs (paths)
for stage in get_benchmark_stages():
    for module in get_modules_by_stage(stage):
        if is_initial(stage):
            pass
    
        rule:
            wildcard_constraints:
                # pre = '(.*\/.*)+',
                stage = '|'.join([re.escape(x) for x in get_benchmark_stages()]),
                params = "default",
                id = '|'.join([re.escape(x) for x in datasets])
            name: f"{{module}}_run_module".format(module = module)
            output:
                "{{pre}}/{{stage}}/{module}/{{params}}/{{id}}.txt".format(module = module)
            params:
                path =  "{{pre}}/{{stage}}/{module}/{{params}}".format(module = module)
            # shell:
            #     """
            #     mkdir -p {params.path}
            #     echo "{wildcards}" > {output}
            #     """
            script:
                op.join("src", "do_something.py")

# start dynamic gatherer generator
# for stage in stages:
#     if not initial nor terminal:
#         for module in modules:
#             get param ranges
#             get excludes
#             expand rules accordingly

# rule 'all' start
# for stage in stages:
#     if stage is terminal:
#         get inputs
#         build rule with that
# rule 'all' end
# end

print([get_initial_dataset_paths(x) for x in get_datasets()])

