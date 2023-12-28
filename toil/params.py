import itertools

import attr, attrs
import numpy

from typeguard import typechecked

# hardcoded for demo - the typecheck could be built at runtime by using a Factory
SPEC_TYPE=dict[str, list[int]]

@typechecked
def spec_datatype(inst: object, attr: attr.Attribute, value: SPEC_TYPE):
    return None

def parameterFactory(**spec):
    """
    Create a combinatorial parameter space. The `grid()` method returns an iterable
    of `ParameterValue` that contains a single combination of parameters according to
    the spec.

    >>> p = parameterFactory(**{'foo': [1, 2, 3], 'bar': [10, 100]})
    >>> list(p.grid())
    [ParameterValue(foo=1, bar=10), ParameterValue(foo=1, bar=100), ParameterValue(foo=2, bar=10), ParameterValue(foo=2, bar=100), ParameterValue(foo=3, bar=10), ParameterValue(foo=3, bar=100)]
    >>> v1 = p.parameterValue(foo=1, bar=2)
    >>> v2 = p.parameterValue(foo=1, bar=2)
    >>> v1 == v2
    True
    >>> v3 = p.parameterValue(foo=1, bar=20)
    >>> v1 != v3
    True
    """
    paramClass = attrs.make_class(
        "ParameterValue",
        {name: attrs.field(factory=int) for name in spec.keys()})

    @attr.s
    class Parameters:
        _spec = attr.field(validator=spec_datatype)

        def _grid(self):
            return itertools.product(*self._spec.values())

        def grid(self):
            return (paramClass(*vals) for vals in self._grid())

        def parameterValue(self, **kw):
            return paramClass(**kw)

    return Parameters(spec)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
