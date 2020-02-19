"""Proxy import to backward compatibility.
Deprecated: use direct import."""
import warnings
from tacyt_sdk.filter_model import Filter

warnings.warn("Use Filter class from tacyt_sdk.filter_model",
              category=DeprecationWarning,
              stacklevel=2)
