import warnings

warnings.warn(
    "ixoncdkingress.cbc had been deprecated, please use ixoncdkingress.function",
    DeprecationWarning,
)

from ixoncdkingress.function.document_db_client import (  # noqa: E402, F401, I001
    DocumentDBAuthentication,
    DocumentDBClient,
    DocumentType,
    TIMEOUT,
)
