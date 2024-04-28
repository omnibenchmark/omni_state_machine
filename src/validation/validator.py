from collections import Counter

from src.validation import ValidationError


class Validator:
    """Simple validator class for Benchmark."""

    def __init__(self):
        self.errors = []

    def validate(self, benchmark_converter):

        # Validate ids are unique
        stage_ids = benchmark_converter.get_stage_ids()
        duplicate_stage_ids = Validator.find_duplicate(stage_ids)
        if duplicate_stage_ids:
            self.errors.append(ValidationError(f"Found duplicate stage ids: {', '.join(duplicate_stage_ids)}"))

        module_ids = benchmark_converter.get_module_ids()
        duplicate_module_ids = Validator.find_duplicate(module_ids)
        if duplicate_module_ids:
            self.errors.append(ValidationError(f"Found duplicate module ids: {', '.join(duplicate_module_ids)}"))

        output_ids = benchmark_converter.get_output_ids()
        duplicate_output_ids = Validator.find_duplicate(output_ids)
        if duplicate_output_ids:
            self.errors.append(ValidationError(f"Found duplicate output ids: {', '.join(duplicate_output_ids)}"))

        for stage_id in benchmark_converter.get_benchmark_stages():
            stage_inputs_set = benchmark_converter.get_stage_implicit_inputs(stage_id)
            for stage_inputs in stage_inputs_set:
                for stage_input_id in stage_inputs:
                    if stage_input_id not in output_ids:
                        self.errors.append(ValidationError(f"Input with id '{stage_input_id}' in stage '{stage_id}' is not valid"))

        # Raise ValidationError if there are errors
        if self.errors:
            raise ValidationError(self.errors)
        else:
            return benchmark_converter

    @staticmethod
    def find_duplicate(ids):
        id_counts = Counter(ids)
        duplicate_ids = [id for id, count in id_counts.items() if count > 1]

        return duplicate_ids
