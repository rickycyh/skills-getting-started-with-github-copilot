from copy import deepcopy
from importlib import import_module

import pytest
from fastapi.testclient import TestClient


app_module = import_module("src.app")


@pytest.fixture
def activity_data(monkeypatch):
    data = deepcopy({
        "Chess Club": {
            "description": "Play chess",
            "schedule": "Fridays",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Art Club": {
            "description": "Make art",
            "schedule": "Wednesdays",
            "max_participants": 20,
            "participants": [],
        },
        "Math Club": {
            "description": "Solve problems",
            "schedule": "Thursdays",
            "max_participants": 16,
            "participants": ["emma@mergington.edu"],
        },
    })
    monkeypatch.setattr(app_module, "activities", data)
    return data


@pytest.fixture
def client(activity_data):
    with TestClient(app_module.app) as test_client:
        yield test_client
