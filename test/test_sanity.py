import io
import re
from unittest.mock import patch, call
from io import StringIO

from prompt_toolkit.input import create_pipe_input
import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.output import DummyOutput

from az.az import main

"""
I am using multiple methods to test the CLI. Just my knowledge of how to test prompt_toolkit apps 
which evolved over time.

TODO:
- mock configured providers (the reading of env vars should be done in main(), otherwise it's not mocked)
"""


class MockLLM:
    def __init__(self, response):
        self.response = response
        self._n_user_messages = 0

    def chat(self, prompt):
        # can simulate a list of responses as well as a single response
        if isinstance(self.response, list):
            for r in self.response: 
                yield r
        else:
            yield self.response
        self._n_user_messages += 1

    def n_user_messages(self):
        return self._n_user_messages
    
    def __str__(self):
        return "MockLLM"
    

@pytest.fixture(autouse=True, scope="function")
def modify_env_variables(monkeypatch):
    for var in ['OPENAI_API_KEY', 'OLLAMA_URL', 'ANTHROPIC_API_KEY', 'GEMINI_API_KEY']:
        monkeypatch.delenv(var, raising=False)
    yield


def test_cli_app():
    output_stream = io.StringIO()
    response = "This is a fixed mock response."
    mock_llm = MockLLM(response=response)
    
    with patch('sys.stdout', output_stream), \
         patch('az.az.provider_factory', return_value=mock_llm), \
         patch('prompt_toolkit.PromptSession.prompt', side_effect=["Test prompt", EOFError]), \
         patch('sys.argv', ['program_name']):
        
        main() 
        
        output = output_stream.getvalue()
        assert response in output
        assert "Bye" in output


def test_bullets_rendering():
    # Test that markdown rendering happens
    output_stream = io.StringIO()
    responses = [
        "This is the first mock response.",
        "This is the second mock response.",
        "This is the third mock response."
    ]

    mock_llm = MockLLM(response=[ f"- {response}\n\n" for response in responses]) 
    
    with patch('sys.stdout', output_stream), \
         patch('az.az.provider_factory', return_value=mock_llm), \
         patch('prompt_toolkit.PromptSession.prompt', side_effect=["Test prompt", EOFError]), \
         patch('sys.argv', ['program_name']):
        
        main() 
        
    output = output_stream.getvalue()
    print(output)
        
    for response in responses:
        assert response.rstrip() in output
    assert '•' in output


def test_help_message():
    output_stream = io.StringIO()
    mock_llm = MockLLM(response="") 
    
    with patch('sys.stdout', new=output_stream, create=True), \
         patch('az.az.provider_factory', return_value=mock_llm), \
         patch('prompt_toolkit.PromptSession.prompt', side_effect=["?\n", EOFError]), \
         patch('sys.argv', ['program_name']):
        
        main() 
        
    output = output_stream.getvalue()
    print(output)
        
    assert re.search(r'^.*Command.*Description.*$', output, re.MULTILINE)
    


def test_double_enter_does_not_call_chat_when_single_enter():
    output_stream = io.StringIO()

    input_stream = io.StringIO("twice\n\n\n\n")
    mock_llm = MockLLM(response="")
    
    with patch('sys.stdout', output_stream), \
         patch('az.az.provider_factory', return_value=mock_llm), \
         patch('sys.argv', ['program_name', '-d']), \
         create_pipe_input() as inp,  \
         patch.object(MockLLM, 'chat', wraps=mock_llm.chat) as mock_chat, \
         patch('az.az.get_input', return_value=inp):
        
        inp.send_text("test\n\nq\n")
        main() 

    output = output_stream.getvalue()
    print(output)

    # Assert that chat() is not called after single enter
    assert mock_chat.call_count == 1
        

@pytest.fixture(autouse=True, scope="function")
def mock_input():
    with create_pipe_input() as pipe_input:
        with create_app_session(input=pipe_input, output=DummyOutput()):
            yield pipe_input


def test_sample_app(mock_input):
    # TODO: not sure why I need two \n\n to get the prompt to show up
    mock_input.send_text("4\n\nq\n\n")
    response = "the response"
    mock_llm = MockLLM(response=response)
    out = StringIO()
    with patch('sys.stdout', new=out), \
        patch('sys.argv', ['program_name']), \
         patch('az.az.provider_factory', return_value=mock_llm):
        main()
    output = out.getvalue()
    print(f"out:\n\n{output}\n\n-----")
    assert response in output


@pytest.mark.skip(reason="real llm is slow. use this only as an exception, also it requires env vars")
def test_sample_app_real_llm(mock_input):
    mock_input.send_text("how much are 2 * 8?\n\nq\n\n")
    out = StringIO()
    with patch('sys.stdout', new=out), \
         patch('sys.argv', ['program_name']):
        main()
    output = out.getvalue()
    print(f"out:\n\n{output}\n\n-----")
    assert "16" in output



