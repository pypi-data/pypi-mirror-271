import pytest

from src import hello


@pytest.fixture
def client():
    with hello.app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"<p>Hello, World!</p>"
