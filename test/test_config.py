import pytest
from az.config import load_config, default_provider, default_model

@pytest.fixture
def config_file():
    return "config.json"

def test_load_config(config_file, tmp_path):
    # Create a temporary config file
    temp_config = tmp_path / config_file
    temp_config.write_text('{"provider": "openai", "model": "gpt-3.5-turbo"}')
    
    config = load_config(str(temp_config))
    assert isinstance(config, dict)
    assert config["provider"] == "openai"
    assert config["model"] == "gpt-3.5-turbo"

def test_load_config_file_not_found(config_file):
    config = load_config("non_existent_config.json")
    assert isinstance(config, dict)
    assert len(config) == 0

def test_default_provider(tmp_path):
    # Create a temporary config file
    temp_config = tmp_path / "test_config.json"
    temp_config.write_text('{"default-provider": "ollama"}')
    
    provider = default_provider(str(temp_config))
    assert isinstance(provider, str)
    assert provider == "ollama"

def test_default_provider_non_existent_file(tmp_path):
    # Test with non-existent file
    non_existent_config = tmp_path / "non_existent.json"
    default_prov = default_provider(str(non_existent_config))
    assert default_prov == "openai"  # Assuming "openai" is the fallback default

def test_default_model(tmp_path):
    # Create a temporary config file
    temp_config = tmp_path / "test_config.json"
    print(f"temp_config: {temp_config}")
    temp_config.write_text('{"default-provider": "openai", "default-models": {"openai": {"model":"gpt-4"}}}')
    
    model = default_model(str(temp_config))
    assert model == "gpt-4"

def test_default_model_non_existent_file(tmp_path):
    # Test with non-existent file
    non_existent_config = tmp_path / "non_existent.json"
    default_mod = default_model(str(non_existent_config))
    assert default_mod is None  # Assuming None is returned when no config file exists

def test_load_config_with_missing_fields(config_file, tmp_path):
    # Create a temporary config file with missing fields
    temp_config = tmp_path / config_file
    temp_config.write_text('{"provider": "openai"}')
    
    config = load_config(str(temp_config))
    assert isinstance(config, dict)
    assert config["provider"] == "openai"
    assert default_model(str(temp_config)) == None, f"default_model should return None if model is not specified in file {str(temp_config)}"


def test_load_config_with_invalid_json(config_file, tmp_path):
    # Create a temporary config file with invalid JSON
    temp_config = tmp_path / config_file
    temp_config.write_text('{"provider": "openai", "model":}')
    
    with pytest.raises(ValueError):  # Assuming the function raises a ValueError for invalid JSON
        load_config(str(temp_config))

