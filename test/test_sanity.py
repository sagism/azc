import io
import re
from unittest.mock import patch




from az.az import main

class MockLLM:
    def __init__(self, response):
        self.response = response

    def chat(self, prompt):
        if isinstance(self.response, list):
            for r in self.response: 
                yield r
        else:
            yield self.response

    def n_user_messages(self):
        return 0
    
    def __str__(self):
        return "MockLLM"
    
    def __repr__(self):
        return "MockLLM"



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
        assert '• '+response.rstrip() in output


def test_help_message():
    output_stream = io.StringIO()
    mock_llm = MockLLM(response="") 
    
    with patch('sys.stdout', output_stream), \
         patch('az.az.provider_factory', return_value=mock_llm), \
         patch('prompt_toolkit.PromptSession.prompt', side_effect=["?\n", EOFError]), \
         patch('sys.argv', ['program_name']):
        
        main() 
        
    output = output_stream.getvalue()
    print(output)
        
    assert re.search(r'^\s*Command\s+Description\s*$', output, re.MULTILINE)
    
    
