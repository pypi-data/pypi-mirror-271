import warnings

warnings.warn(
    "ixoncdkingress.cbc had been deprecated, please use ixoncdkingress.function",
    DeprecationWarning,
)

from ixoncdkingress.function.objectstorage.types import ( # noqa: E402, F401, I001
    ListPathResponse,
    PathData,
    PathMapping,
    PathResponse,
    ResourceType,
)
