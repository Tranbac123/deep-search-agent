from deep_search_agent.retrieval.base import WebDocument
from deep_search_agent.retrieval.rag import score_documents


def test_score_documents_orders_by_overlap() -> None:
    query = "python web framework"
    documents = [
        WebDocument(title="Django", url="https://djangoproject.com", snippet="Python web framework", content=""),
        WebDocument(title="Rust", url="https://rust-lang.org", snippet="systems programming language", content=""),
    ]
    ranked = score_documents(query, documents)
    assert ranked[0].document.title == "Django"
