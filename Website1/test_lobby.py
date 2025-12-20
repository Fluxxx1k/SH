import requests

# Create a session to maintain cookies
session = requests.Session()

# Login first
login_data = {
    'username': 'test_user',
    'password': 'test_password'
}
response = session.post('http://127.0.0.1:20050/login', data=login_data)
print('Login response:', response.status_code)

# Now access lobby
response = session.get('http://127.0.0.1:20050/lobby')
print('Lobby access after login:', response.status_code)

# Check if games are in the response
if 'test_game' in response.text:
    print('SUCCESS: test_game found in lobby page!')
    
    # Look for the game item structure
    if 'game-item' in response.text:
        print('SUCCESS: Game items are being rendered!')
    else:
        print('WARNING: No game items found in HTML')
        
    # Show a snippet of the games section
    start = response.text.find('<div class="available-games">')
    if start != -1:
        end = response.text.find('</div>', start + 1000)
        if end != -1:
            print('Games section snippet:')
            print(response.text[start:end+6])
else:
    print('INFO: test_game not found in lobby page')
    print('Looking for no games message...')
    if 'Нет доступных игр' in response.text:
        print('Found "No games available" message')
    else:
        print('No games message not found')