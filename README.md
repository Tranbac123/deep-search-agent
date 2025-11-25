# 🔍 Deep Search Agent

Command-line research assistant that plans web queries, gathers evidence, and summarizes answers through an LLM-driven workflow. Works fully offline (stub retriever + local LLM) or online (DuckDuckGo + OpenAI).

## 🚧 Features at a Glance

- Multi-step workflow (plan → search → aggregate → summarize)
- Pluggable LLM backend (`BaseLLM`) with OpenAI or local stub
- Swappable retrievers (`BaseRetriever`) with DuckDuckGo or stub data
- CLI with REPL and single-run modes, JSON output for automation
- Easy embedding via `DeepSearchAgent.from_settings(...)`

## ⚙️ Installation

```bash
git clone https://github.com/your-org/deep-search-agent
cd deep-search-agent
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env  # optional; set OPENAI_API_KEY etc. if using online mode
```

### Environment options

- `DEEPSEARCH_OFFLINE=true` (or `--offline`) keeps everything local with stub data.
- Set `OPENAI_API_KEY=sk-...` to enable the OpenAI backend; otherwise the CLI quietly falls back to the local LLM.
- Other knobs (LLM model, top_k, etc.) live in `.env.example` and can be overridden via CLI flags.

## 🖥️ CLI Usage

### Offline mode (default when `DEEPSEARCH_OFFLINE=true` or `--offline`)
```bash
python main.py --offline
```
This uses the local stub LLM + stub retriever (no network/API keys needed).

### Online mode (requires `OPENAI_API_KEY`)
```bash
export OPENAI_API_KEY=sk-...
python main.py --workflow production
```

### REPL mode (default)
```bash
python main.py --offline
🔎 Query (or 'exit'): best open-source LLMs
...
```
Add `--once` to exit after the first answer.

### Single query + JSON output
```bash
python main.py --offline --json "compare fastapi and flask"
```
Prints structured JSON with `query`, `plan`, `answer`, and `sources`.

### Useful flags
- `--offline` – force local LLM + stub retriever
- `--workflow {basic,production,langgraph}` – choose workflow
- `--llm-provider {openai,local}` – override backend
- `--top-k N` – limit retrieved documents per step
- `--json` – emit JSON instead of prose
- positional `query` – run once and exit
- `--once` – exit after first REPL answer

## 🧩 Embedding as a Library

```python
from deep_search_agent.config import get_settings
from deep_search_agent.agents.deep_search_agent import DeepSearchAgent

settings = get_settings().with_overrides(offline=True)
agent = DeepSearchAgent.from_settings(settings, workflow_name="production")
result = agent.run("best vector databases 2024")

print(result.summary)
for source in result.findings:
    print(source.title, source.url)
```

`AgentResult` exposes `summary`, `plan`, and `findings`, plus `to_dict()` for serialization.

## 🧪 Tests

All tests run offline using stubs:

```bash
pytest
```

## 📁 Project Layout

```
deep-search-agent/
├── main.py                     # CLI entrypoint
├── src/deep_search_agent/
│   ├── cli/                    # CLI wiring
│   ├── agents/                 # DeepSearchAgent + steps
│   ├── workflows/              # basic / production / langgraph
│   ├── models/                 # BaseLLM, OpenAI backend, Local backend
│   ├── retrieval/              # BaseRetriever, DuckDuckGo, stub
│   ├── prompts/, context/, infra/, tools/, utils/
└── tests/                      # Offline unit/perf tests
```

## 📝 Notes

- Offline mode is recommended for development and CI.
- Online mode only activates when `OPENAI_API_KEY` is set and `--offline` is not used.
- Extend or replace retrievers/LLMs by implementing the `BaseRetriever` / `BaseLLM` protocols.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/unit/test_workflow.py -v
```

## ⚙️ Configuration

Key settings in `.env`:

```bash
# LLM Configuration
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.1

# RAG Configuration
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
RAG_TOP_K=6
VECTOR_SIMILARITY_THRESHOLD=0.35

# Workflow Configuration
MAX_TOOLS_PER_QUERY=5
MAX_CONTENT_LENGTH=2000

# Rate Limiting
REQUESTS_PER_MINUTE=60
ENABLE_RATE_LIMITING=true

