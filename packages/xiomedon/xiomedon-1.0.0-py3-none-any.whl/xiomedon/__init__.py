from openai_wrapper import openai_invoke 

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown version"


__all__ = ["openai_invoke","__version__"]