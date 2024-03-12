from src.converter.converter import SnakemakeConverterTrait


class BenchmarkConverter(SnakemakeConverterTrait):
    def __init__(self, benchmark):
        self.benchmark = benchmark

    def get_benchmark_definition(self):
        return self.benchmark

    def get_benchmark_stages(self):
        raise NotImplementedError("Method not implemented yet")

    def get_modules_by_stage(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_implicit_inputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_explicit_inputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_stage_outputs(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_modules_by_stage(self, stage):
        raise NotImplementedError("Method not implemented yet")

    def get_module_excludes(self, module):
        raise NotImplementedError("Method not implemented yet")

    def get_module_parameters(self, module):
        raise NotImplementedError("Method not implemented yet")

