import inspect
import sys
from contextlib import AbstractContextManager
from typing import Mapping, Any, Type

from hgraph._types import AUTO_RESOLVE, TS, TSB, TS_SCHEMA, SCALAR, SCALAR_1, TIME_SERIES_TYPE, REF, STATE, HgREFTypeMetaData
from hgraph._wiring._wiring_port import WiringPort
from hgraph._wiring._wiring_node_class import BaseWiringNodeClass, create_input_output_builders
from hgraph._wiring._decorators import graph, sink_node, pull_source_node
from hgraph._runtime._global_state import GlobalState

__all__ = ('TimeSeriesContextTracker',)


def findclass(func):
    cls = sys.modules.get(func.__module__)
    if cls is None:
        return None
    for name in func.__qualname__.split('.')[:-1]:
        if name == '<locals>':
            raise ValueError('Local classes are not supported for time series context managers')
        cls = getattr(cls, name)
    if not inspect.isclass(cls):
        raise ValueError(f'failed to find class for context manager function {func}')
    return cls


def get_context_manager_base(tp):
    if (enter := getattr(tp, '__enter__', None)) and (exit := getattr(tp, '__exit__', None)):
        if tp.__mro__.index(enter_class := findclass(enter)) < tp.__mro__.index(exit_class := findclass(exit)):
            return exit_class
        else:
            return enter_class
    else:
        return None


class TimeSeriesContextTracker(AbstractContextManager):
    __instance__ = None
    __counter__ = 0

    def __init__(self):
        self.contexts: list[tuple[WiringPort, object, int, str]] = []

    @classmethod
    def instance(cls):
        if cls.__instance__ is None:
            cls.__instance__ = cls()
        return cls.__instance__

    def __enter__(self):
        self.__instance__ = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__instance__ == self:
            self.__instance__ = None

    def enter_context(self, context, graph_scope):
        self.__counter__ += 1
        path = f"{context.output_type}-{self.__counter__}"
        capture_context(path, context)
        self.contexts.append((context, graph_scope, graph_scope.graph_nesting_depth(), path))

    def exit_context(self, context):
        self.contexts.pop()

    def find_context(self, tp, graph_scope):
        for context, scope, depth, path in reversed(self.contexts):

            if tp.is_scalar and tp.matches(context.output_type.dereference().scalar_type()):
                match = True
            elif not tp.is_scalar and tp.matches(context.output_type):
                match = True
            else:
                match = False

            if match:
                if graph_scope == scope:  # the consumer is on the same graph as the producer
                    return context
                else:
                    from hgraph import TIME_SERIES_TYPE
                    return get_context_output[TIME_SERIES_TYPE: context.output_type](path, depth - 1)
        return None

    def max_context_rank(self):
        # we are making an assumption here that the rank of the capture_output_to_global_state node
        # is always 1 higher than the rank of the context manager node
        return max(0, 0, *(c[0].rank + 1 for c in self.contexts))


@sink_node(active=tuple(), valid=tuple())
def capture_context(path: str, ts: REF[TIME_SERIES_TYPE], state: STATE = None):
    """
    This node serves to capture the output of a context node and record the output reference in the global state
    with a prefix that would allow to distinguish it from same context node wired in other branches (if created on a branch).
    """


@capture_context.start
def capture_context_start(path: str, ts: REF[TIME_SERIES_TYPE], state: STATE):
    """Place the reference into the global state"""
    source = ts.output or ts.value.output
    state.path = f"context-{source.owning_node.owning_graph_id}-{path}"
    GlobalState.instance()[state.path] = ts


@capture_context.stop
def capture_context_stop(path: str, state: STATE):
    """Clean up references"""
    del GlobalState.instance()[state.path]


class ContextNodeClass(BaseWiringNodeClass):

    def create_node_builder_instance(self, node_signature: "NodeSignature",
                                     scalars: Mapping[str, Any]) -> "NodeBuilder":
        output_type = node_signature.time_series_output
        if type(output_type) is not HgREFTypeMetaData:
            node_signature = node_signature.copy_with(time_series_output=HgREFTypeMetaData(output_type))

        from hgraph._impl._builder import PythonNodeImplNodeBuilder
        input_builder, output_builder, error_builder = create_input_output_builders(node_signature,
                                                                                    self.error_output_type)

        from hgraph._impl._runtime._node import BaseNodeImpl

        class _PythonContextStubSourceNode(BaseNodeImpl):

            def do_eval(self):
                """The service must be available by now, so we can retrieve the output reference."""
                from hgraph._runtime._global_state import GlobalState
                path = f'context-{self.owning_graph_id[:self.scalars["depth"]*2]}-{self.scalars["path"]}'
                shared_input = GlobalState.instance().get(path)
                if shared_input is None:
                    raise RuntimeError(f"Missing shared output for path: {path}")
                elif shared_input.has_peer: # it is a reference with a per so its value might update
                    output = shared_input.output
                    output.subscribe(self)
                    if self.subscribed_output is not None and self.subscribed_output is not output:
                        self.subscribed_output.unsubscribe(self)
                    self.subscribed_output = output
                # NOTE: The output needs to be a reference value output so we can set the value and continue!
                self.output.value = shared_input.value  # might be none

            def do_start(self):
                """Make sure we get notified to serve the reference"""
                self.subscribed_output = None
                self.notify()

            def do_stop(self):
                if self.subscribed_output is not None:
                    self.subscribed_output.unsubscribe(self)

        return PythonNodeImplNodeBuilder(
            signature=node_signature,
            scalars=scalars,
            input_builder=input_builder,
            output_builder=output_builder,
            error_builder=error_builder,
            node_impl=_PythonContextStubSourceNode
        )


@pull_source_node(node_impl=ContextNodeClass)
def get_context_output(path: str, depth: int) -> REF[TIME_SERIES_TYPE]:
    """Uses the special node to extract a context output from the global state."""


@graph(resolvers={SCALAR_1: lambda m, s: get_context_manager_base(m[SCALAR].py_type)})
def enter_ts_context(context: TS[SCALAR], tp: Type[SCALAR_1] = AUTO_RESOLVE) -> TS[SCALAR]:
    from hgraph._wiring._wiring_node_instance import WiringNodeInstanceContext
    TimeSeriesContextTracker.instance().enter_context(context, WiringNodeInstanceContext.instance())

    return context


@graph(overloads=enter_ts_context, resolvers={SCALAR_1: lambda m, s: get_context_manager_base(m[TS_SCHEMA].py_type.scalar_type())})
def enter_ts_context_tsb(context: TSB[TS_SCHEMA], tp: Type[SCALAR_1] = AUTO_RESOLVE) -> TSB[TS_SCHEMA]:
    from hgraph._wiring._wiring_node_instance import WiringNodeInstanceContext
    TimeSeriesContextTracker.instance().enter_context(context, WiringNodeInstanceContext.instance())

    return context


WiringPort.__enter__ = lambda s: enter_ts_context(s)


@graph  # __enter__ will have checked SCALAR is a context manager class
def exit_ts_context(context: TIME_SERIES_TYPE):
    TimeSeriesContextTracker.instance().exit_context(context)


WiringPort.__exit__ = lambda s, exc_type, exc_val, exc_tb: exit_ts_context(s)



