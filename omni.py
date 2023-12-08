# Some Class declarations

import attr

@attr.s
class Benchmark:
    """A simple class representing a Benchmark."""
    name: str = attr.ib()
    definition: str = attr.ib()

    # TODO: load stages & populate other attributes
    # TODO: fetch from remote
