"""Minimal bind_tools agent loop (no langgraph.prebuilt dependency)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import NamedTuple

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool

from tools.trace_call import trace_info, trace_span


class ToolAgentResult(NamedTuple):
    """Final assistant text plus tools invoked during the loop."""

    text: str
    tools_called: list[str]


def run_tool_agent(
    *,
    model: BaseChatModel,
    tools: Sequence[BaseTool],
    system: str,
    user: str,
    max_turns: int = 8,
) -> ToolAgentResult:
    """Run a tool-calling chat loop; return final text and tools called."""
    bound = model.bind_tools(list(tools))
    tools_by_name = {t.name: t for t in tools}
    tools_called: list[str] = []
    messages: list[BaseMessage] = [
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]
    with trace_span("agent", "tool_loop", max_turns=max_turns, tools=len(tools)):
        for turn in range(1, max_turns + 1):
            with trace_span("turn", f"{turn}/{max_turns}"):
                response = bound.invoke(messages)
                messages.append(response)
                if not isinstance(response, AIMessage) or not response.tool_calls:
                    text = _text_content(response)
                    trace_info("final text", chars=len(text), tools=len(tools_called))
                    return ToolAgentResult(text=text, tools_called=tools_called)
                for call in response.tool_calls:
                    name = call["name"]
                    args = call["args"]
                    tools_called.append(name)
                    trace_info("invoke", tool=name, **_safe_args(args))
                    tool = tools_by_name[name]
                    result = tool.invoke(args)
                    messages.append(
                        ToolMessage(content=str(result), tool_call_id=call["id"])
                    )
        text = _text_content(messages[-1])
        trace_info("max turns reached", chars=len(text), tools=len(tools_called))
        return ToolAgentResult(text=text, tools_called=tools_called)


def _safe_args(args: object) -> dict[str, object]:
    if not isinstance(args, dict):
        return {"args": args}
    return {str(k): v for k, v in args.items()}


def _text_content(message: object) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    return str(content)
