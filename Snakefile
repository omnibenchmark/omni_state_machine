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
        all_paths,
        # "out/data/D2/default/D2.dataext",
        # "out/data/D2/default/process/P1/default/D2.txt.gz",
        # "out/data/D1/default/process/P2/default/methods/M2/default/D1.model.out.gz"


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


stages = converter.get_benchmark_stages()
for node in G.nodes:
    print('node is', node)
    stage_id = node.stage_id
    module_id = node.module_id
    param_id = node.param_id

    stage = stages[stage_id]
    print('stage_id is', stage_id, 'and module_id is', module_id, 'is initial', converter.is_initial(stage))

    if converter.is_initial(stage):
        rule:
            name: f"{{stage}}_{{module}}_{{param}}_run".format(stage=stage_id, module=module_id, param=param_id)
            wildcard_constraints:
                stage= stage_id,
                param = "default",
                name= module_id 
            output:
                "out/{stage}/{name}/{param}/{name}.txt.gz",
                "out/{stage}/{name}/{param}/{name}.meta.json",
                "out/{stage}/{name}/{param}/{name}_params.txt"
            script:
                op.join('src','do_something.py')
    elif converter.is_terminal(stage):
        rule:
            name: f"{{stage}}_{{module}}_{{param}}_run".format(stage=stage_id, module=module_id, param=param_id)
            script:
                op.join('src', 'do_something.py')
    else:
        rule:
            wildcard_constraints:
                post = stage_id + '/' + module_id + '/' + param_id,
                stage= stage_id, # '|'.join([re.escape(x) for x in converter.get_benchmark_stages()]),
                module = module_id,
                name='|'.join([re.escape(x) for x in converter.get_initial_datasets()]),
                ext=".*$"
            name:  f"{{stage}}_{{module}}_{{param}}_run".format(stage=stage_id, module=module_id, param=param_id)
            input:
                '{pre}/{name}.txt.gz'                
            output:
                "{pre}/{post}/{name}.{ext}"
            script:
                op.join("src", "do_something.py")

## nested module runner, dynamically getting input/outputs (paths)

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
