from importlib import metadata

try:
    __version__ = str(metadata.version("deepstack-ai"))
except metadata.PackageNotFoundError:
    __version__ = "main"
