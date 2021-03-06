# Third Party Module Import
import pytest

# Python Module Import
import tempfile

# Apps Module Import
from apps import create_app
from apps.models.database import init_db, init_create_user


@pytest.fixture(scope='session')
def client():
    app = create_app()
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
            init_create_user()
        yield client
