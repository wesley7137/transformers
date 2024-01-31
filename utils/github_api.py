import requests


def make_api_request(method, endpoint, headers=None, payload=None):
    """Make an API request to the GitHub API"""
    url = f"https://api.github.com/{endpoint}"
    response = requests.request(method, url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def authenticate(access_token):
    """Authenticate with the GitHub API"""
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def parse_response(response):
    """Parse the API response"""
    return response.json()


# Additional functions can be added as needed for specific API interactions
