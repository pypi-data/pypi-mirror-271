import llama_index.core

from lastmile_eval.rag.debugger.tracing.auto_instrumentation import (
    LlamaIndexCallbackHandler,
)

llama_index.core.global_handler = LlamaIndexCallbackHandler()

# # P1: Overriding of current tracer provider is not allowed --> check if already
# # set

import os
import dotenv
from getpass import getpass

dotenv.load_dotenv()
if os.getenv("OPENAI_API_KEY") is None:
    os.environ["OPENAI_API_KEY"] = getpass(
        "Paste your OpenAI key from:"
        " https://platform.openai.com/account/api-keys\n"
    )
assert os.getenv("OPENAI_API_KEY", "").startswith(
    "sk-"
), "This doesn't look like a valid OpenAI API key"
print("OpenAI API key configured")
