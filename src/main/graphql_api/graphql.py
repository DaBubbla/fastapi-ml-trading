# """ Graphql application module
# """

# # import logging
# from inspect import isawaitable
# from typing import (
#     Any, Callable, Dict,
#     List, Optional, Type,
#     Union, cast
# )

# import graphene
# from graphene_federation import build_schema
# from graphql import ExecutionContext, GraphQLError, Middleware, graphql
# from starlette.background import BackgroundTasks
# from starlette.requests import HTTPConnection, Request
# from starlette.responses import JSONResponse

# from src.main.graphql_api.query import Query
# try:
#     # graphql-core==3.2.*
#     from graphql import GraphQLFormattedError
#     from src.main.graphql_api.graphql_error_handler import format_error
# except ImportError:
#     # graphql-core==3.1.*
#     from graphql import format_error

#     GraphQLFormattedError = Dict[str, Any]



# ContextValue = Union[Any, Callable[[HTTPConnection], Any]]
# RootValue = Any

# async def _get_operation_from_request(
#         request: Request,
# ) -> Union[Dict[str, Any], List[Any]]:
#     content_type = request.headers.get("Content-Type", "").split(";")[0]
#     if content_type == "application/json":
#         try:
#             return cast(Union[Dict[str, Any], List[Any]], await request.json())
#         except (TypeError, ValueError):
#             raise ValueError("Request body is not a valid JSON")
#     else:
#         raise ValueError("Content-type must be application/json")


# class GraphQLApplication:
#     def __init__(
#             self,
#             schema: graphene.Schema,
#             context_value: ContextValue = None,
#             root_value: RootValue = None,
#             middleware: Optional[Middleware] = None,
#             error_formatter: Callable[[GraphQLError],
#                                       GraphQLFormattedError] = format_error,
#             logger_name: Optional[str] = None,
#             execution_context_class: Optional[Type[ExecutionContext]] = None,
#     ):
#         self.schema = schema
#         self.context_value = context_value
#         self.root_value = root_value
#         self.error_formatter = error_formatter
#         self.middleware = middleware
#         self.execution_context_class = execution_context_class
#         self.logger = logging.getLogger(logger_name or __name__)

#     async def _get_context_value(self, request: HTTPConnection) -> Any:
#         if callable(self.context_value):
#             context = self.context_value(request)
#             if isawaitable(context):
#                 context = await context
#             return context
#         else:
#             return self.context_value or {
#                 "request": request,
#                 "background": BackgroundTasks(),
#             }

#     async def _handle_http_request(self, request: Request) -> JSONResponse:
#         try:
#             operations = await _get_operation_from_request(request)
#         except ValueError as e:
#             return JSONResponse({"errors": [e.args[0]]}, status_code=400)

#         if isinstance(operations, list):
#             return JSONResponse(
#                 {"errors": ["This server does not support batching yet."]}, status_code=400
#             )
#         else:
#             operation = operations

#         query = operation["query"]
#         variable_values = operation.get("variables")
#         operation_name = operation.get("operationName")
#         context_value = await self._get_context_value(request)

#         result = await graphql(
#             self.schema.graphql_schema,
#             source=query,
#             context_value=context_value,
#             root_value=self.root_value,
#             middleware=self.middleware,
#             variable_values=variable_values,
#             operation_name=operation_name,
#             execution_context_class=self.execution_context_class,
#         )

#         response: Dict[str, Any] = {"data": result.data}

#         if result.errors:
#             for error in result.errors:
#                 if error.original_error:
#                     self.logger.error(
#                         "An exception occurred in resolvers",
#                         exc_info=error.original_error,
#                     )
#             response["errors"] = [
#                 self.error_formatter(error) for error in result.errors
#             ]

#         return JSONResponse(
#             response,
#             status_code=200,
#             background=context_value.get("background"),
#         )


# GRAPHQL_APP = GraphQLApplication(
#     schema=build_schema(query=Query, auto_camelcase=False),
#     logger_name="orgLogger"
# )
