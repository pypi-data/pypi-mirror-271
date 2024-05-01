# cntrlai/openai.py

import logging
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional, Union, cast

import nanoid
from cntrlai.logger import BaseContextTracer

from cntrlai.types import (
    ChatMessage,
    ErrorCapture,
    SpanInputOutput,
    SpanMetrics,
    TraceMetadata,
    TypedValueChatMessages,
    TypedValueText,
    SpanParams,
    SpanTimestamps,
    LLMSpan,
)
from cntrlai.utils import (
    capture_async_chunks_with_timings_and_reyield,
    capture_chunks_with_timings_and_reyield,
    capture_exception,
    milliseconds_timestamp,
    safe_get,
)

from openai import (
    AsyncStream,
    OpenAI,
    AsyncOpenAI,
    Stream,
    AzureOpenAI,
    AsyncAzureOpenAI,
)

from openai.types import Completion
from openai.types.chat import ChatCompletion, ChatCompletionChunk

logger = logging.getLogger("chainlit")

class BasicLoggerOpenAI(BaseContextTracer):
    """
    Tracing for both Completion and ChatCompletion endpoints
    """

    def __init__(
        self,
        instance: Union[OpenAI, AsyncOpenAI],
        trace_id: Optional[str] = None,
        metadata: Optional[TraceMetadata] = None,
    ):
        super().__init__(
            trace_id=trace_id,
            metadata=metadata,
        )
        trace_id = self.trace_id
        self.completion_tracer = OpenAICompletionTracer(
            instance=instance, trace_id=trace_id, metadata=metadata
        )
        self.chat_completion_tracer = OpenAIChatCompletionTracer(
            instance=instance, trace_id=trace_id, metadata=metadata
        )

    def __enter__(self):
        super().__enter__()
        self.completion_tracer.__enter__()
        self.chat_completion_tracer.__enter__()
        logger.info("Entered BasicLoggerOpenAI")

    def __exit__(self, _type, _value, _traceback):
        super().__exit__(_type, _value, _traceback)
        self.completion_tracer.__exit__(_type, _value, _traceback)
        self.chat_completion_tracer.__exit__(_type, _value, _traceback)
        logger.info("Exited BasicLoggerOpenAI")


class AzureOpenAITracer(BasicLoggerOpenAI):
    """
    Tracing for both Completion and ChatCompletion endpoints
    """

    def __init__(
        self,
        instance: Union[AzureOpenAI, AsyncAzureOpenAI],
        trace_id: Optional[str] = None,
        metadata: Optional[TraceMetadata] = None,
    ):
        super().__init__(
            instance=instance,
            trace_id=trace_id,
            metadata=metadata,
        )
        logger.info("Initialized AzureOpenAITracer")


