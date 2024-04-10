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
        # "out/data/D1/default/process/P2/default/methods/M2/default/m1/default/D1.results.txt"

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

for node in nodes:
    stage_id = node.stage_id
    module_id = node.module_id
    param_id = node.param_id
    run_id = node.run_id

    outputs = node.get_outputs()

    post = stage_id + '/' + module_id
    if any(['{params}' in o for o in outputs]):
        post += '/' + param_id

    if any(['{run}' in o for o in outputs]):
        post += '/' + run_id

    if node.is_initial():
        rule:
            name: f"{{stage}}_{{module}}_{{param}}_{{run}}".format(stage=stage_id, module=module_id, param=param_id, run=run_id)
            wildcard_constraints:
                stage=stage_id,
                module=module_id,
                params=param_id,
                run=run_id,
                name=module_id
            output:
                format_output_templates_to_be_expanded(node)
                # "out/{stage}/{module}/{params}/{run}/{name}.txt.gz",
                # "out/{stage}/{module}/{params}/{run}/{name}.meta.json",
                # "out/{stage}/{module}/{params}/{run}/{name}_params.txt"
            params:
                parameters = node.get_parameters()
            script:
                'do_something.py'
    else:
        rule:
            wildcard_constraints:
                post=post,
                stage=stage_id,
                module=module_id
            name: f"{{stage}}_{{module}}_{{param}}_{{run}}".format(stage=stage_id,module=module_id,param=param_id,run=run_id)
            input:
                lambda wildcards: format_input_templates_to_be_expanded(wildcards)
            output:
                format_output_templates_to_be_expanded(node)
                # "{pre}/{stage}/{module}/{params}/{run}/{name}.txt.gz",
            params:
                parameters = node.get_parameters()
            script:
                'do_something.py'