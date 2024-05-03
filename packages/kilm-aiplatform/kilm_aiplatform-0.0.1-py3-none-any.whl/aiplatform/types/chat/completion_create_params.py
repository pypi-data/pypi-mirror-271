# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from ..chat_model import ChatModel
from .chat_completion_message_param import ChatCompletionMessageParam

__all__ = [
    "CompletionCreateParamsBase",
    "CompletionCreateParamsNonStreaming",
    "CompletionCreateParamsStreaming",
]


class CompletionCreateParamsBase(TypedDict, total=False):
    messages: Required[Iterable[ChatCompletionMessageParam]]
    """A list of messages comprising the conversation so far.

    [Example Python code](https://cookbook.aiplatform.com/examples/how_to_format_inputs_to_chatgpt_models).
    """

    model: Required[Union[str, ChatModel]]
    """ID of the model to use.

    See the
    [model endpoint compatibility](https://platform.aiplatform.com/docs/models/model-endpoint-compatibility)
    table for details on which models work with the Chat API.
    """

    max_tokens: Optional[int]
    """
    The maximum number of [tokens](/tokenizer) that can be generated in the chat
    completion.

    The total length of input tokens and generated tokens is limited by the model's
    context length.
    [Example Python code](https://cookbook.aiplatform.com/examples/how_to_count_tokens_with_tiktoken)
    for counting tokens.
    """

    seed: Optional[int]
    """
    This feature is in Beta. If specified, our system will make a best effort to
    sample deterministically, such that repeated requests with the same `seed` and
    parameters should return the same result. Determinism is not guaranteed, and you
    should refer to the `system_fingerprint` response parameter to monitor changes
    in the backend.
    """

    stop: Union[Optional[str], List[str]]
    """Up to 4 sequences where the API will stop generating further tokens."""

    temperature: Optional[float]
    """What sampling temperature to use, between 0 and 2.

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic.

    We generally recommend altering this or `top_p` but not both.
    """

    top_p: Optional[float]
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered.

    We generally recommend altering this or `temperature` but not both.
    """


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase):
    stream: Optional[Literal[False]]
    """If set, partial message deltas will be sent, like in ChatGPT.

    Tokens will be sent as data-only
    [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
    as they become available, with the stream terminated by a `data: [DONE]`
    message.
    [Example Python code](https://cookbook.aiplatform.com/examples/how_to_stream_completions).
    """


class CompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """If set, partial message deltas will be sent, like in ChatGPT.

    Tokens will be sent as data-only
    [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
    as they become available, with the stream terminated by a `data: [DONE]`
    message.
    [Example Python code](https://cookbook.aiplatform.com/examples/how_to_stream_completions).
    """


CompletionCreateParams = Union[CompletionCreateParamsNonStreaming, CompletionCreateParamsStreaming]
