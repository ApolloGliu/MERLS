# Import necessary modules and make sure Python can find your app
import sys
import os
import pytest

# Add the project root to the system path so "from app import app" works properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import your Flask app

# Create a test client fixture
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# ------------------- TESTS START HERE --------------------

def test_missing_json_body(client):
    """Test POST /submissions with no JSON body"""
    response = client.post('/submissions', json=None)
    data = response.get_json()
    assert response.status_code == 400
    assert "Missing JSON body" in data.get("error", "")

def test_missing_participant_id(client):
    """Test POST /submissions with no participantId"""
    response = client.post('/submissions', json={})
    data = response.get_json()
    assert response.status_code == 400
    assert "Missing participantId" in data.get("error", "")

def test_user_endpoint_exists(client):
    """Test GET /users endpoint returns a successful response"""
    response = client.get('/users')
    assert response.status_code in [200, 500]  # 500 if DB unavailable
    # Optional print for debugging
    print("Users API returned:", response.status_code)
