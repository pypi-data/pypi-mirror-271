from xiomedon.openai_wrapper import invoke_openai 

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown version"


__all__ = ["invoke_openai","__version__"]