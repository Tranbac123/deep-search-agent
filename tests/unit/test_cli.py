from io import StringIO

from deep_search_agent.cli import app as cli_app


def test_cli_single_query_json_offline():
    output = StringIO()

    cli_app.run_cli(
        argv=["--offline", "--json", "offline json query"],
        output_fn=lambda msg: output.write(msg + "\n"),
    )

    content = output.getvalue()
    assert '"query": "offline json query"' in content
    assert '"sources":' in content


def test_cli_repl_once_mode():
    inputs = iter(["repl question"])
    output = StringIO()

    cli_app.run_cli(
        argv=["--offline", "--once"],
        input_fn=lambda _: next(inputs),
        output_fn=lambda msg: output.write(msg + "\n"),
    )

    content = output.getvalue()
    assert "Plan" in content
    assert "Summary" in content
