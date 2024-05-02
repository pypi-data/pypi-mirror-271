"""
Functions for finding and calling Cloud Functions.
"""
import importlib
import sys
from typing import Any

from pymongo.errors import OperationFailure

from ixoncdkingress.function.context import FunctionContext
from ixoncdkingress.types import FunctionArguments, FunctionLocation
from ixoncdkingress.utils import handle_exception
from ixoncdkingress.webserver.config import Config
from ixoncdkingress.webserver.response import Response


def call_function(
        config: Config, context: FunctionContext,
        function_location: FunctionLocation,
        function_kwargs: FunctionArguments,
        response: Response
    ) -> Any:
    """
    Finds, loads and calls the function specified in the body. The content_type specifies the
    format of the body.
    """

    # Get the specified module
    sys.path.insert(0, config.cbc_path)
    module = importlib.import_module(function_location[0])
    if config.production_mode is False:
        try:
            module = importlib.reload(module)
        except ImportError as error:
            handle_exception(error, response)
            return None
    del sys.path[0]

    # Get the specified function
    if hasattr(module, function_location[1]):
        function = getattr(module, function_location[1])

        # Check if it's exposed
        if getattr(function, 'exposed', False):
            try:
                return function(context, **function_kwargs)
            except OperationFailure as ex:
                if ex.details and ex.details.get('codeName'):
                    return f'Document DB operation failure: {ex.details["codeName"]}'

                return 'Document DB operation failure'


    return f"Not found, function '{'.'.join(function_location)}' does not exist or is not exposed"
