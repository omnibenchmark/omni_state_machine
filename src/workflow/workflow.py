import os.path

from src.model.benchmark import Benchmark


class WorkflowEngine:

    def __init__(self, benchmark: Benchmark):
        self.benchmark = benchmark

    def run_workflow(self):
        """
        Serializes & runs benchmark workflow.

        Returns:
        - Status code of the workflow run.
        """
        raise NotImplementedError("Method not implemented yet")

    def serialize_workflow(self, output_path=os.getcwd()):
        """
        Serializes a workflow file for the benchmark.

        Returns:
        - Workflow file path.
        """
        raise NotImplementedError("Method not implemented yet")

    def run_node_workflow(self, node):
        """
        Serializes & runs benchmark node's workflow.

        Returns:
        - Status code of the workflow run.
        """
        raise NotImplementedError("Method not implemented yet")

    def serialize_node_workflow(self, node, output_path=os.getcwd()):
        """
        Serializes a workflow file for a benchmark node.

        Returns:
        - Workflow file path.
        """
        raise NotImplementedError("Method not implemented yet")

