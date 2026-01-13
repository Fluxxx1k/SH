document.addEventListener('DOMContentLoaded', function() {
    // Game initialization
    const startGameBtn = document.getElementById('startGameBtn');
    if (startGameBtn) {
        startGameBtn.addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите начать игру?')) {
                fetch(`/game/${gameId}/start`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Игра начата!');
                        updateVoteLog();
                    } else {
                        alert('Ошибка: ' + data.message);
                    }
                });
            }
        });
    }
    
    // Update vote log from server
    function updateVoteLog() {
        fetch(`/game/${gameId}`)
            .then(response => response.json())
            .then(data => {
                const logTable = document.querySelector('.log-table');
                logTable.innerHTML = '';
                
                data.votes.forEach(vote => {
                    const logEntry = document.createElement('div');
                    logEntry.className = 'log-entry';
                    
                    if (vote.target) {
                        logEntry.textContent = `${vote.voter} проголосовал за ${vote.target}`;
                    } else {
                        logEntry.textContent = `${vote.voter} проголосовал ${vote.type}`;
                    }
                    
                    logTable.appendChild(logEntry);
                });
            });
    }
    
    // Unified vote handler
    function sendVote(type, targetPlayer = null) {
        const voteData = {
            voter: username,
            vote_type: type
        };
        if (targetPlayer) voteData.target_player = targetPlayer;
        
        fetch(`/game/${gameId}/vote`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(voteData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateVoteLog();
                const msg = targetPlayer 
                    ? `Вы проголосовали за ${targetPlayer}` 
                    : `Ваш голос "${type}" учтен`;
                alert(msg);
            } else {
                alert('Ошибка при голосовании: ' + data.message);
            }
        });
    }
    
    // Voting buttons
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function() {
            const voteType = this.classList.contains('vote-yes') ? 'yes' : 
                            this.classList.contains('vote-no') ? 'no' : 'pass';
            sendVote(voteType);
        });
    });
    
    // Player vote
    document.querySelector('.vote-player-btn').addEventListener('click', function() {
        const playerSelect = document.querySelector('.player-select');
        const selectedPlayer = playerSelect.options[playerSelect.selectedIndex].text;
        if (confirm(`Вы уверены, что хотите проголосовать за ${selectedPlayer}?`)) {
            sendVote('player', selectedPlayer);
        }
    });

    // Socket.IO connection for real-time updates
    const socket = io(`/game/${gameId}`);
    
    socket.on('connect', () => {
        console.log('Connected to game room');
    });
    
    socket.on('vote_update', (data) => {
        const logTable = document.querySelector('.log-table');
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        
        if (data.target) {
            logEntry.textContent = `${data.voter} проголосовал за ${data.target}`;
        } else {
            logEntry.textContent = `${data.voter} проголосовал ${data.type}`;
        }
        
        logTable.appendChild(logEntry);
        logTable.scrollTop = logTable.scrollHeight;
    });
    
    function updatePlayerList(players) {
        const playerList = document.querySelector('.players');
        playerList.innerHTML = '';
        
        players.forEach(player => {
            const playerElement = document.createElement('li');
            playerElement.className = 'player';
            
            const nameSpan = document.createElement('span');
            nameSpan.className = 'player-name';
            nameSpan.textContent = player.name;
            
            const roleSpan = document.createElement('span');
            roleSpan.className = 'player-role';
            roleSpan.textContent = player.role;
            
            playerElement.appendChild(nameSpan);
            playerElement.appendChild(roleSpan);
            playerList.appendChild(playerElement);
        });
    }
});