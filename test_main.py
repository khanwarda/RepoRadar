"""
PROJECT: Advanced GitHub CLI - Test File
PURPOSE: To automatically test our main.py code and ensure it works correctly without us manually checking it.
"""

# Import the specific function we want to test from our main.py file
from main import fetch_user_data

def test_valid_user():
    """
    TEST 1: Check if fetching a real user works.
    We give it 'octocat' and 'assert' (claim/check) that the data is NOT empty,
    and that the login name inside the data is actually 'octocat'.
    """
    print("\nRunning Test 1: Valid User...")
    data = fetch_user_data("octocat")
    
    # Assert checks if a condition is True. If it's False, the test fails (Red).
    assert data is not None, "Error: Data should not be None for a valid user."
    assert data["login"] == "octocat", "Error: The login name should match 'octocat'."

def test_invalid_user():
    """
    TEST 2: Check if fetching a fake user correctly handles the error.
    We use a guaranteed fake name. Since our main.py handles 404 errors by returning None,
    we 'assert' that the result MUST be None.
    """
    print("\nRunning Test 2: Invalid User...")
    # Using a very random name that definitely doesn't exist
    fake_username = "this_user_definitely_does_not_exist_9999"
    data = fetch_user_data(fake_username)
    
    # We expect our function to return None when it hits a 404 error
    assert data is None, "Error: Data should be None for a non-existent user."