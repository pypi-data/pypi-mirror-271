from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rich.console import Console

from .base_model import _BedrockModel

if TYPE_CHECKING:
    from botocore.config import Config

logger = logging.getLogger()

console = Console()


class _Claude3(_BedrockModel):
    model_params = {  # noqa: RUF012
        "max_tokens": 2000,
        "temperature": 1,
        "top_k": 250,
        "top_p": 0.999,
        "stop_sequences": ["\n\nHuman:"],
        "anthropic_version": "bedrock-2023-05-31",
    }

    def _create_invoke_body(self) -> dict:
        return {
            "messages": self.messages,
        }

    def _handle_response(self, body: dict) -> str:
        response_message = body["content"][0]

        if response_message["type"] != "text":
            raise RuntimeError("Unexpected response type to prompt: " + response_message["type"])

        return response_message["text"]

    def __init__(self, boto_config: None | Config = None) -> None:
        super().__init__(
            boto_config=boto_config,
        )


class Claude3Sonnet(_Claude3):
    name = "Claude-3-Sonnet"

    def __init__(self, boto_config: None | Config = None) -> None:
        self._model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

        super().__init__(
            boto_config=boto_config,
        )


class Claude3Haiku(_Claude3):
    name = "Claude-3-Haiku"

    def __init__(self, boto_config: None | Config = None) -> None:
        self._model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        super().__init__(
            boto_config=boto_config,
        )
