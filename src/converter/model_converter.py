from src.converter.converter import SnakemakeConverterTrait
from src.helpers import merge_dict_list


class BenchmarkConverter(SnakemakeConverterTrait):
    def __init__(self, benchmark):
        self.benchmark = benchmark

    def get_benchmark_definition(self):
        return self.benchmark

    def get_benchmark_stages(self):
        return dict([(x.id, x) for x in self.benchmark.steps])

    def get_benchmark_stage(self, stage_id):
        stages = self.get_benchmark_stages()
        return [stage for stage in stages if stage.id == stage_id]

    def get_modules_by_stage(self, stage):
        return dict([(x.id, x) for x in stage.members])

    def get_stage_implicit_inputs(self, stage):
        if stage.initial:
            return None

        return [input.entries for input in stage.inputs]

    def get_stage_explicit_inputs(self, stage):
        implicit = self.get_stage_implicit_inputs(stage)
        explicit = implicit
        if implicit is not None:
            all_stages = self.get_benchmark_stages()
            all_stages_outputs = [self.get_stage_outputs(stage=stage_id) for stage_id in all_stages]
            all_stages_outputs = merge_dict_list(all_stages_outputs)

            for i in range(len(implicit)):
                explicit[i] = {key: None for key in implicit[i]}

                for in_deliverable in implicit[i]:
                    # beware stage needs to be substituted
                    curr_output = all_stages_outputs[in_deliverable]

                    explicit[i][in_deliverable] = curr_output

        return explicit

    def get_stage_outputs(self, stage):
        if isinstance(stage, str):
            stage = self.get_benchmark_stages()[stage]

        if stage.terminal:
            return None

        return dict([(output.id, output.path) for output in stage.outputs])

    def get_module_excludes(self, module):
        return module.exclude

    def get_module_parameters(self, module):
        params = None
        if module.parameters is not None:
            params = [x.values for x in module.parameters]

        return params

    def is_initial(self, stage):
        if stage.initial:
            return stage.initial
        else:
            return False

    def is_terminal(self, stage):
        if stage.terminal:
            return stage.terminal
        else:
            return False