# Caching
ENABLE_CACHING=true
CACHE_TTL_HOURS=24
```

## 📁 Project Structure

```
DEEP-SEARCH-AGENT/
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── main.py                 # entrypoint: python main.py -> calls CLI
├── src/
│   └── deep_search_agent/  # main package
│       ├── __init__.py
│       ├── config.py       # Settings (model_backend, keys, timeouts,…)
│       │
│       ├── cli/            # Interface layer: handles CLI / terminal I/O only
│       │   ├── __init__.py
│       │   └── app.py      # run_cli(): loop to read input -> call agent
│       │
│       ├── agents/         # Core agent logic (no I/O dependency)
│       │   ├── __init__.py
│       │   ├── deep_search_agent.py   # DeepSearchAgent (plan + run)
│       │   └── steps/      # if you want to break down into agentic steps
│       │       ├── __init__.py
│       │       ├── plan.py           # decompose query -> plan
│       │       ├── search.py         # call retrieval
│       │       ├── aggregate.py      # merge / filter results
│       │       └── summarize.py      # summarize, format output
│       │
│       ├── workflows/      # different flow versions
│       │   ├── __init__.py
│       │   ├── basic.py              # simple workflow (demo)
│       │   ├── production.py         # more production-ready workflow
│       │   └── langgraph_based.py    # if using LangGraph
│       │
│       ├── models/         # LLM backend abstraction (local & API)
│       │   ├── __init__.py
│       │   ├── base.py              # BaseLLM, BaseEmbeddings,...
│       │   ├── openai_backend.py    # using OpenAI / other API providers
│       │   └── local_backend.py     # using local models (Ollama, vLLM,…)
│       │
│       ├── retrieval/      # search & RAG layer
│       │   ├── __init__.py
│       │   ├── base.py             # Retriever interface
│       │   ├── web_search.py       # call search APIs (Tavily, Serper,…)
│       │   ├── crawler.py          # Firecrawl / custom crawling
│       │   └── rag.py              # retrieve + chunk + rerank (if needed)
│       │
│       ├── prompts/        # prompt templates for each step
│       │   ├── __init__.py
│       │   ├── system.py           # global system prompt
│       │   ├── search_prompt.py
│       │   └── summarize_prompt.py
│       │
│       ├── context/        # context/memory management (if needed)
│       │   ├── __init__.py
│       │   └── memory.py          # short-term / long-term memory
│       │
│       ├── infra/          # shared infrastructure (cross-cutting)
│       │   ├── __init__.py
│       │   ├── cache.py           # cache web/LLM results
│       │   ├── rate_limiter.py
│       │   └── logger.py
│       │
│       ├── tools/          # wrappers as "Tools" for agent
│       │   ├── __init__.py
│       │   ├── firecrawl_client.py
│       │   └── web_search_tool.py  # uses Retriever + format results for LLM
│       │
│       └── utils/          # small helpers, pure logic
│           ├── __init__.py
│           ├── text.py            # clean_text, truncate, highlight,...
│           └── timing.py          # measure time, simple metrics
│
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── test_agents.py
    │   ├── test_retrieval.py
    │   ├── test_models.py
    │   └── test_cli.py
    └── performance/
        ├── __init__.py
        └── test_end_to_end.py      # measure end-to-end search agent timing

```

## 🔄 Workflow Pipeline

The production workflow follows this pipeline:

1. **Planning** - Break down research question into sub-questions
2. **Search** - Multi-provider search (Tavily, Brave, Firecrawl)
3. **Fetch & Parse** - Scrape content, create chunks, generate embeddings
4. **Evidence Selection** - Semantic search + scoring to find best evidence
5. **Synthesis** - LLM generates answer with citations
6. **Critique** - Verify completeness and accuracy
7. **Fact-Check Gate** - Ensure claims have sufficient evidence
8. **Finalize** - Export evidence pack with full traceability

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add more search providers (Google, DuckDuckGo)
- Improve chunking strategies (semantic chunking)
- Add more embedding models
- Enhance citation formatting
- Add web UI
- Add API server mode

## 📝 License

MIT License - see LICENSE file for details

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall in editable mode
pip install -e .
```

### "API key not found"
```bash
# Check your .env file exists
cat .env

# Verify it contains your keys
# OPENAI_API_KEY=sk-...
# FIRECRAWL_API_KEY=fc-...
```

### Tests failing
```bash
# Some tests require actual API keys
# Skip integration tests if needed
pytest -m "not integration"
```

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

---

Built with ❤️ using LangChain and LangGraph
