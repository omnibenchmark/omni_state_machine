
class BenchmarkNode:
    def __init__(self, converter,
                 stage, module, parameters,
                 inputs, outputs,
                 param_id):

        self.converter = converter
        self.stage = stage
        self.module = module
        self.parameters = parameters
        self.inputs = inputs
        self.outputs = outputs

        self.stage_id = converter.get_stage_id(stage)
        self.module_id = converter.get_module_id(module)
        self.param_id = f'param_{param_id}' if parameters else 'default'

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

    def get_parameters(self):
        return self.parameters

    def is_initial(self):
        return self.converter.is_initial(self.stage)

    def __str__(self):
        return f"BenchmarkNode({self.stage_id}, {self.module_id}, {self.param_id})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, BenchmarkNode):
            return (self.stage_id, self.module_id, self.parameters, self.inputs) == \
                   (other.stage_id, other.module_id, other.parameters, other.inputs)
        return False

    def __hash__(self):
        return hash((self.stage_id, self.module_id, self.param_id))
