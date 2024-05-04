import json
from typing import Any, Dict, Optional

from llama_index.core.callbacks import CBEventType
from openinference.instrumentation.llama_index._callback import (
    OpenInferenceTraceCallbackHandler,
)

from lastmile_eval.rag.debugger.tracing import get_lastmile_tracer

from ...common.utils import DEFAULT_PROJECT_NAME, LASTMILE_SPAN_KIND_KEY_NAME


class LlamaIndexCallbackHandler(OpenInferenceTraceCallbackHandler):
    """
    This is a callback handler for automatically instrumenting with
    LLamaIndex. Here's how to use it:

    ```
    from lastmile_eval.rag.debugger.tracing import LlamaIndexCallbackHandler
    llama_index.core.global_handler = LlamaIndexCallbackHandler()
    # Do regular LlamaIndex calls as usual
    ```
    """

    def __init__(self, project_name: Optional[str] = None):
        tracer = get_lastmile_tracer(
            project_name or DEFAULT_PROJECT_NAME,
        )
        super().__init__(tracer)

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        event_id = super().on_event_start(
            event_type, payload, event_id, parent_id, **kwargs
        )
        if event_id not in self._event_data:
            # OpenInferenceTraceCallbackHandler is acting on a
            # CBEventType.TEMPLATING event type that does not generate a span
            # so we should exit early and do the next one
            return event_id

        span = self._event_data[event_id].span
        span.set_attribute(LASTMILE_SPAN_KIND_KEY_NAME, event_type)

        if payload:
            serializable_payload: Dict[str, Any] = {}
            for key, value in payload.items():
                try:
                    json.dumps(value)
                except TypeError as _e:
                    serializable_value: list[Any] = []
                    if isinstance(value, list):
                        for item in value:
                            to_dict = getattr(item, "dict", None)
                            if callable(to_dict):
                                serializable_value.append(to_dict())
                        if len(serializable_value) > 0:
                            value = serializable_value
                    else:
                        to_dict = getattr(value, "dict", None)
                        if callable(to_dict):
                            value = to_dict()

                value_as_json_str: str
                try:
                    value_as_json_str = json.dumps(value)
                    # self._tracer.register_param(key, value, span=span)
                except TypeError as e:
                    # TODO: Change to logger.warning()
                    # print(f"Error serializing value: {e}")
                    value_as_json_str = f"Error serializing LlamaIndex payload value: {repr(e)}"
                    # print("yo yo ma: not serializable: ")
                    # print(f"{event_type=}")
                    # print(f"{key=}")
                    # print(f"{value=}")
                    # print()
                    # pass
                finally:
                    self._tracer.register_param(
                        key, value_as_json_str, span=span
                    )
                    serializable_payload[key] = value_as_json_str
            self._tracer.add_rag_event(
                event_type, serializable_payload, span=span
            )
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        # Add logic here like saving RAGEvent to our table
        super().on_event_end(event_type, payload, event_id, **kwargs)
        return
