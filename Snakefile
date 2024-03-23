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

stages = converter.get_benchmark_stages()
for node in G.nodes:
    stage_id = node.stage_id
    module_id = node.module_id
    param_id = node.param_id
    run_id = node.run_id

    stage = stages[stage_id]
    # print('stage_id is', stage_id, 'and module_id is', module_id, 'is initial', converter.is_initial(stage))

    if converter.is_initial(stage):
        rule:
            name: f"{{stage}}_{{module}}_{{param}}_{{run}}".format(stage=stage_id,module=module_id,param=param_id,run=run_id)
            wildcard_constraints:
                stage=stage_id,
                module=module_id,
                param=param_id,
                run=run_id,
                name=module_id
            output:
                format_output_templates_to_be_expanded(stage_id,initial=True)
                # "out/{stage}/{module}/{param}/{name}.txt.gz",
                # "out/{stage}/{module}/{param}/{name}.meta.json",
                # "out/{stage}/{module}/{param}/{name}_params.txt"
            params:
                parameters = node.parameters
            script:
                op.join('src','do_something.py')
    else:
        rule:
            wildcard_constraints:
                post=stage_id + '/' + module_id + '/' + param_id + '/' + run_id,
                stage=stage_id,
                module=module_id,
                name='|'.join([re.escape(x) for x in converter.get_initial_datasets()]),
            name: f"{{stage}}_{{module}}_{{param}}_{{run}}".format(stage=stage_id,module=module_id,param=param_id,run=run_id)
            input:
                lambda wildcards: format_input_templates_to_be_expanded(wildcards)
                # '{pre}/{name}.txt.gz'
            output:
                format_output_templates_to_be_expanded(stage_id)
                # "{pre}/{stage}/{module}/{param}/{name}.txt.gz",
            params:
                parameters = node.parameters
            script:
                op.join("src","do_something.py")
