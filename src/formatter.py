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
def format_output_templates_to_be_expanded(converter, stage_id, module_id, param_id, initial=False):
    input_dirname = 'out' if initial else '{pre}'
    stage_outputs = converter.get_stage_outputs(stage_id).values()
    o = [x.format(input_dirname=input_dirname,
                  stage='{stage}',
                  module='{module}',
                  params='{param}',
                  name='{name}') for x in stage_outputs]

    if not initial:
        o = [x.replace('/{stage}/{module}/{param}/', '/{post}/') for x in o]

    print(f'Output: {stage_id} {module_id} {param_id}: {o}')
    return o


def format_input_templates_to_be_expanded(converter, stage_id, module_id, param_id):
    stage_inputs = converter.get_stage_explicit_inputs(stage_id).values()
    i = [x.format(input_dirname='{pre}',
                  stage='{stage}',
                  module='{module}',
                  params='{param}',
                  name='{name}') for x in stage_inputs]

    i = [x.replace('/{stage}/{module}/{param}/', '/') for x in i]

    print(f'Input: {stage_id} {module_id} {param_id}: {i}')
    return i
