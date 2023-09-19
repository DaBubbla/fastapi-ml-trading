import pytest
from unittest.mock import patch
from src.main.framework.config_manager import APP_CONFIG

@pytest.fixture
def mock_app_config():
    with patch.object(APP_CONFIG, 'get_configs') as patched:
        yield patched