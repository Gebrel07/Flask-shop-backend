import pytest
from flask import Flask
from .custom_client import TestClient

from src.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app: Flask):
    client = TestClient(app)
    return client
