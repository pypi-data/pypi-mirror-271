import warnings

warnings.warn(
    "ixoncdkingress.cbc had been deprecated, please use ixoncdkingress.function",
    DeprecationWarning,
)

from ixoncdkingress.function.api_client import ApiClient # noqa: E402, F401, I001
