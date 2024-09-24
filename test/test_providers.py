from az.ollama_provider import OllamaClient

import pytest
from az.ollama_provider import OllamaClient
from az.openai_provider import OpenAIClient
from az.anthropic_provider import AnthropicClient
from az.gemini_provider import GeminiClient

@pytest.fixture(params=[OllamaClient, OpenAIClient, AnthropicClient, GeminiClient])
def client(request):
    return request.param(primer="Limit your response to 300 characters or less")

@pytest.mark.expensive
@pytest.mark.parametrize("question,expected", [
    # ("how much is 6^2?", "36"),
    ("what is the capital of France?", "Paris"),
    # ("who wrote 'To Kill a Mockingbird'?", "Harper Lee"),
])
def test_providers(client, question, expected):
    response = ""
    for text in client.chat(question):
        response += text
    assert expected in response
    assert client.n_user_messages() == 1
    client.new_chat()
    assert client.n_user_messages() == 0


