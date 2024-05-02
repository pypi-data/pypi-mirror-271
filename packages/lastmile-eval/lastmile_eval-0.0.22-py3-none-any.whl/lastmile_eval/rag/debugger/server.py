import dataclasses
import json
import logging
from textwrap import dedent

import uvicorn
from result import Err, Ok, Result

from lastmile_eval.rag.debugger.app import CLIENT_DIR, get_request
from lastmile_eval.rag.debugger.app_utils import (
    AppState,
    LaunchConfig,
    ServerMode,
    run_frontend_server_background,
    update_app_state_from_launch_config,
)

logger = logging.getLogger(__name__)
logging.basicConfig()


def serve(launch_config: LaunchConfig) -> Result[str, str]:
    should_reload = launch_config.server_mode != "PROD"
    app_state = update_app_state_from_launch_config(launch_config, AppState())

    # TODO: un-jank this (do it in memory)
    with open("initial_app_state.json", "w") as f:
        f.write(json.dumps(dataclasses.asdict(app_state), indent=2))
        logger.debug(f"Wrote initial app state to initial_app_state.json")

    if launch_config.server_mode == ServerMode.DEBUG:
        run_frontend_server_background(CLIENT_DIR)

    resp = get_request(
        "tokens/list",
        launch_config.server_mode,
        app_state.lastmile_api_token,
    )
    if "status" in resp and resp["status"] != 200:
        return Err(
            dedent(
                f"""
                LastMile token did not work. Please double check:
                * your .env
                * your LastMile account (https://lastmileai.dev/settings?page=tokens)
                    You can create a new token if necessary.

                LastMile server returned:
                {resp}
                """
            )
        )
    else:
        logger.info("Token is good. Starting server.")

        uvicorn.run(
            "lastmile_eval.rag.debugger.app:app",
            port=launch_config.server_port,
            log_level=logger.level,
            reload=should_reload,
        )

        return Ok("Stopped serving.")
