# import logging
# import os
# from logging.config import dictConfig
# from logging import DEBUG

# _PLATFORM_FILTER_MAPPING = {
#     "lambda": "LambdaContextFilter",
#     "ec2": "Ec2ContextFilter",
#     "ecs-ec2": "EcsEc2ContextFilter",
#     "ecs-fargate": "EcsFargateContextFilter",
# }
# _DEFAULT_PLATFORM = "ecs-fargate"

# logger = logging.getLogger("orgLogger")
# logger.setLevel(os.getenv('LOGLEVEL', DEBUG))


# def configure_org_logger():
#     """
#     Convenience function to configure the root logger using
#     the default org logging architecture.
#     This includes a logging Handler that pushes logs to
#     a stage/region-specific AWS Kinesis stream,
#     a logging Formatter that ensures that logs are
#     fomatted in the expected Kibana format and a logging
#     Filter that collects contextual information based on
#     the runtime environment.
#     Collects 'LOG_LEVEL' environment variable to
#     determine the log level of the root logger.
#     Collects 'AWS_PLATFORM' environment variable to
#     determine the proper log Filter class to use.
#     Collects 'LOGGING_TEST' environment variable to
#     determine if the MockKinesisHandler should be used.
#     """
#     level = os.getenv("LOG_LEVEL", "INFO").upper()
#     if getattr(logging, level, None) is None:
#         logger.warning(f"Invalid LOG_LEVEL '{level}'. Using INFO.")
#         level = "INFO"

#     aws_platform = os.getenv("AWS_PLATFORM", _DEFAULT_PLATFORM).lower()
#     if aws_platform not in _PLATFORM_FILTER_MAPPING:
#         logger.warning(
#             f"aws platform '{aws_platform}' not supported for "
#             f"log filtering. Using default platform '{_DEFAULT_PLATFORM}' "
#             "for log filtering."
#         )
#         aws_platform = _DEFAULT_PLATFORM

#     _filter = _PLATFORM_FILTER_MAPPING[aws_platform]

#     fluent_format = {
#         "version": 1,
#         "handlers": {
#             "streamHandler": {
#                 "class": "logging.StreamHandler",
#                 "level": "INFO",
#                 "formatter": "KibanaFormatter",
#                 "filters": [f"{_filter}", "orgLoggerFilter"],
#                 "stream": "ext://sys.stdout",
#             },
#             "fluentHandler": {
#                 "class": "fluent.handler.FluentHandler",
#                 "host": "localhost",
#                 "port": 24224,
#                 "tag": "xmeligibility",
#                 "formatter": "FluentRecordFormatter",
#                 "filters": [f"{_filter}", "orgLoggerFilter"],
#                 "level": "INFO",
#             }
#         },
#         "filters": {
#             f"{_filter}": {"()": f"tpx_logging.filters.{_filter}"},
#             "orgLoggerFilter": {"()": "src.main.framework.loggingconfig.orgLoggerFilter"},
#         },
#         "formatters": {
#             "KibanaFormatter": {"()": "tpx_logging.formatters.KibanaFormatter"},
#             "FluentRecordFormatter": {"()": "tpx_logging.formatters.FluentFormatter"}
#         },
#         "root": {"handlers": ["streamHandler", "fluentHandler"], "level": level, },
#         "disable_existing_loggers": False
#     }

#     dictConfig(fluent_format)


# def get_org_logger():
#     '''
#     Configure and return org logger.
#     '''
#     configure_org_logger()
#     return logger


# class orgLoggerFilter(logging.Filter):
#     """
#     Filters out log records from 3rd-party
#     modules if they have a log-level at or below INFO
#     """

#     def filter(self, record):
#         if record.name != "orgLogger" and not record.name.startswith("tpx"):
#             return record.levelno > logging.INFO
#         return True