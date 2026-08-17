"""
Pytest configuration and fixtures for API tests.
Provides test client and sample data fixtures using AAA pattern.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Create a TestClient for API testing.
    Arrange: Set up the test client for all tests.
    
    The TestClient allows testing FastAPI apps without running a live server.
    Scope: function (new instance for each test).
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture: Provide fresh sample activity data for each test.
    Arrange: Create test data that's isolated per test.
    
    Prevents cross-test contamination by providing independent data.
    Scope: function (new copy for each test).
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["alice@test.edu", "bob@test.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["charlie@test.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }


@pytest.fixture
def mock_activities_setup(sample_activities, monkeypatch):
    """
    Fixture: Temporarily replace app's activities dict with test data.
    Arrange: Inject test data into the app for isolated testing.
    
    This fixture uses monkeypatch to replace the activities dictionary
    in src.app module with sample_activities. The original is automatically
    restored after each test completes.
    
    Scope: function (isolated per test).
    Returns: The sample_activities dict for use in assertions.
    """
    monkeypatch.setattr("src.app.activities", sample_activities)
    return sample_activities
