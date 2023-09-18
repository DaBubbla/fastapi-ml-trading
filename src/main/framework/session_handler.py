from starlette.background import BackgroundTasks

# from tpx_localization_request.auth.auth_builder import AuthBuilder
# from src.main.framework.logging import LoggingHandler
# from tpx_metrics.globals import metrics_context
# TODO: create some models
# from src.main.framework.models import RequestModel

class SessionHandler:

    def __init__(
            self,
            config: dict,
            # req_body: RequestModel = None,
            req_body = None,
            # auth_builder: AuthBuilder = None,
            # log_handler=LoggingHandler,
            # metrics_id=None,
            app=None,
            # imei: str = None,
            # phone_number: str = None
    ) -> None:

        self.req_body = req_body
        self.app = app
        # self.log_handler = log_handler(req=self.req_body)
        self.config = config
        # self.auth_builder: AuthBuilder = auth_builder or self.app.state.auth_builder
        # self.metrics_id = metrics_id if metrics_id else metrics_context.metrics[
            # "CollectMetricsInvocationId"]
        # self.imei = imei
        # self.phone_number = phone_number
