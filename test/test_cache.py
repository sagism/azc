import pytest
import tempfile
import os


from az.cache import FileCache

@pytest.fixture
def file_cache():
    temp_dir = tempfile.mkdtemp()
    cache_file = os.path.join(temp_dir, 'test_cache.json')
    cache = FileCache(cache_file)
    yield cache
    os.remove(cache_file)
    os.rmdir(temp_dir)

def test_set_and_get(file_cache):
    file_cache.set('test_key', ['value1', 'value2'])
    assert file_cache.get('test_key') == {'value1', 'value2'}

def test_update(file_cache):
    file_cache.set('test_key', ['value1'])
    file_cache.update('test_key', ['value2', 'value3'])
    assert file_cache.get('test_key') == {'value1', 'value2', 'value3'}

def test_clear(file_cache):
    file_cache.set('test_key', ['value1'])
    file_cache.clear()
    assert file_cache.get('test_key') == set()

def test_persistence(file_cache):
    file_cache.set('test_key', ['value1'])
    cache_file = file_cache.cache_file
    del file_cache
    new_cache = FileCache(cache_file)
    assert new_cache.get('test_key') == {'value1'}