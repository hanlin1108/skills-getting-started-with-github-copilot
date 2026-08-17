"""
API endpoint tests using Arrange-Act-Assert (AAA) pattern.

Each test follows the AAA pattern to clearly separate:
- Arrange: Set up test prerequisites and fixtures
- Act: Execute the code being tested
- Assert: Verify the results match expectations

This pattern makes tests more readable, maintainable, and easier to debug.
"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_success(self, client, mock_activities_setup):
        """
        Test: Successfully retrieve all activities.
        
        Arrange: Set up test client with sample activities (via fixture).
        Act: Make GET request to /activities endpoint.
        Assert: Verify 200 status, correct response structure, and all activities returned.
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert isinstance(data["Chess Club"]["participants"], list)

    def test_get_activities_empty(self, client, monkeypatch):
        """
        Test: Handle empty activities list gracefully.
        
        Arrange: Mock activities as empty dict.
        Act: Make GET request to /activities endpoint.
        Assert: Verify 200 status and empty dict returned.
        """
        # Arrange
        monkeypatch.setattr("src.app.activities", {})

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert response.json() == {}


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, mock_activities_setup):
        """
        Test: Successfully sign up a new student for an activity.
        
        Arrange: Set up client with sample activities.
        Act: POST signup request with valid activity and new email.
        Assert: Verify 200 status, success message, and participant added.
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "david@test.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
        assert new_email in mock_activities_setup[activity_name]["participants"]

    def test_signup_already_registered(self, client, mock_activities_setup):
        """
        Test: Reject signup if student is already registered.
        
        Arrange: Get activity with existing participant, try to sign up again.
        Act: POST signup request with email already in participants.
        Assert: Verify 400 status and appropriate error message.
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "alice@test.edu"  # Already in sample_activities

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_activity_not_found(self, client, mock_activities_setup):
        """
        Test: Reject signup if activity doesn't exist.
        
        Arrange: Set up client with valid email but fake activity.
        Act: POST signup request to non-existent activity.
        Assert: Verify 404 status and "Activity not found" error.
        """
        # Arrange
        fake_activity = "Nonexistent Club"
        email = "test@test.edu"

        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestUnregisterEndpoint:
    """Tests for POST /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client, mock_activities_setup):
        """
        Test: Successfully unregister a participant from an activity.
        
        Arrange: Get activity with participants, select one to remove.
        Act: POST unregister request with valid activity and participant email.
        Assert: Verify 200 status, success message, and participant removed.
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "alice@test.edu"
        assert email_to_remove in mock_activities_setup[activity_name]["participants"]

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email_to_remove} from {activity_name}"
        assert email_to_remove not in mock_activities_setup[activity_name]["participants"]

    def test_unregister_not_registered(self, client, mock_activities_setup):
        """
        Test: Reject unregister if student is not in activity.
        
        Arrange: Get activity and email not in participants.
        Act: POST unregister request for non-participant.
        Assert: Verify 400 status and appropriate error message.
        """
        # Arrange
        activity_name = "Programming Class"
        non_participant_email = "notregistered@test.edu"
        assert non_participant_email not in mock_activities_setup[activity_name]["participants"]

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": non_participant_email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"

    def test_unregister_activity_not_found(self, client, mock_activities_setup):
        """
        Test: Reject unregister if activity doesn't exist.
        
        Arrange: Set up client with valid email but fake activity.
        Act: POST unregister request to non-existent activity.
        Assert: Verify 404 status and "Activity not found" error.
        """
        # Arrange
        fake_activity = "Nonexistent Club"
        email = "test@test.edu"

        # Act
        response = client.post(
            f"/activities/{fake_activity}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestRootRedirect:
    """Tests for GET / endpoint."""

    def test_root_redirect(self, client):
        """
        Test: Root path redirects to static HTML page.
        
        Arrange: Set up client.
        Act: Make GET request to root path without following redirects.
        Assert: Verify 307 redirect status and Location header.
        """
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
