import dataclasses
import json
import logging
import os
from typing import Any
from urllib.parse import urlencode

import requests
import lastmile_utils.lib.core.api as core_utils
from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from result import Err, Ok

import lastmile_eval.rag.debugger.prompt_iteration.run_user_llm_script as lib_run_user_llm_script
from lastmile_eval.rag.debugger.app_utils import (
    AppState,
    ServerMode,
    get_lastmile_endpoint,
)
from lastmile_eval.rag.debugger.common import core

logger = logging.getLogger(__name__)
logging.basicConfig()


app = FastAPI()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.join(THIS_DIR, "client")
BUILD_DIR = os.path.join(CLIENT_DIR, "build")
STATIC_DIR = os.path.join(BUILD_DIR, "static")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=BUILD_DIR)


origins = [
    "http://localhost:3001",  # dev client
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app_state = None


class EvaluationTestCaseData(core_utils.Record):
    # TODO: Why is this erroring?
    # query: core_utils.JSONValue
    # context: core_utils.JSONValue | None = None
    # fullyResolvedPrompt: core_utils.JSONValue | None = None
    # output: core_utils.JSONValue | None = None
    # groundTruth: core_utils.JSONValue | None = None
    # metadata: core_utils.JSONObject | None = None
    # ragQueryTraceId: str | None = None
    query: str | list[str] | dict[str, Any]
    context: str | list[str] | dict[str, Any] | None = None
    fullyResolvedPrompt: str | list[str] | dict[str, Any] | None = None
    output: str | list[str] | dict[str, Any] | None = None
    groundTruth: str | list[str] | dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    ragQueryTraceId: str | None = None


def read_global_app_state():
    try:
        # TODO: un-jank this (do it in memory)
        with open("initial_app_state.json", "r") as f:
            contents = f.read()
            # print(f"Contents: {contents}")
            loaded = json.loads(contents)
            # print(f"Loaded: {loaded}")
            app_state = AppState(**loaded)
            logger.info(f"Loaded initial app state from json file")
            return app_state
    except Exception as e:
        logger.error(f"Failed to load initial app state: {e}")

        return AppState()


def get_app_state() -> AppState:
    global app_state
    if app_state is None:
        app_state = read_global_app_state()

    return app_state


def get_request(
    api_route: str, server_mode: ServerMode, lastmile_api_token: core.APIToken
):
    """
    Make a GET request to the lastmile API for given route.
    """

    global app_state
    res = requests.get(
        get_lastmile_endpoint(api_route, server_mode),
        headers={"Authorization": f"Bearer {lastmile_api_token}"},
        timeout=30,
    )
    return res.json()


def post_request(
    api_route: str,
    data: dict[str, Any],
    server_mode: ServerMode,
    lastmile_api_token: core.APIToken,
):
    """
    Make a POST request to the lastmile API for given route.
    """

    global app_state
    res = requests.post(
        get_lastmile_endpoint(api_route, server_mode),
        headers={
            "Authorization": f"Bearer {lastmile_api_token}",
            "Content-Type": "application/json",
        },
        json=data,
        timeout=30,
    )
    return res.json()


def put_request(
    api_route: str,
    data: dict[str, Any],
    server_mode: ServerMode,
    lastmile_api_token: core.APIToken,
):
    """
    Make a POST request to the lastmile API for given route.
    """

    global app_state
    res = requests.put(
        get_lastmile_endpoint(api_route, server_mode),
        headers={
            "Authorization": f"Bearer {lastmile_api_token}",
            "Content-Type": "application/json",
        },
        json=data,
        timeout=30,
    )
    return res.json()


@app.get("/app_state")
def test_app_state(app_state: AppState = Depends(get_app_state)):
    """
    Get the current app state.
    """
    return {"state": dataclasses.asdict(app_state)}


@app.get("/api/evaluation_sets/list")
def list_evaluation_sets(
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
    app_state: AppState = Depends(get_app_state),
):
    """
    List evaluation sets.
    """
    params = {
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"evaluation_sets/list?{encoded_params}"

    return get_request(
        api_route, app_state.server_mode, app_state.lastmile_api_token
    )


@app.get("/api/evaluation_test_cases/list")
def list_evaluation_test_cases(
    evaluationSetId: str | None = None,
    testSetId: str | None = None,
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
    app_state: AppState = Depends(get_app_state),
):
    """
    List evaluation test cases.
    """
    params = {
        "evaluationSetId": evaluationSetId,
        "testSetId": testSetId,
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"evaluation_test_cases/list?{encoded_params}"

    return get_request(
        api_route, app_state.server_mode, app_state.lastmile_api_token
    )


class CreateTestSetsData(core_utils.Record):
    """
    Data for creating evaluation test sets.
    """

    name: str
    testCases: list[EvaluationTestCaseData]
    description: str | None = None
    orgId: str | None = None
    projectId: str | None = None
    # metadata: core_utils.JSONObject | None = None, TODO: Why is this erroring?
    metadata: dict[str, Any] | None = None


@app.post("/api/evaluation_test_sets/create")
def create_evaluation_test_sets(
    create_test_sets_data: CreateTestSetsData,
    app_state: AppState = Depends(get_app_state),
):
    """
    Create an evaluation test set.
    """
    return post_request(
        "evaluation_test_sets/create",
        create_test_sets_data.model_dump(),
        app_state.server_mode,
        app_state.lastmile_api_token,
    )


@app.get("/api/evaluation_test_sets/list")
def list_evaluation_test_sets(
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
    app_state: AppState = Depends(get_app_state),
):
    """
    List evaluation sets.
    """
    params = {
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"evaluation_test_sets/list?{encoded_params}"

    return get_request(
        api_route, app_state.server_mode, app_state.lastmile_api_token
    )


@app.get("/api/rag_ingestion_traces/list")
def list_rag_ingestion_traces(
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
    startTime: int | None = None,
    endTime: int | None = None,
    app_state: AppState = Depends(get_app_state),
):
    """
    List RAG ingestion traces.
    """
    params = {
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
        "startTime": startTime,
        "endTime": endTime,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"rag_ingestion_traces/list?{encoded_params}"

    return get_request(
        api_route, app_state.server_mode, app_state.lastmile_api_token
    )


@app.get("/api/rag_query_traces/list")
def list_rag_query_traces(
    search: str | None = None,
    pageSize: int | None = None,
    cursor: str | None = None,
    startTime: int | None = None,
    endTime: int | None = None,
    app_state: AppState = Depends(get_app_state),
):
    """
    List RAG query traces.
    """
    params = {
        "search": search,
        "pageSize": pageSize,
        "cursor": cursor,
        "startTime": startTime,
        "endTime": endTime,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    api_route = f"rag_query_traces/list?{encoded_params}"

    return get_request(
        api_route, app_state.server_mode, app_state.lastmile_api_token
    )


class CreateTraceAnnotationData(core_utils.Record):
    """
    Data for creating trace annotation.
    """

    annotation: str
    traceId: str
    orgId: str | None = None
    # metadata: core_utils.JSONObject | None = None, TODO: Why is this erroring?
    metadata: dict[str, Any] | None = None


@app.post("/api/trace_annotations/create")
def create_trace_annotation(
    create_trace_annotation_data: CreateTraceAnnotationData,
    app_state: AppState = Depends(get_app_state),
):
    """
    Create a trace annotation.
    """
    return post_request(
        "trace_annotations/create",
        create_trace_annotation_data.model_dump(),
        app_state.server_mode,
        app_state.lastmile_api_token,
    )


class UpdateTraceAnnotationData(core_utils.Record):
    """
    Data for updating trace annotation.
    """

    id: str
    annotation: str
    # metadata: core_utils.JSONObject | None = None, TODO: Why is this erroring?
    metadata: dict[str, Any] | None = None


@app.put("/api/trace_annotations/update")
def update_trace_annotation(
    update_trace_annotation_data: UpdateTraceAnnotationData,
    app_state: AppState = Depends(get_app_state),
):
    """
    Update a trace annotation
    """
    return put_request(
        "trace_annotations/update",
        update_trace_annotation_data.model_dump(),
        app_state.server_mode,
        app_state.lastmile_api_token,
    )


@app.get("/api/trace/read")
def get_trace(
    id: str | None = None,
    app_state: AppState = Depends(get_app_state),
):
    """
    Get an OTEL trace by ID.
    """
    return get_request(
        f"trace/read?id={id}",
        app_state.server_mode,
        app_state.lastmile_api_token,
    )


class PromptContainer(BaseModel):
    prompt: str


@app.post("/api/run_user_llm_script")
def run_user_llm_script(
    prompt_container: PromptContainer,
    response: Response,
    app_state: AppState = Depends(get_app_state),
):
    """
    Run the user LLM script.
    """

    script_path = app_state.run_llm_script_path
    logger.debug(f"Script path: {script_path}")
    if script_path is None:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "No script path configured. Please rerun app with --help."
        }

    logger.info("Running user LLM script")
    config = lib_run_user_llm_script.RunUserLLMScriptconfig(
        executable=script_path,
        timeout_s=app_state.run_llm_script_timeout_s,
    )

    script_response = lib_run_user_llm_script.run_user_llm_script(
        config, prompt_container.prompt
    )

    match script_response:
        case Ok(response_):
            return {"response": response_}
        case Err(error):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message": error}


# Defines a route handler for `/*` essentially.
# NOTE: this needs to be the last route defined b/c it's a catch all route
@app.get("/{rest_of_path:path}")
async def react_app(
    req: Request, app_state: AppState = Depends(get_app_state)
):
    """
    Serve the frontend react app (DEBUG ONLY).
    """
    if app_state.server_mode == ServerMode.DEBUG:  # type: ignore
        return {
            "message": "Not serving bundle in DEBUG mode, use yarn start in client/"
        }
    return templates.TemplateResponse("index.html", {"request": req})
