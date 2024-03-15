import re

## f-strings: rule maker
## wildcards: output mapper (only params, currently)
# def format_dataset_templates_to_be_expanded(dataset):
#     filled = []
#     for stage in self.config['steps'].keys():
#         if 'initial' in self.config['steps'][stage].keys() and self.config['steps'][stage]['initial']:
#              outs = list(get_stage_outputs(stage).values())
#              for i in range(len(outs)):
#                  filled.append([outs[i].format(stage = stage, module = dataset, params = '{params}', name = dataset)])

#     return(sum(filled, []))
# def format_dataset_templates_to_be_expanded(converter, dataset_id):
#     filled = []
#     stages = converter.get_benchmark_stages()
#     for stage_id in stages:
#         stage = stages[stage_id]
#         if converter.is_initial(stage):
#             outs = list(converter.get_stage_outputs(stage).values())
#             for i in range(len(outs)):
#                 filled.append([outs[i].format(
#                     input_dirname='{pre}',
#                     stage=stage_id,
#                     module=dataset_id,
#                     params='{params}',
#                     name=dataset_id)])
#
#     return sum(filled, [])


## f-strings: rule maker
## wildcards (single curly bracket): expanded from the output mapper
def format_output_templates_to_be_expanded(converter, stage_id, module_id, param_id, name=None, initial=False):
    input_dirname = 'out' if initial else '{pre}'
    name = name if name else '{name}'
    o = [x.format(input_dirname=input_dirname,
                  stage=stage_id,
                  module=module_id,
                  params=param_id,
                  name=name) for x in converter.get_stage_outputs(stage_id).values()]

    print(f'Output: {stage_id} {module_id} {param_id}: {o}')
    return o


def format_input_templates_to_be_expanded(converter, all_paths, wildcards, stage_id, module_id, param_id):
    o = []

    for x in converter.get_stage_explicit_inputs(stage_id).values():
        prefix = wildcards.pre
        name = wildcards.name

        x = x.format(input_dirname='{pre}',
                     stage='{stage}',
                     module='{module}',
                     params='{params}',
                     name=name)

        # Transform to regular expression pattern
        #pattern = re.sub(r'\{pre\}', r'(.*)', x)
        #pattern = re.sub(r'\{module\}', r'([^\/]+)', pattern)
        #pattern = re.sub(r'\{params\}', r'([^\/]+)', pattern)

        # Compile the pattern into a regular expression object
        #regex = re.compile(pattern)

        # Match file paths based on the pattern
        #matched_files = [path for path in all_paths if regex.match(path) and (len(path) < len(prefix) or path.startswith(prefix))]
        #o.extend(matched_files)



    print(f'Pre: {wildcards}')
    print(f'Input: {stage_id} {module_id} {param_id}: {o}')
    return '{pre}/data/{module}/{params}/{name}.txt.gz'
