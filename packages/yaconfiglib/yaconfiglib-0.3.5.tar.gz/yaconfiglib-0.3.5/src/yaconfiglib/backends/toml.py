import re

try:
    import tomllib as toml
except ImportError:
    import toml  # type: ignore

from pathlib_next import Path

from yaconfiglib.backends.base import ConfigBackend

__all__ = ["TomlConfig"]


class TomlConfig(ConfigBackend):
    PATHNAME_REGEX = re.compile(r".*\.toml$", re.IGNORECASE)

    def load(self, path: Path, encoding: str, **kwargs):
        return toml.loads(path.read_text(encoding=encoding or self.DEFAULT_ENCODING))
