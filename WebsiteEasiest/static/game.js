document.addEventListener('DOMContentLoaded', function() {
    // Game initialization
    const startGameBtn = document.getElementById('startGameBtn');
    const joinGameBtn = document.getElementById('joinGameBtn');
    
    if (joinGameBtn) {
        joinGameBtn.addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите присоединиться к игре?')) {
                fetch(`/game/${gameId}/join`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Вы успешно присоединились к игре!');
                        location.reload();
                    } else {
                        alert('Ошибка: ' + data.message);
                    }
                });
            }
        });
    }
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
                updateGameData();
            } else {
                        alert('Ошибка: ' + data.message);
                    }
                });
            }
        });
    }
    
    // Update game data from server
    function updateGameData() {
        fetch(`/game/${gameId}`)
            .then(response => response.json())
            .then(data => {
                updateVoteLog(data.votes);
                updatePlayerList(data.players);
            });
    }
    
    // Update vote log from server
     function updateVoteLog(votes) {
         const logTable = document.querySelector('.log-table');
         logTable.innerHTML = '';
         
         votes.forEach(vote => {
                    const logEntry = document.createElement('div');
                    logEntry.className = 'log-entry';
                    
                    if (vote.target) {
                        logEntry.textContent = `${vote.voter} проголосовал за ${vote.target}`;
                    } else {
                        logEntry.textContent = `${vote.voter} проголосовал ${vote.type}`;
                    }
                    
                    logTable.appendChild(logEntry);
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
                updateGameData();
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