import os.path

from src.model.benchmark import Benchmark


class WorkflowEngine:

    def __init__(self, benchmark: Benchmark):
        self.benchmark = benchmark

    def run_workflow(self):
        raise NotImplementedError("Method not implemented yet")

    def serialize_workflow(self, output_path=os.getcwd()):
        raise NotImplementedError("Method not implemented yet")

    def run_node_workflow(self, node):
        raise NotImplementedError("Method not implemented yet")

    def serialize_node_workflow(self, node, output_path=os.getcwd()):
        raise NotImplementedError("Method not implemented yet")

