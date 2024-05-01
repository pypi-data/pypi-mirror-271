### cntrlai/guardrails.py
from typing import List, Literal, Optional, Union, cast
from warnings import warn

import httpx
from pydantic import BaseModel

import cntrlai
import cntrlai.logger
from cntrlai.logger import ContextSpan, get_current_tracer, _local_context
from cntrlai.types import GuardrailResult, RAGChunk, TypedValueGuardrailResult


class Money(BaseModel):
    currency: str
    amount: float


class GuardrailResultModel(BaseModel):
    status: Literal["processed", "skipped", "error"]
    passed: bool = True
    score: Optional[float] = None
    details: Optional[str] = None
    cost: Optional[Money] = None


def evaluate(
    slug: str,
    input: Optional[str] = None,
    output: Optional[str] = None,
    contexts: List[RAGChunk] = [],
):
    with cntrlai.logger.create_span(name=slug, type="guardrail") as span:
        request_params = prepare_data(slug, input, output, contexts, span=span)
        try:
            with httpx.Client() as client:
                response = client.post(**request_params)
                response.raise_for_status()
        except Exception as e:
            return handle_response(
                {
                    "status": "error",
                    "message": str(e),
                    "passed": True,
                },
                span,
            )

        return handle_response(response.json(), span)


async def async_evaluate(
    slug: str,
    input: Optional[str] = None,
    output: Optional[str] = None,
    contexts: List[RAGChunk] = [],
):
    current_span = getattr(_local_context, "current_span", None)
    with cntrlai.logger.create_span(name=slug, type="guardrail") as span:
        # hack: avoid nesting async evaluate spans when they are called in parallel
        _local_context.current_span = current_span

        request_params = prepare_data(slug, input, output, contexts, span=span)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(**request_params)
                response.raise_for_status()
        except Exception as e:
            return handle_response(
                {
                    "status": "error",
                    "message": str(e),
                    "passed": True,
                },
                span,
            )

        return handle_response(response.json(), span)


def prepare_data(
    slug: str,
    input: Optional[str],
    output: Optional[str],
    contexts: List[RAGChunk],
    span: ContextSpan,
):
    current_tracer = get_current_tracer()
    data = {}
    if input:
        data["input"] = input
    if output:
        data["output"] = output
    if contexts and len(contexts) > 0:
        data["contexts"] = contexts
    span.input = data

    return {
        "url": cntrlai.endpoint + f"/api/guardrails/{slug}/evaluate",
        "json": {
            "trace_id": current_tracer.trace_id if current_tracer else None,
            "data": data,
        },
        "headers": {"X-Auth-Token": str(cntrlai.api_key)},
    }


def handle_response(
    response: dict,
    span: ContextSpan,
):
    result = GuardrailResultModel.model_validate(response)
    if result.status == "error":
        result.details = response.get("message", "")
    span.output = TypedValueGuardrailResult(
        type="guardrail_result", value=cast(GuardrailResult, result.model_dump())
    )
    return result