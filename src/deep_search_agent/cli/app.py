"""Terminal entrypoint for the Deep Search Agent."""

from __future__ import annotations

import argparse
import json
from typing import Callable, List, Optional

from dotenv import load_dotenv

from deep_search_agent.agents.types import AgentResult
from deep_search_agent.agents.deep_search_agent import DeepSearchAgent, default_agent
from ..config import settings
from ..models.base import BaseLLM
from ..models.local_backend import LocalLLM
from ..models.openai_backend import OpenAILLM
from ..retrieval.base import BaseRetriever
from ..retrieval.stub import StubRetriever
from ..retrieval.web_search import DuckDuckGoRetriever


def build_llm(active_settings) -> BaseLLM:
    if active_settings.offline or active_settings.llm_provider != "openai":
        return LocalLLM()
    try:
        return OpenAILLM(api_key=active_settings.openai_api_key, model=active_settings.openai_model)
    except RuntimeError:
        # Fallback if API key missing.
        return LocalLLM()


def build_retriever(active_settings) -> BaseRetriever:
    if active_settings.offline:
        return StubRetriever()
    return DuckDuckGoRetriever(max_results=active_settings.web_max_results)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deep Search Agent CLI")
    parser.add_argument(
        "query",
        nargs="?",
        help="Run once with this query (otherwise enter interactive mode).",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use local LLM + stub retriever (never touch network/APIs).",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Prompt exactly once (after the first answer, exit the CLI).",
    )
    parser.add_argument(
        "--workflow",
        choices=["basic", "production", "langgraph"],
        default="production",
        help="Select which workflow implementation to run.",
    )
    parser.add_argument(
        "--llm-provider",
        choices=["openai", "local"],
        help="Override the configured LLM provider.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        metavar="N",
        help="Number of web documents to fetch per sub-query.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print AgentResult as JSON with keys (query, answer, sources).",
    )
    return parser.parse_args(argv)


def run_cli(
    argv: Optional[List[str]] = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    load_dotenv()
    args = parse_args(argv)
    overrides = {}
    if args.offline or settings.offline:
        overrides["offline"] = True
    if args.llm_provider:
        overrides["llm_provider"] = args.llm_provider
    if args.top_k:
        overrides["web_max_results"] = args.top_k
    active_settings = settings.with_overrides(**overrides) if overrides else settings
    llm = build_llm(active_settings)
    retriever = build_retriever(active_settings)
    agent = DeepSearchAgent.from_settings(active_settings, workflow_name=args.workflow)

    output_fn("=" * 60)
    mode = "OFFLINE" if active_settings.offline else "ONLINE"
    output_fn(f"Deep Search Agent (CLI) - {mode} mode")
    output_fn("=" * 60)

    def render(query: str) -> None:
        result = agent.run(query)
        if args.json:
            output_fn(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
            return
        pretty_print_result(result, output_fn)

    if args.query:
        render(args.query)
        return

    while True:
        query = input_fn("🔎 Query (or 'exit'): ").strip()
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            output_fn("Goodbye!")
            break
        render(query)
        if args.once:
            break


def pretty_print_result(result: AgentResult, output_fn: Callable[[str], None]) -> None:
    output_fn(f"\nPlan: {result.plan}")
    output_fn("\nFindings:")
    for finding in result.findings:
        output_fn(f"- {finding.title} -> {finding.url}")
    output_fn("\nSummary:\n" + result.summary + "\n")
