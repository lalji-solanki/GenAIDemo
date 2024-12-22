import pytest
from app import app

# Test for the Flask application
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data  # Check for HTML structure

def test_get_response(client, mocker):
    """Test the /get_response endpoint."""
    
    # Mocking the chat_with_gemini function to avoid calling the actual API
    mock_response = "This is a mock response"
    mocker.patch('app.chat_with_gemini', return_value=mock_response)
    
    # Send a POST request to the /get_response endpoint
    response = client.post('/get_response', data={'user_message': 'Hello'})
    
    # Check that the response status code is 200
    assert response.status_code == 200
    
    # Check that the response contains the mocked bot response
    json_data = response.get_json()
    assert 'bot_response' in json_data
    assert json_data['bot_response'] == mock_response