class OpenAICompletionTracer(BaseContextTracer):
    def __init__(
        self,
        instance: Union[OpenAI, AsyncOpenAI, AzureOpenAI, AsyncAzureOpenAI],
        trace_id: Optional[str] = None,
        metadata: Optional[TraceMetadata] = None,
    ):
        self.instance = instance
        super().__init__(
            trace_id=trace_id,
            metadata=metadata,
        )
        logger.info("Initialized OpenAICompletionTracer")

    def __enter__(self):
        super().__enter__()
        self.instance.completions._original_create = self.instance.completions.create  # type: ignore
        if isinstance(self.instance, AsyncOpenAI):
            self.instance.completions.create = self.patched_completion_acreate  # type: ignore
        else:
            self.instance.completions.create = self.patched_completion_create  # type: ignore
        logger.info("Entered OpenAICompletionTracer")

    def __exit__(self, _type, _value, _traceback):
        super().__exit__(_type, _value, _traceback)
        self.instance.completions.create = self.instance.completions._original_create  # type: ignore
        logger.info("Exited OpenAICompletionTracer")

    def patched_completion_create(self, *args, **kwargs):
        started_at = milliseconds_timestamp()
        logger.info(f"Patched completion create started at: {started_at}")
        try:
            response: Union[Completion, Stream[Completion]] = cast(
                Any, self.instance.completions
            )._original_create(*args, **kwargs)

            if isinstance(response, Stream):
                logger.info("Response is a Stream")
                return capture_chunks_with_timings_and_reyield(
                    cast(Generator[Completion, Any, Any], response),
                    lambda chunks, first_token_at, finished_at: self.handle_deltas(
                        chunks,
                        SpanTimestamps(
                            started_at=started_at,
                            first_token_at=first_token_at,
                            finished_at=finished_at,
                        ),
                        **kwargs,
                    ),
                )
            else:
                finished_at = milliseconds_timestamp()
                logger.info(f"Completion finished at: {finished_at}")
                self.handle_completion(
                    response,
                    SpanTimestamps(started_at=started_at, finished_at=finished_at),
                    **kwargs,
                )
                return response
        except Exception as err:
            finished_at = milliseconds_timestamp()
            logger.exception(f"Exception occurred at: {finished_at}", exc_info=err)
            self.handle_exception(
                err,
                SpanTimestamps(started_at=started_at, finished_at=finished_at),
                **kwargs,
            )
            raise err

    async def patched_completion_acreate(self, *args, **kwargs):
        started_at = milliseconds_timestamp()
        logger.info(f"Patched async completion create started at: {started_at}")
        response: Union[Completion, AsyncStream[Completion]] = await cast(
            Any, self.instance.completions
        )._original_create(*args, **kwargs)

        if isinstance(response, AsyncStream):
            logger.info("Response is an AsyncStream")
            return capture_async_chunks_with_timings_and_reyield(
                cast(AsyncGenerator[Completion, Any], response),
                lambda chunks, first_token_at, finished_at: self.handle_deltas(
                    chunks,
                    SpanTimestamps(
                        started_at=started_at,
                        first_token_at=first_token_at,
                        finished_at=finished_at,
                    ),
                    **kwargs,
                ),
            )
        else:
            finished_at = milliseconds_timestamp()
            logger.info(f"Async completion finished at: {finished_at}")
            self.handle_completion(
                response,
                SpanTimestamps(started_at=started_at, finished_at=finished_at),
                **kwargs,
            )
            return response

    def handle_deltas(
        self,
        deltas: List[Completion],
        timestamps: SpanTimestamps,
        **kwargs,
    ):
        logger.info(f"Handling deltas: {deltas}")
        text_outputs: Dict[int, str] = {}
        for delta in deltas:
            for choice in delta.choices:
                index = choice.index or 0
                text_outputs[index] = text_outputs.get(index, "") + (choice.text or "")

        self.append_span(
            self.build_trace(
                outputs=[
                    TypedValueText(type="text", value=output)
                    for output in text_outputs.values()
                ],
                metrics=SpanMetrics(),
                timestamps=timestamps,
                error=None,
                **kwargs,
            )
        )
        logger.info("Deltas handled successfully")

    def handle_completion(
        self,
        response: Completion,
        timestamps: SpanTimestamps,
        **kwargs,
    ):
        logger.info(f"Handling completion: {response}")
        self.append_span(
            self.build_trace(
                outputs=[
                    TypedValueText(type="text", value=output.text)
                    for output in response.choices
                ],
                metrics=SpanMetrics(
                    prompt_tokens=safe_get(response, "usage", "prompt_tokens"),
                    completion_tokens=safe_get(response, "usage", "completion_tokens"),
                ),
                timestamps=timestamps,
                error=None,
                **kwargs,
            )
        )
        logger.info("Completion handled successfully")

    def handle_exception(
        self,
        err: Exception,
        timestamps: SpanTimestamps,
        **kwargs,
    ):
        logger.exception("Handling exception", exc_info=err)
        self.append_span(
            self.build_trace(
                outputs=[],
                metrics=SpanMetrics(),
                timestamps=timestamps,
                error=capture_exception(err),
                **kwargs,
            )
        )
        logger.info("Exception handled")

    def build_trace(
        self,
        outputs: List[SpanInputOutput],
        metrics: SpanMetrics,
        timestamps: SpanTimestamps,
        error: Optional[ErrorCapture],
        **kwargs,
    ) -> LLMSpan:
        logger.info("Building trace")
        return LLMSpan(
            type="llm",
            span_id=f"span_{nanoid.generate()}",
            parent_id=self.get_parent_id(),
            trace_id=self.trace_id,
            vendor="openai",
            model=kwargs.get("model", "unknown"),
            input=TypedValueText(type="text", value=kwargs.get("prompt", "")).copy(),
            outputs=outputs,
            error=error,
            params=SpanParams(
                temperature=kwargs.get("temperature", 1.0),
                stream=kwargs.get("stream", False),
            ),
            metrics=metrics,
            timestamps=timestamps,
        )


