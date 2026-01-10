document.addEventListener('DOMContentLoaded', function() {
    // Voting buttons functionality
    const voteButtons = document.querySelectorAll('.vote-btn');
    voteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const voteType = this.classList.contains('vote-yes') ? 'yes' : 
                            this.classList.contains('vote-no') ? 'no' : 'pass';
            
            // Send vote to server
            fetch(`/game/${gameId}/vote`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ vote: voteType })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`Ваш голос "${voteType}" учтен`);
                } else {
                    alert('Ошибка при голосовании: ' + data.message);
                }
            });
        });
    });

    // Player vote functionality
    const votePlayerBtn = document.querySelector('.vote-player-btn');
    votePlayerBtn.addEventListener('click', function() {
        const playerSelect = document.querySelector('.player-select');
        const selectedPlayerId = playerSelect.value;
        const selectedPlayerName = playerSelect.options[playerSelect.selectedIndex].text;
        
        if (confirm(`Вы уверены, что хотите проголосовать за ${selectedPlayerName}?`)) {
            fetch(`/game/${gameId}/vote_player`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ player_id: selectedPlayerId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`Вы проголосовали за ${selectedPlayerName}`);
                } else {
                    alert('Ошибка при голосовании: ' + data.message);
                }
            });
        }
    });

    // WebSocket connection for real-time updates
    const socket = new WebSocket(`ws://${window.location.host}/game/${gameId}/ws`);
    
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.type === 'action') {
            // Update action log
            const logTable = document.querySelector('.log-table');
            const newRow = document.createElement('div');
            newRow.textContent = `${data.time} - ${data.player}: ${data.action}`;
            logTable.appendChild(newRow);
            logTable.scrollTop = logTable.scrollHeight;
        } else if (data.type === 'player_update') {
            // Update player list
            updatePlayerList(data.players);
        }
    };
    
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