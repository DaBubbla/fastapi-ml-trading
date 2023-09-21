import os
import pytest
from unittest import mock
from src.main.framework.config_manager import APP_CONFIG
from fastapi.testclient import TestClient
from src.main.application import app


path = "src.main.application"


@pytest.fixture
def mock_app_config():
    with mock.patch(path, APP_CONFIG) as patched:
        patched.get_configs = mock.Mock()
        yield patched


@pytest.fixture
def mock_app():
    client = TestClient(app)
    client.state = mock.Mock()
    client.state.config = mock.Mock()
    yield client