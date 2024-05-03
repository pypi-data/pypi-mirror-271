# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict


__all__ = ["ChatCompletionAssistantMessageParam"]


class ChatCompletionAssistantMessageParam(TypedDict, total=False):
    role: Required[Literal["assistant"]]
    """The role of the messages author, in this case `assistant`."""

    content: Optional[str]
    """The contents of the assistant message.

    Required unless `tool_calls` or `function_call` is specified.
    """

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """
