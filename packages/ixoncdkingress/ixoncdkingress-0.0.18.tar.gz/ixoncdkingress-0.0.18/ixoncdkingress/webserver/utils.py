"""
Utility functions.
"""
import json
from time import sleep
from typing import TYPE_CHECKING, Any, Optional
from urllib.parse import parse_qs

from docker import errors, from_env

from ixoncdkingress.function.api_client import ApiClient, Query
from ixoncdkingress.function.context import FunctionContext, FunctionResource
from ixoncdkingress.function.document_db_client import DocumentDBAuthentication, DocumentDBClient
from ixoncdkingress.types import FunctionArguments, FunctionLocation
from ixoncdkingress.webserver.config import Config

if TYPE_CHECKING:
    from docker.models.containers import Container

def read_qs_as_dict(in_put: bytes) -> dict[str, str]:
    """
    Reads and parses the URL query string, returns it as a dict with for each value only the first
    occurrence.
    """
    body = in_put.decode('utf-8')

    # parse_qs always returns non-empty lists!
    return {key: value[0] for (key,value) in parse_qs(body).items()}

def parse_function_location(in_put: str) -> FunctionLocation:
    """
    Parses the full function path into a module path and a function name.
    """

    function_path = in_put.split('.')

    function_name = function_path.pop()
    module_name = '.'.join(function_path)

    if not function_path:
        return 'functions', function_name

    return module_name, function_name

def _parse_context_values(context_items: dict[str, Any]) -> dict[str, Any]:
    """
    Parses expected context_items into FunctionResources
    and discards any unexpected context_items.
    """
    context_values = {}
    for context_name, context_resource in context_items.items():
        # context_values.apiApplication and .accessToken will be sent to the FunctionContext
        # but are unused, they are only used to create the ApiClient.
        if (context_name not in
                ['user', 'company', 'agent', 'asset', 'apiApplication', 'accessToken']):
            continue

        if context_resource is None:
            continue

        # accessToken is not a FunctionResource because it doesn't have
        # a publicId, name and custom field.
        if context_name == 'accessToken':
            context_values[context_name] = context_resource.get('headerValue')
            continue

        permissions = None
        if context_name in ['company', 'agent', 'asset']:
            permissions = set()
            if 'permissions' in context_resource:
                permissions.update(context_resource['permissions'])

        context_values[context_name] = FunctionResource(
            context_resource['publicId'],
            context_resource['name'],
            context_resource['custom'],
            permissions,
        )

    return context_values

def parse_json_input(
        config: Config,
        context_config: dict[str, str],
        body: str
    ) -> tuple[FunctionContext, FunctionLocation, FunctionArguments, str]:
    """
    Parses an application/json request body string into a context, function
    location and function arguments.
    """
    in_put = json.loads(body)

    function_location = parse_function_location(in_put.get('name', ''))

    # Get all context values, may be overwritten if a custom apiApplication is set
    # however this is then still needed for getting authentication values
    context_values = _parse_context_values(in_put.get('context', {}))

    context_config = context_config | in_put.get('config', {})

    api_client_kwargs = {}

    if api_application_res := context_values.get('apiApplication'):
        api_client_kwargs['api_application'] = api_application_res.public_id
    if api_company_res:= context_values.get('company'):
        api_client_kwargs['api_company'] = api_company_res.public_id
    if access_token := context_values.get('accessToken'):
        api_client_kwargs['authorization'] = access_token

    api_client = ApiClient(config.api_client_base_url, **api_client_kwargs)

    # Override the API application if it's set in context_config and not in production mode
    # and refetch custom properties of context_values for scoped custom properties.
    if not config.production_mode and (api_application_res := context_config.get('apiApplication')):
        query: Query = { 'fields': 'custom,name' }
        api_client.set_custom_api_application(api_application_res)

        # Without an access token we don't requery the custom properties
        # as the request will fail anyways.
        if context_values.get('accessToken'):
            api_data = {}
            user_res = api_client.get('MyUser', query=query)
            api_data['user'] = user_res['data']

            # Without a company we don't need to requery these properties
            # as the requests will fail anyways.
            if context_values.get('company'):
                company_res = api_client.get('MyCompany', query=query)
                api_data['company'] = company_res['data']

                if agent := context_values.get('agent'):
                    agent_res = api_client.get(
                        'Agent',
                        { 'publicId': agent.public_id },
                        query=query,
                    )
                    api_data['agent'] = agent_res['data']

                if asset := context_values.get('asset'):
                    asset_res = api_client.get(
                        'Asset',
                        { 'publicId': asset.public_id },
                        query=query,
                    )
                    api_data['asset'] = asset_res['data']

            # Overwrite existing context_values
            context_values = _parse_context_values(api_data)

    document_db_client = None
    if ((db_config := in_put.get('internalConfig', {}).get('dbConfig'))
            and context_values.get('company')
        ):
        # The database name is the public id of the company
        # The collection name is the public id of the Cloud Function template
        document_db_client = DocumentDBClient(
            db_config['uri'],
            context_values['company'].public_id,
            in_put['internalConfig']['publicId'],
            DocumentDBAuthentication(username=db_config['username'], password=db_config['password'])
        )
    elif not config.production_mode and context_values.get('company'):
        document_db_client = DocumentDBClient(
            f'mongodb://localhost:{config.document_db_port}/',
            context_values['company'].public_id,
            'cloud_function_pid',
            DocumentDBAuthentication(username='root', password='mongo-root'), # nosec # noqa: S106
            tls=False
        )

    context = FunctionContext(context_config, api_client, document_db_client, **context_values)

    function_arguments = in_put.get('arguments', {})
    created_on = in_put.get('created_on', '')

    return context, function_location, function_arguments, created_on

def setup_mongo_container(config: Config) -> Optional['Container']:
    """
    Sets up a development MongoDB when not in production mode.

    Will create a docker container named: `ixon-cloud-function-mongo`. The mongodb will be
    accessable at the configured port with user: `root` and password: `mongo-root`

    Returns the created container so that it can be removed on exit.
    """
    if config.production_mode:
        return None

    logger = config.get_logger()
    logger.info('Starting DocumentDB server')

    try:
        client = from_env()

        container: 'Container'
        try:
            container = client.containers.get('ixon-cloud-function-mongo')
            container.remove(force=True)
        except errors.NotFound:
            pass

        container = client.containers.run(
            "mongo:6.0.6-jammy",
            name='ixon-cloud-function-mongo',
            ports={'27017/tcp': config.document_db_port},
            detach=True
        )

        # Ensure database is running and user created. has to be variable because of possible
        # slow development computers of users
        retries, exit_code = 0, 1
        max_retries = 10
        while retries < max_retries and exit_code != 0:
            sleep(1 * retries)
            retries += 1
            exit_code = container.exec_run("""
                mongosh --eval 'db.getSiblingDB("admin").createUser({
                    user: "root",
                    pwd: "mongo-root",
                    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
                })'
            """).exit_code

        logger.info('DocumentDB server started successfully')

        return container
    except errors.DockerException as error:
        logger.error("\
            Exception with setting up DocumentDB. \
            Please make sure you have docker installed on your machine \
            and port %s is unused or configure a different port \
            by setting DOCUMENT_DB_PORT to an available port\
        ", config.document_db_port)
        raise error

def shutdown_mongo_container(config: Config, container: 'Container') -> None:
    """
    Tears down and removes the earlier created DocumentDB container
    """
    logger = config.get_logger()

    logger.info('Shutting down DocumentDB server')
    container.remove(force=True)
