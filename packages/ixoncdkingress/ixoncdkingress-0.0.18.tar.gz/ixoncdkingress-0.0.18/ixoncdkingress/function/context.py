"""
Context.
"""
from inspect import _empty, signature
from typing import Any

from ixoncdkingress.function.api_client import ApiClient
from ixoncdkingress.function.document_db_client import DocumentDBClient


class FunctionResource:
    """
    Describes an IXAPI resource.
    """
    public_id: str
    name: str
    custom_properties: dict[str, Any]
    permissions: set[str] | None

    def __init__(
            self,
            public_id: str,
            name: str,
            custom_properties: dict[str, Any],
            permissions: set[str] | None
        ) -> None:
        self.public_id = public_id
        self.name = name
        self.custom_properties = custom_properties
        self.permissions = permissions

    def __repr__(self) -> str:
        return (
            '<FunctionResource'
            f' public_id={self.public_id},'
            f' name={self.name},'
            f' custom_properties={self.custom_properties!r},'
            f' permissions={self.permissions!r},'
            f'>'
        )

class FunctionContext:
    """
    The context for a Cloud Function.
    """
    config: dict[str, str]
    api_client: ApiClient
    document_db_client: DocumentDBClient | None = None
    user: FunctionResource | None = None
    company: FunctionResource | None = None
    asset: FunctionResource | None = None
    agent: FunctionResource | None = None

    @property
    def agent_or_asset(self) -> FunctionResource:
        """
        Return either an Agent or an Asset resource, depending on what's available. If both are
        available in the context, returns the Asset resource.
        """
        if self.asset:
            return self.asset

        assert self.agent
        return self.agent

    def __init__(
            self,
            config: dict[str, str],
            api_client: ApiClient,
            document_db_client: DocumentDBClient | None = None,
            user: FunctionResource | None = None,
            company: FunctionResource | None = None,
            asset: FunctionResource | None = None,
            agent: FunctionResource | None = None,
            **kwargs: Any
        ) -> None:
        del kwargs

        self.config = config
        self.api_client = api_client
        self.document_db_client = document_db_client
        self.user = user
        self.company = company
        self.asset = asset
        self.agent = agent

    def __repr__(self) -> str:
        return (
            f'<FunctionContext'
            f' config={self.config!r},'
            f' api_client={self.api_client!r},'
            f' document_db_client={self.document_db_client!r},'
            f' user={self.user!r},'
            f' company={self.company!r},'
            f' asset={self.asset!r},'
            f' agent={self.agent!r},'
            f'>'
        )

    @staticmethod
    def expose(function: Any) -> Any:
        """
        Decorator to mark a function as an exposed endpoint.
        """
        sig = signature(function)

        if not sig.parameters:
            raise Exception('Function has no argument for FunctionContext')

        # If the first function argument has a type annotation it should be of FunctionContext
        context_param = sig.parameters[next(iter(sig.parameters))]
        if (context_param.annotation is not _empty
                and context_param.annotation is not FunctionContext):
            raise Exception('First function parameter should be of type FunctionContext')

        function.exposed = True

        return function
