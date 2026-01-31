import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity_success():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/participants/{email}")

def test_signup_duplicate():
    email = "testdupe@mergington.edu"
    activity = "Programming Class"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/participants/{email}")

def test_remove_participant_success():
    email = "removeuser@mergington.edu"
    activity = "Gym Class"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

def test_remove_participant_not_found():
    email = "notfound@mergington.edu"
    activity = "Gym Class"
    # Ensure user is not signed up
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_remove_activity_not_found():
    response = client.delete("/activities/NonexistentActivity/participants/someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
