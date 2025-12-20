import requests
import time

# Test the refresh functionality
session = requests.Session()

# First, login
login_response = session.post('http://127.0.0.1:20050/login', data={
    'username': 'test_user',
    'password': 'test_password'
})

print(f"Login status: {login_response.status_code}")

# Get the lobby page
lobby_response = session.get('http://127.0.0.1:20050/lobby')
print(f"Lobby status: {lobby_response.status_code}")

# Test the API endpoint directly
games_response = session.get('http://127.0.0.1:20050/api/games')
print(f"Games API status: {games_response.status_code}")
if games_response.status_code == 200:
    data = games_response.json()
    print(f"Games data: {data}")
else:
    print(f"Games API error: {games_response.text}")

print("Refresh button should now work - it calls refreshGames() which calls loadAvailableGames()")