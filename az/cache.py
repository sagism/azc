import json
import os
from typing import Dict, List, Set

class FileCache:
    def __init__(self, cache_file: str):
        self.cache_file = cache_file
        self.cache: Dict[str, Set[str]] = self._load_cache()

    def _load_cache(self) -> Dict[str, Set[str]]:
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                return {k: set(v) for k, v in data.items()}
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump({k: list(v) for k, v in self.cache.items()}, f)

    def get(self, key: str) -> Set[str]:
        return self.cache.get(key, set())

    def set(self, key: str, value: List[str]):
        self.cache[key] = set(value)
        self._save_cache()

    def update(self, key: str, value: List[str]):
        self.cache.setdefault(key, set()).update(value)
        self._save_cache()

    def clear(self):
        self.cache.clear()
        self._save_cache()