class OpenAIChatCompletionTracer(BaseContextTracer):
    def __init__(
        self,
        instance: Union[OpenAI, AsyncOpenAI, AzureOpenAI, AsyncAzureOpenAI],
        trace_id: Optional[str] = None,
        metadata: Optional[TraceMetadata] = None,
    ):
        self.instance = instance
        super().__init__(
            trace_id=trace_id,
            metadata=metadata,
        )
        logger.info("Initialized OpenAIChatCompletionTracer")

    def __enter__(self):
        super().__enter__()
        self.instance.chat.completions._original_create = self.instance.chat.completions.create  # type: ignore
        if isinstance(self.instance, AsyncOpenAI):
            self.instance.chat.completions.create = self.patched_completion_acreate  # type: ignore
        else:
            self.instance.chat.completions.create = self.patched_completion_create  # type: ignore
        logger.info("Entered OpenAIChatCompletionTracer")

    def __exit__(self, _type, _value, _traceback):
        super().__exit__(_type, _value, _traceback)
        self.instance.chat.completions.create = self.instance.chat.completions._original_create  # type: ignore
        logger.info("Exited OpenAIChatCompletionTracer")

    def patched_completion_create(self, *args, **kwargs):
        started_at = milliseconds_timestamp()
        logger.info(f"Patched chat completion create started at: {started_at}")
        try:
            response: Union[ChatCompletion, Stream[ChatCompletionChunk]] = cast(
                Any, self.instance.chat.completions
            )._original_create(*args, **kwargs)

            if isinstance(response, Stream):
                logger.info("Response is a Stream")
                return capture_chunks_with_timings_and_reyield(
                    cast(Generator[ChatCompletionChunk, Any, Any], response),
                    lambda chunks, first_token_at, finished_at: self.handle_deltas(
                        chunks,
                        SpanTimestamps(
                            started_at=started_at,
                            first_token_at=first_token_at,
                            finished_at=finished_at,
                        ),
                        **kwargs,
                    ),
                )
            else:
                finished_at = milliseconds_timestamp()
                logger.info(f"Chat completion finished at: {finished_at}")
                self.handle_completion(
                    response,
                    SpanTimestamps(started_at=started_at, finished_at=finished_at),
                    **kwargs,
                )
                return response
        except Exception as err:
            finished_at = milliseconds_timestamp()
            logger.exception(f"Exception occurred at: {finished_at}", exc_info=err)
            self.handle_exception(
                err,
                SpanTimestamps(started_at=started_at, finished_at=finished_at),
                **kwargs,
            )
            raise err

    async def patched_completion_acreate(self, *args, **kwargs):
        started_at = milliseconds_timestamp()
        logger.info(f"Patched async chat completion create started at: {started_at}")
        response: Union[ChatCompletion, AsyncStream[ChatCompletionChunk]] = await cast(
            Any, self.instance.chat.completions
        )._original_create(*args, **kwargs)

        if isinstance(response, AsyncStream):
            logger.info("Response is an AsyncStream")
            return capture_async_chunks_with_timings_and_reyield(
                cast(AsyncGenerator[ChatCompletionChunk, Any], response),
                lambda chunks, first_token_at, finished_at: self.handle_deltas(
                    chunks,
                    SpanTimestamps(
                        started_at=started_at,
                        first_token_at=first_token_at,
                        finished_at=finished_at,
                    ),
                    **kwargs,
                ),
            )
        else:
            finished_at = milliseconds_timestamp()
            logger.info(f"Async chat completion finished at: {finished_at}")
            self.handle_completion(
                response,
                SpanTimestamps(started_at=started_at, finished_at=finished_at),
                **kwargs,
            )
            return response

    def handle_deltas(
        self,
        deltas: List[ChatCompletionChunk],
        timestamps: SpanTimestamps,
        **kwargs,
    ):
        logger.info(f"Handling chat completion deltas: {deltas}")
        # Accumulate deltas
        chat_outputs: Dict[int, List[ChatMessage]] = {}
        for delta in deltas:
            for choice in delta.choices:
                index = choice.index
                delta = choice.delta
                if delta.role:
                    chat_message: ChatMessage = {
                        "role": delta.role,
                        "content": delta.content,
                    }
                    if delta.function_call:
                        chat_message["function_call"] = {
                            "name": delta.function_call.name or "",
                            "arguments": delta.function_call.arguments or "",
                        }
                    if delta.tool_calls:
                        chat_message["tool_calls"] = [
                            {
                                "id": tool.id or "",
                                "type": tool.type or "",
                                "function": {
                                    "name": safe_get(tool, "function", "name") or "",
                                    "arguments": safe_get(tool, "function", "arguments")
                                    or "",
                                },
                            }
                            for tool in delta.tool_calls
                        ]
                    if index not in chat_outputs:
                        chat_outputs[index] = []
                    chat_outputs[index].append(chat_message)
                elif delta.function_call:
                    last_item = chat_outputs[index][-1]
                    if "function_call" in last_item and last_item["function_call"]:
                        current_arguments = last_item["function_call"].get(
                            "arguments", ""
                        )
                        last_item["function_call"]["arguments"] = current_arguments + (
                            delta.function_call.arguments or ""
                        )
                elif delta.tool_calls:
                    last_item = chat_outputs[index][-1]
                    if (
                        "tool_calls" in last_item
                        and last_item["tool_calls"]
                        and len(last_item["tool_calls"]) > 0
                    ):
                        for tool in delta.tool_calls:
                            last_item["tool_calls"][tool.index]["function"][
                                "arguments"
                            ] = last_item["tool_calls"][tool.index]["function"].get(
                                "arguments", ""
                            ) + (
                                safe_get(tool, "function", "arguments") or ""
                            )
                elif delta.content:
                    chat_outputs[index][-1]["content"] = (
                        chat_outputs[index][-1].get("content", "") or ""
                    ) + delta.content

        self.append_span(
            self.build_trace(
                outputs=[
                    TypedValueChatMessages(type="chat_messages", value=output)
                    for output in chat_outputs.values()
                ],
                metrics=SpanMetrics(),
                timestamps=timestamps,
                error=None,
                **kwargs,
            )
        )
        logger.info("Chat completion deltas handled successfully")

    def handle_completion(
        self,
        response: ChatCompletion,
        timestamps: SpanTimestamps,
        **kwargs,
    ):
        logger.info(f"Handling chat completion: {response}")
        self.append_span(
            self.build_trace(
                outputs=[
                    TypedValueChatMessages(
                        type="chat_messages",
                        value=[cast(ChatMessage, output.message.model_dump())],
                    )
                    for output in response.choices
                ],
                metrics=SpanMetrics(
                    prompt_tokens=safe_get(response, "usage", "prompt_tokens"),
                    completion_tokens=safe_get(response, "usage", "completion_tokens"),
                ),
                timestamps=timestamps,
                error=None,
                **kwargs,
            )
        )
        logger.info("Chat completion handled successfully")

    def handle_exception(
        self,
        err: Exception,
        timestamps: SpanTimestamps,
        **kwargs,
    ):
        logger.exception("Handling exception in chat completion", exc_info=err)
        self.append_span(
            self.build_trace(
                outputs=[],
                metrics=SpanMetrics(),
                timestamps=timestamps,
                error=capture_exception(err),
                **kwargs,
            )
        )
        logger.info("Chat completion exception handled")

    def build_trace(
        self,
        outputs: List[SpanInputOutput],
        metrics: SpanMetrics,
        timestamps: SpanTimestamps,
        error: Optional[ErrorCapture],
        **kwargs,
    ) -> LLMSpan:
        logger.info("Building chat completion trace")
        params = SpanParams(
            temperature=kwargs.get("temperature", 1.0),
            stream=kwargs.get("stream", False),
        )
        functions = kwargs.get("functions", None)
        if functions:
            params["functions"] = functions
        tools = kwargs.get("tools", None)
        if tools:
            params["tools"] = tools
        tool_choice = kwargs.get("tool_choice", None)
        if tool_choice:
            params["tool_choice"] = tool_choice
        return LLMSpan(
            type="llm",
            span_id=f"span_{nanoid.generate()}",
            parent_id=self.get_parent_id(),
            trace_id=self.trace_id,
            vendor=(
                "azure"
                if issubclass(type(self.instance), AzureOpenAI)
                or issubclass(type(self.instance), AsyncAzureOpenAI)
                else "openai"
            ),
            model=kwargs.get("model", "unknown"),
            input=TypedValueChatMessages(
                type="chat_messages", value=kwargs.get("messages", []).copy()
            ),
            outputs=outputs,
            error=error,
            params=params,
            metrics=metrics,
            timestamps=timestamps,
        )
                                