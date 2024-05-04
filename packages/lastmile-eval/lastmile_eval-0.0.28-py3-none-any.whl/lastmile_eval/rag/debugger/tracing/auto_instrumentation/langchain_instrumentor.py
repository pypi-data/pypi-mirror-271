import logging
from typing import Any, Callable, Collection, Type

from langchain_core.callbacks import BaseCallbackManager
from openinference.instrumentation.langchain import (
    LangChainInstrumentor as LangChainInstrumentorBase,
)
from openinference.instrumentation.langchain._tracer import OpenInferenceTracer
from openinference.instrumentation.langchain.package import _instruments
from openinference.instrumentation.langchain.version import __version__
from opentelemetry import trace as trace_api
from wrapt import wrap_function_wrapper

# TODO: Fix typing
from lastmile_eval.rag.debugger.tracing.sdk import get_lastmile_tracer

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LangChainInstrumentor(LangChainInstrumentorBase):
    """
    This is a callback handler for automatically instrumenting with
    Langchain. Here's how to use it:

    ```
    from lastmile_eval.rag.debugger.tracing.auto_instrumentation import LangChainInstrumentor
    LangChainInstrumentor().instrument()
    # Do regular LangChain calls as usual
    ```
    """

    def __init__(self) -> None:
        super().__init__()
        self._tracer = get_lastmile_tracer(
            tracer_name="my-tracer",
            initial_params={"motivation_quote": "I love staring into the sun"},
            # output_filepath=OUTPUT_FILE_PATH,
        )

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs: Any) -> None:

        wrap_function_wrapper(
            module="langchain_core.callbacks",
            name="BaseCallbackManager.__init__",
            wrapper=_BaseCallbackManagerInit(
                tracer=self._tracer, cls=OpenInferenceTracer
            ),
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        pass


class _BaseCallbackManagerInit:
    __slots__ = ("_tracer", "_cls")

    def __init__(
        self, tracer: trace_api.Tracer, cls: Type[OpenInferenceTracer]
    ):
        self._tracer = tracer
        self._cls = cls

    def __call__(
        self,
        wrapped: Callable[..., None],
        instance: BaseCallbackManager,
        args: Any,
        kwargs: Any,
    ) -> None:
        wrapped(*args, **kwargs)
        for handler in instance.inheritable_handlers:
            # Handlers may be copied when new managers are created, so we
            # don't want to keep adding. E.g. see the following location.
            # https://github.com/langchain-ai/langchain/blob/5c2538b9f7fb64afed2a918b621d9d8681c7ae32/libs/core/langchain_core/callbacks/manager.py#L1876  # noqa: E501
            if isinstance(handler, self._cls):
                break
        else:
            instance.add_handler(self._cls(tracer=self._tracer), True)
