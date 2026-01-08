// WebSocket connection for lobby updates
const lobbySocket = new WebSocket(`ws://${window.location.host}/lobby`);

lobbySocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'games_list') {
        updateGamesList(data.games);
    } else if (data.type === 'game_created') {
        document.getElementById('current-game').innerHTML = `
            <h3>Your Game (${data.game_id})</h3>
            <p>Waiting for players... (1/5)</p>
            <p>You are the game creator</p>
        `;
    } else if (data.type === 'game_joined') {
        const gameInfo = document.getElementById('current-game');
        if (gameInfo) {
            const match = gameInfo.innerHTML.match(/\((\d+)\/5\)/);
            if (match) {
                const count = parseInt(match[1]) + 1;
                gameInfo.innerHTML = gameInfo.innerHTML.replace(
                    /\d+\/5/, `${count}/5`
                );
            }
        }
    } else if (data.type === 'player_joined') {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.innerHTML = `${data.player} joined the game (${data.players_count}/5)`;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    } else if (data.type === 'game_started') {
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
            <p>Players: ${game.players.length}/5</p>
            <div class="game-meta">
                <span>Status: ${game.status}</span>
                ${game.status === 'waiting' ? 
                    `<button onclick="joinGame('${game.id}')">Join</button>` : 
                    ''}
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