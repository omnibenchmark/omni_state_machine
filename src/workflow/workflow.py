import os.path

from src.model import Benchmark, BenchmarkNode


class WorkflowEngine:
    """Interface for the workflow engine."""

    def run_workflow(self, benchmark: Benchmark, cores: int = 1, dryrun: bool = False, work_dir: str = os.getcwd(), **kwargs):
        """
        Serializes & runs benchmark workflow.

        Args:
            benchmark (Benchmark): benchmark to run
            cores (int): number of cores to run
            dryrun (bool): validate the workflow with the benchmark without actual execution
            work_dir (str): working directory
            **kwargs: keyword arguments to pass to the workflow engine

        Returns:
        - Status code of the workflow run.
        """
        raise NotImplementedError("Method not implemented yet")

    def serialize_workflow(self, benchmark: Benchmark, output_dir: str = os.getcwd()):
        """
        Serializes a workflow file for the benchmark.

        Args:
            benchmark (Benchmark): benchmark to serialize
            output_dir (str): output directory for the workflow file

        Returns:
        - Workflow file path.
        """
        raise NotImplementedError("Method not implemented yet")

    def run_node_workflow(self, node: BenchmarkNode, cores: int = 1, dryrun: bool = False, work_dir: str = os.getcwd(), **kwargs):
        """
        Serializes & runs benchmark node workflow.

        Args:
            node (Benchmark): benchmark node to run
            cores (int): number of cores to run
            dryrun (bool): validate the workflow with the benchmark without actual execution
            work_dir (str): working directory
            **kwargs: keyword arguments to pass to the workflow engine

        Returns:
        - Status code of the workflow run.
        """
        raise NotImplementedError("Method not implemented yet")

    def serialize_node_workflow(self, node: BenchmarkNode, output_dir: str = os.getcwd()):
        """
        Serializes a workflow file for a benchmark node.

        Args:
            node (BenchmarkNode): benchmark node to serialize
            output_dir (str): output directory for the workflow file

        Returns:
        - Workflow file path.
        """
        raise NotImplementedError("Method not implemented yet")

