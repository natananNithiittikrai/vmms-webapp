import pytest
from flask.testing import FlaskClient

from vmms_webapp.app import create_app
from vmms_webapp.database.database_service import DatabaseService


@pytest.fixture(scope="session")
def database_service() -> DatabaseService:
    return DatabaseService("sqlite://", default_populate=False)


@pytest.fixture(scope="session")
def client() -> FlaskClient:
    app = create_app(DatabaseService("sqlite://"))
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app.test_client()
