# 📁 New Clean Project Structure

Created on: November 24, 2024

This is the new clean architecture for the Deep Search Agent, following best practices for separation of concerns.

## 🎯 Structure Overview

```
deep-search-agent/
├── deep_search_agent/          # Main package (NEW CLEAN STRUCTURE)
│   ├── __init__.py
│   ├── config.py              # Settings (model_backend, keys, timeouts)
│   │
│   ├── cli/                   # CLI Interface layer
│   │   ├── __init__.py
│   │   └── app.py            # run_cli(): loop to read input -> call agent
│   │
│   ├── agents/                # Core agent logic
│   │   ├── __init__.py
│   │   ├── deep_search_agent.py   # Main DeepSearchAgent (plan + run)
│   │   └── steps/            # Agentic steps breakdown
│   │       ├── __init__.py
│   │       ├── plan.py       # Decompose query -> plan
│   │       ├── search.py     # Call retrieval
│   │       ├── aggregate.py  # Merge / filter results
│   │       └── summarize.py  # Summarize, format output
│   │
│   ├── workflows/             # Different workflow versions
│   │   ├── __init__.py
│   │   ├── basic.py          # Simple workflow (demo)
│   │   ├── production.py     # Production-ready workflow
│   │   └── langgraph_based.py # LangGraph-based workflow
│   │
│   ├── models/                # LLM backend abstraction
│   │   ├── __init__.py
│   │   ├── base.py           # BaseLLM, BaseEmbeddings
│   │   ├── openai_backend.py # OpenAI / API providers
│   │   └── local_backend.py  # Local models (Ollama, vLLM)
│   │
│   ├── retrieval/             # Search & RAG layer
│   │   ├── __init__.py
│   │   ├── base.py           # Retriever interface
│   │   ├── web_search.py     # Search APIs (Tavily, Serper)
│   │   ├── crawler.py        # Firecrawl / custom crawling
│   │   └── rag.py            # Retrieve + chunk + rerank
│   │
│   ├── prompts/               # Prompt templates
│   │   ├── __init__.py
│   │   ├── system.py         # Global system prompt
│   │   ├── search_prompt.py  # Search prompts
│   │   └── summarize_prompt.py # Summarization prompts
│   │
│   ├── context/               # Context/memory management
│   │   ├── __init__.py
│   │   └── memory.py         # Short-term / long-term memory
│   │
│   ├── infra/                 # Cross-cutting infrastructure
│   │   ├── __init__.py
│   │   ├── cache.py          # Cache web/LLM results
│   │   ├── rate_limiter.py   # Rate limiting
│   │   └── logger.py         # Structured logging
│   │
│   ├── tools/                 # Tool wrappers for agent
│   │   ├── __init__.py
│   │   ├── firecrawl_client.py  # Firecrawl wrapper
│   │   └── web_search_tool.py   # Search tool wrapper
│   │
│   └── utils/                 # Helper utilities
│       ├── __init__.py
│       ├── text.py           # Text processing utils
│       └── timing.py         # Timing/metrics utils
│
├── tests_new/                 # Test suite (NEW)
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_agents.py
│   │   ├── test_retrieval.py
│   │   ├── test_models.py
│   │   └── test_cli.py
│   └── performance/
│       ├── __init__.py
│       └── test_end_to_end.py
│
├── src/                       # OLD structure (to be migrated)
│   └── ... (existing files)
│
├── main.py                    # Entry point
├── config.py                  # Global config (OLD)
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## 📊 File Count

**New Structure:**
- Total directories: 11
- Total files: 53
- Python modules: 47

## 🎯 Key Design Principles

### 1. **Separation of Concerns**
- **CLI layer** (`cli/`) - Handles only I/O and terminal interaction
- **Agents layer** (`agents/`) - Pure business logic, no I/O
- **Infrastructure** (`infra/`) - Cross-cutting concerns
- **Tools** (`tools/`) - External service wrappers

### 2. **Abstraction**
- **Models** (`models/`) - Abstract LLM backends (OpenAI vs local)
- **Retrieval** (`retrieval/`) - Abstract search/RAG operations
- **Workflows** (`workflows/`) - Different execution strategies

### 3. **Modularity**
- Each component is independently testable
- Clear interfaces between layers
- Easy to swap implementations

### 4. **Extensibility**
- Add new workflows without changing core logic
- Support multiple LLM backends
- Plug in different search providers

## 🚀 Next Steps

### Phase 1: Migration (Current State)
- [x] Create new directory structure
- [x] Create all placeholder files
- [ ] Move existing code to new structure
- [ ] Update imports

### Phase 2: Refactoring
- [ ] Split monolithic workflow into steps
- [ ] Abstract LLM backend
- [ ] Create proper interfaces
- [ ] Add dependency injection

### Phase 3: Testing
- [ ] Write unit tests for each module
- [ ] Add integration tests
- [ ] Performance benchmarks

### Phase 4: Documentation
- [ ] Add docstrings to all modules
- [ ] Create usage examples
- [ ] API documentation

## 📝 Usage (After Migration)

```python
from deep_search_agent.cli.app import run_cli

# Run CLI interface
run_cli()
```

Or programmatically:

```python
from deep_search_agent.agents.deep_search_agent import DeepSearchAgent
from deep_search_agent.workflows.production import ProductionWorkflow

# Create agent
agent = DeepSearchAgent(workflow=ProductionWorkflow())

# Run search
result = agent.search("Python web frameworks 2024")
print(result)
```

## 🔄 Migration Guide

To migrate from old `src/` structure to new `deep_search_agent/`:

1. **Models** - Move `src/models*.py` → `deep_search_agent/models/`
2. **Workflows** - Move `src/workflow*.py` → `deep_search_agent/workflows/`
3. **Tools** - Move `src/tools*.py` → `deep_search_agent/tools/`
4. **Retrieval** - Move `src/retrieval/` → `deep_search_agent/retrieval/`
5. **Infrastructure** - Move `src/cache.py`, `src/logger.py`, `src/rate_limiter.py` → `deep_search_agent/infra/`
6. **Prompts** - Move `src/prompts.py` → `deep_search_agent/prompts/`

---

**Status:** Structure created, ready for code migration

