from functools import partial, wraps
import inspect
import json


def _check_json_serializable(event):
    try:
        return json.dumps(event)
    except TypeError as e:
        raise Exception(
            f"All logged values must be JSON-serializable: {event}"
        ) from e


def _try_log_input(span, f_sig, f_args, f_kwargs):
    bound_args = f_sig.bind(*f_args, **f_kwargs).arguments
    input_serializable = bound_args
    try:
        _check_json_serializable(bound_args)
    except Exception as e:
        input_serializable = "<input not json-serializable>: " + str(e)
    span.set_attribute("input", json.dumps(input_serializable))


def _try_log_output(span, output):
    output_serializable = output
    try:
        _check_json_serializable(output)
    except Exception as e:
        output_serializable = "<output not json-serializable>: " + str(e)
    span.set_attribute("output", json.dumps(output_serializable))


def traced(tracer):

    print("tracer:", tracer)

    def decorator(f):

        f_sig = inspect.signature(f)

        @wraps(f)
        def wrapper_sync(*f_args, **f_kwargs):
            with tracer.start_as_current_span(f.__name__) as span:
                _try_log_input(span, f_sig, f_args, f_kwargs)
                ret = f(*f_args, **f_kwargs)
                _try_log_output(span, ret)
                return ret

        @wraps(f)
        async def wrapper_async(*f_args, **f_kwargs):
            with tracer.start_as_current_span(f.__name__) as span:
                _try_log_input(span, f_sig, f_args, f_kwargs)
                ret = await f(*f_args, **f_kwargs)
                _try_log_output(span, ret)
                return ret

        if inspect.iscoroutinefunction(f):
            return wrapper_async
        else:
            return wrapper_sync

    return decorator
