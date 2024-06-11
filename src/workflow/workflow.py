import os.path

from src.model import Benchmark, BenchmarkNode


class WorkflowEngine:

    def run_workflow(self, benchmark: Benchmark, cores: int = 1, dryrun: bool = False, work_dir: str = os.getcwd(), **kwargs):
        """
        Serializes & runs benchmark workflow.

        Returns:
        - Status code of the workflow run.
        """
        raise NotImplementedError("Method not implemented yet")

    def serialize_workflow(self, benchmark: Benchmark, output_dir: str = os.getcwd()):
        """
        Serializes a workflow file for the benchmark.

        Returns:
        - Workflow file path.
        """
        raise NotImplementedError("Method not implemented yet")

    def run_node_workflow(self, node: BenchmarkNode, cores: int = 1, dryrun: bool = False, work_dir: str = os.getcwd(), **kwargs):
        """
        Serializes & runs benchmark node's workflow.

        Returns:
        - Status code of the workflow run.
        """
        raise NotImplementedError("Method not implemented yet")

    def serialize_node_workflow(self, node: BenchmarkNode, output_dir: str = os.getcwd()):
        """
        Serializes a workflow file for a benchmark node.

        Returns:
        - Workflow file path.
        """
        raise NotImplementedError("Method not implemented yet")

