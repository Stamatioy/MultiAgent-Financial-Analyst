from financial_analyst.llm.client import LocalLLMClient


def test_remove_json_markdown_fence() -> None:
    content = """```json
{
  "result": "valid"
}
```"""

    cleaned = LocalLLMClient._remove_markdown_fences(content)

    assert cleaned == """{
  "result": "valid"
}"""