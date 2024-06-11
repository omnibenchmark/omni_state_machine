import re
from typing import List, Set, Tuple

from src.model import BenchmarkNode, Benchmark


def format_output_templates_to_be_expanded(node: BenchmarkNode):
    """Formats node outputs that will be expanded according to Snakemake's engine"""

    outputs = node.get_outputs()
    is_initial = node.is_initial()

    if not is_initial:
        outputs = [re.sub(r'\/.*\/', '/{post}/', o, count=1) for o in outputs]

    # print(f'Output: {node.stage_id}: {outputs}')
    return outputs


def format_input_templates_to_be_expanded(benchmark: Benchmark, wildcards):
    """Formats benchmark inputs that will be expanded according to Snakemake's engine"""

    pre = wildcards.pre
    post = wildcards.post
    name = wildcards.name

    nodes = benchmark.get_nodes()
    stage_ids = set([node.stage_id for node in nodes])

    pre_stages = _extract_stages_from_path(pre, stage_ids)
    after_stage = pre_stages[-1][0] if len(pre_stages) > 0 else None

    stage_id, module_id, param_id = _match_node_format(post)

    node_hash = hash(BenchmarkNode.to_id(stage_id, module_id, param_id, after_stage))
    matching_node = next((node for node in nodes if hash(node) == node_hash), None)
    assert matching_node is not None

    node_inputs = matching_node.get_inputs()

    inputs = _match_inputs(node_inputs, pre_stages, pre, name)

    # print(f'Inputs: {stage_id} {module_id} {param_id}: {inputs}')
    return inputs


def _extract_stages_from_path(path: str, known_stage_ids: Set[str]):
    parts = path.split('/')
    stages = []

    i = 1
    while i < len(parts) - 1:
        if parts[i] in known_stage_ids:
            j = i+1

            while j < len(parts) and parts[j] not in known_stage_ids:
                j += 1

            sub_parts = parts[i:j]

            assert 2 <= len(sub_parts) <= 4
            stages.append(tuple(sub_parts))
            i = j
        else:
            i += 1

    return stages


def _match_node_format(to_match: str):
    if type(to_match) is str:
        to_match = to_match.split('/')

    stage_id = to_match[0]
    module_id = to_match[1]
    if len(to_match) == 2:
        param_id = 'default'
    else:
        param_id = to_match[2]

    return stage_id, module_id, param_id


def _match_input_module(input: str, stages: List[Tuple[str]], name: str):
    expected_input_module = input.split('{pre}/')[1].split('/{module}')[0]
    matching_stage = next((tup for tup in stages if tup[0] == expected_input_module), None)

    if matching_stage:
        matched_module = matching_stage[1]

        input = input.replace('{module}', matched_module)
        input = input.replace('{name}', name)
        if '{params}' in input:
            matched_params = next((x for x in matching_stage[2:] if 'param' or 'default' in x), None)
            input = input.replace('{params}', matched_params)

        return input
    else:
        print(f'Could not find matching stage for {input} in {stages}')
        return None


def _match_input_prefix(input: str, pre: str):
    stage = f'/{input.split("/")[1]}'
    matched_prefix = pre.split(stage)[0]
    formatted_input = input.format(pre=matched_prefix)

    # print(f'Input: {input} Prefix: {pre} Formatted: {formatted_input}')
    return formatted_input


def _match_inputs(inputs: List[str], stages: List[Tuple[str]], pre: str, name: str):
    all_matched = True

    formatted_inputs = []
    for input in inputs:
        formatted_input = _match_input_module(input, stages, name)
        if not formatted_input:
            all_matched = False
            break
        else:
            formatted_input = _match_input_prefix(formatted_input, pre)
            formatted_inputs.append(formatted_input)

    return formatted_inputs if all_matched else []
