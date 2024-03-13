#!/usr/bin/env snakemake -s
##
## Snakefile to orchestrate YAML-defined omnibenchmarks
##
## Started 05 Feb 2024
##
## Izaskun Mallona


from snakemake import rules
import os.path as op

include: 'snakemake.py'

configfile: op.join('data', 'Benchmark_001.yaml')

rule all:
    input:
        expand('{pre}/{stage}/{module}/{params}/{name}.model.out.gz',
               pre = 'out/data/D1/default/process/P2/default',
               stage = 'methods',
               params = 'default',
               module = ['M2', 'M1'],
               name = ['D1', 'D2'])
               

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

# for dataset_id in converter.get_initial_datasets():
#     rule:
#         name: f"{{dataset}}_materialize".format(dataset = dataset_id)
#         input:
#             op.join('log', 'system_profiling.txt')
#         output:
#
#             format_output_templates_to_be_expanded(stage_id = 'data', module_id = module_id)
#             format_dataset_templates_to_be_expanded(dataset = dataset_id)
#             # "out/data/{dataset}/{params}/{dataset}_params.txt"
#         script:
#             op.join('src', 'do_something.py')


## nested module runner, dynamically getting input/outputs (paths)
stages = converter.get_benchmark_stages()
for stage_id in stages:
    stage = stages[stage_id]

    modules_in_stage = converter.get_modules_by_stage(stage)
    for module_id in modules_in_stage:
        if converter.is_initial(stage):
            rule:
                name: f"stage_{{stage}}_module_{{module}}_run".format(stage = stage_id, module = module_id)
                input:
                    op.join('log','system_profiling.txt')
                wildcard_constraints:
                    # pre = '(.*\/.*)+',
                    stage='|'.join([re.escape(x) for x in converter.get_benchmark_stages()]),
                    # params = "default",
                    name='|'.join([re.escape(x) for x in converter.get_initial_datasets()])
                output:
                    format_output_templates_to_be_expanded(stage_id=stage_id,module_id=module_id)
                    # "out/data/{dataset}/{params}/{dataset}_params.txt"
                script:
                    op.join('src','do_something.py')
        if not converter.is_terminal(stage):
            rule:
                wildcard_constraints:
                    # pre = '(.*\/.*)+',
                    stage = '|'.join([re.escape(x) for x in converter.get_benchmark_stages()]),
                    # params = "default",
                    name = '|'.join([re.escape(x) for x in converter.get_initial_datasets()])
                name: f"stage_{{stage}}_module_{{module}}_run".format(stage = stage_id, module = module_id)
                output:
                    format_output_templates_to_be_expanded(stage_id = stage_id, module_id = module_id)
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
