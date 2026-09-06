import pytest
from fastapi.testclient import TestClient

from ultramedia.config import Settings
from ultramedia.main import create_app


@pytest.fixture()
def client(tmp_path):
    settings = Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        provider_mode="local",
        cors_origins="http://localhost:3000",
    )
    with TestClient(create_app(settings)) as test_client:
        yield test_client
