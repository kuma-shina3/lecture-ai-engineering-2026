from types import SimpleNamespace

import app.ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    class FakeModels:
        def generate_content(self, model, contents):
            return SimpleNamespace(
                text="回答テキスト",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=123,
                    candidates_token_count=45,
                ),
            )

    class FakeClient:
        def __init__(self, *, api_key):
            self.api_key = api_key
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", lambda api_key: FakeClient(api_key=api_key))
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "dummy-key")

    response_text = ask_module.ask("質問")

    captured = capsys.readouterr().out
    assert response_text == "回答テキスト"
    assert "入力トークン" in captured
    assert "123" in captured
    assert "出力トークン" in captured
    assert "45" in captured
