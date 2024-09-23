import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from prompt_toolkit import PromptSession
from sample_app import main
from unittest.mock import patch
from io import StringIO

@pytest.fixture(autouse=True, scope="function")
def mock_input():
    with create_pipe_input() as pipe_input:
        with create_app_session(input=pipe_input, output=DummyOutput()):
            yield pipe_input


def test_sample(mock_input):
    mock_input.send_text("test\n\nq\n")
    session = PromptSession()
    result = session.prompt("")
    assert result == "test"


def test_sample_app(mock_input):
    mock_input.send_text("4\n")
    out = StringIO()
    with patch('sys.stdout', new=out) as fake_out:
        main()
    assert out.getvalue().strip() == "4"