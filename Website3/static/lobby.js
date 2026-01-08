// WebSocket connection for lobby updates
const lobbySocket = new WebSocket(`ws://${window.location.host}/lobby`);

lobbySocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'games_list') {
        updateGamesList(data.games);
    } else if (data.type === 'game_created') {
        window.location.href = `/game/${data.game_id}`;
    } else if (data.type === 'game_joined') {
        window.location.href = `/game/${data.game_id}`;
    }
};

document.getElementById('createGameBtn').addEventListener('click', () => {
    lobbySocket.send(JSON.stringify({
        type: 'create_game'
    }));
});

document.getElementById('joinGameBtn').addEventListener('click', () => {
    const gameCode = document.getElementById('gameCode').value.trim();
    if (gameCode) {
        lobbySocket.send(JSON.stringify({
            type: 'join_game',
            game_id: gameCode
        }));
    }
});

function updateGamesList(games) {
    const gamesContainer = document.getElementById('gamesContainer');
    
    if (games.length === 0) {
        gamesContainer.innerHTML = '<p>No games available. Create one!</p>';
        return;
    }
    
    gamesContainer.innerHTML = games.map(game => 
        `<div class="game-item">
            <h3>Game ${game.id}</h3>
            <p>Players: ${game.players.length}/${game.max_players}</p>
            <div class="game-meta">
                <span>Status: ${game.status}</span>
                <button onclick="joinGame('${game.id}')">Join</button>
            </div>
        </div>`
    ).join('');
}

function joinGame(gameId) {
    lobbySocket.send(JSON.stringify({
        type: 'join_game',
        game_id: gameId
    }));
}