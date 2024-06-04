import os

from src.workflow.snakemake import scripts
from src.workflow.snakemake.format import formatter


def create_node_rule(benchmark, node):
    if node.is_initial():
        return _create_initial_node(node)
    else:
        return _create_intermediate_node(benchmark, node)


def _create_initial_node(node):
    stage_id = node.stage_id
    module_id = node.module_id
    param_id = node.param_id

    rule:
        name: f"{{stage}}_{{module}}_{{param}}".format(stage=stage_id,module=module_id,param=param_id)
        wildcard_constraints:
            stage=stage_id,
            module=module_id,
            params=param_id,
            name=module_id
        output:
            formatter.format_output_templates_to_be_expanded(node),
        params:
            parameters = node.get_parameters(),
        script: os.path.join(os.path.dirname(os.path.realpath(scripts.__file__)), 'run_module.py')


def _create_intermediate_node(benchmark, node):
    stage_id = node.stage_id
    module_id = node.module_id
    param_id = node.param_id

    outputs = node.get_outputs()

    post = stage_id + '/' + module_id
    if any(['{params}' in o for o in outputs]):
        post += '/' + param_id

    rule:
        name: f"{{stage}}_{{module}}_{{param}}".format(stage=stage_id,module=module_id,param=param_id)
        wildcard_constraints:
            post=post,
            stage=stage_id,
            module=module_id
        input:
            lambda wildcards: formatter.format_input_templates_to_be_expanded(benchmark, wildcards)
        output:
            formatter.format_output_templates_to_be_expanded(node)
        params:
            parameters = node.get_parameters()
        script: os.path.join(os.path.dirname(os.path.realpath(scripts.__file__)), 'run_module.py')