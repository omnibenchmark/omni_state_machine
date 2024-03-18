
## f-strings: rule maker
## wildcards (single curly bracket): expanded from the output mapper
def format_output_templates_to_be_expanded(converter, stage_id, initial=False):
    input_dirname = 'out' if initial else '{pre}'
    stage_outputs = converter.get_stage_outputs(stage_id).values()
    o = [x.format(input_dirname=input_dirname,
                  stage='{stage}',
                  module='{module}',
                  params='{param}',
                  name='{name}') for x in stage_outputs]

    if not initial:
        o = [x.replace('/{stage}/{module}/{param}/', '/{post}/') for x in o]

    # print(f'Output: {stage_id} {module_id} {param_id}: {o}')
    return o


def extract_stages(path):
    parts = path.split('/')
    stages = []

    for i in range(len(parts) - 1, 0, -3):
        sub_parts = parts[i-2:i+1]
        stages.append(tuple(sub_parts))

    return list(reversed(stages))


def match_input_module(input, stages, name):
    # print(input)
    expected_input_module = input.split('{input_dirname}/')[1].split('/{module}')[0]
    matching_stage = next((tup for tup in stages if tup[0] == expected_input_module), None)

    if matching_stage:
        return input.format(
            input_dirname='{pre}',
            module=matching_stage[1],
            params=matching_stage[2],
            name=name,
        )
    else:
        # print(f'Could not find matching stage for {input} in {stages}')
        return None


def match_input_prefix(input, pre):
    # print(f'Input: {input} Prefix: {pre}')
    stage = f'/{input.split("/")[1]}'
    matched_prefix = pre.split(stage)[0]
    formatted_input = input.format(pre=matched_prefix)
    return formatted_input


def match_inputs(inputs, stages, pre, post, name):
    all_matched = True

    formatted_inputs = []
    for input in inputs:
        formatted_input = match_input_module(input, stages, name)
        if not formatted_input:
            all_matched = False
            break
        else:
            formatted_input = match_input_prefix(formatted_input, pre)
            formatted_inputs.append(formatted_input)

    return formatted_inputs if all_matched else []


def format_input_templates_to_be_expanded(converter, output_paths, wildcards):
    pre = wildcards.pre
    post = wildcards.post
    name = wildcards.name

    pre_stages = extract_stages(pre)

    stage_id, module_id, param_id = post.split('/')
    stage_inputs = converter.get_stage_explicit_inputs(stage_id).values()

    inputs = match_inputs(stage_inputs, pre_stages, pre, post, name)
    for i in inputs:
        assert i in output_paths

    # print(f'Inputs: {stage_id} {module_id} {param_id}: {inputs}')
    return inputs
