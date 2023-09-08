# """ Logging framework initialization
# """

# from src.main.framework.loggingconfig import get_org_logger
# org_logger = get_org_logger()
# from src.main.framework.models import RequestModel

# class LoggingHandler:
#     def __init__(self, req: RequestModel):
#         self.req = req

#     def logger(self, log_method, msg):
#         base_msg = f"TRACK_ID: {self.req.trackingId}: "
#         base_msg += str(msg)

#         log_method(base_msg)

#     def error(self, msg):
#         self.logger(org_logger.error, msg)

#     def debug(self, msg):
#         self.logger(org_logger.debug, msg)

#     def info(self, msg):
#         self.logger(org_logger.info, msg)

#     def warn(self, msg):
#         self.logger(org_logger.warn, msg)
