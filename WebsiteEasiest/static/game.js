document.addEventListener('DOMContentLoaded', function() {
    // Check if mobile device
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    // Adjust log table height for mobile
    if (isMobile) {
        const logTable = document.querySelector('.log-table');
        if (logTable) {
            logTable.style.height = '40vh';
        }
    }
    // Game initialization
    const startGameBtn = document.getElementById('startGameBtn');
    const joinGameBtn = document.getElementById('joinGameBtn');
    const deleteGameBtn = document.getElementById('deleteGameBtn');
    try {
        if (joinGameBtn) {
            joinGameBtn.addEventListener('click', function () {
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
    }
    catch (e) {
        console.error('Ошибка добавления обработчика события joinGameBtn:', e);
        alert('Ошибка: не удалось присоединиться к игре. Пожалуйста, попробуйте позже: ' + e);
    }
    try {
        if (startGameBtn) {
            startGameBtn.addEventListener('click', function () {
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
    }
    catch (e) {
        console.error('Ошибка добавления обработчика события startGameBtn:', e);
        alert('Ошибка: не удалось начать игру. Пожалуйста, попробуйте позже: ' + e);
    }
    
    try {
        if (deleteGameBtn) {
            deleteGameBtn.addEventListener('click', function () {
                if (confirm('Вы уверены, что хотите удалить игру? Это действие нельзя отменить.')) {
                    fetch(`/game/${gameId}/end`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'}
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                alert('Игра удалена!');
                                window.location.href = '/lobby';
                            } else {
                                alert('Ошибка: ' + data.message);
                            }
                        });
                }
            });
        }
    }
    catch (e) {
        console.error('Ошибка добавления обработчика события deleteGameBtn:', e);
        alert('Ошибка: не удалось удалить игру. Пожалуйста, попробуйте позже: ' + e);
    }
    
    // Update game data from server
    function updateGameData() {
        // Scroll to top of action log on mobile after update
        if (isMobile) {
            const logTable = document.querySelector('.log-table');
            if (logTable) {
                logTable.scrollTop = 0;
            }
        }
        try {
            fetch(`/game/${gameId}`)
                .then(response => response.json())
                .then(data => {
                    updateVoteLog(data.votes);
                    updatePlayerList(data.players);
                });
        }
        catch (e) {
            console.error('Ошибка обновления данных игры:', e);
            alert('Ошибка: не удалось обновить данные игры. Пожалуйста, попробуйте позже: ' + e);
        }
    }
    
    // Update vote log from server
     function updateVoteLog(votes) {
        try {
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
        catch (e) {
            console.error('Ошибка обновления лога голосов:', e);
            alert('Ошибка: не удалось обновить лог голосов. Пожалуйста, попробуйте позже: ' + e);
        }
    }
    
    // Unified vote handler
    function sendVote(type, target = null) {
        try {
            const voteData = {
                voter: username,
                vote_type: type
            };
            if (target) voteData.target_player = target;

            fetch(`/game/${gameId}/vote`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(voteData)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        updateGameData();
                        const msg = voteData.vote_type === 'player'
                            ? `Вы проголосовали за ${target}`
                            : `Ваш голос "${target}" учтен`;
                        alert(msg);
                    } else {
                        alert('Ошибка при голосовании: ' + data.message);
                    }
                });
        }
        catch (e) {
            console.error('Ошибка отправки голосования:', e);
            alert('Ошибка: не удалось отправить голос. Пожалуйста, попробуйте позже: ' + e);
        }
    }
    
    // Voting buttons
    try {
        document.querySelectorAll('.vote-btn').forEach(button => {
            button.addEventListener('click', function () {
                const vote = this.classList.contains('vote-yes') ? 'yes' :
                    this.classList.contains('vote-no') ? 'no' : 'pass';
                sendVote('YesNo', vote);
            });
        });
    }
    catch (e) {
        console.error('Ошибка добавления обработчика события vote-btn:', e);
        alert('Ошибка: не удалось добавить обработчик события vote-btn. Пожалуйста, попробуйте позже: ' + e);
    }
    
    // Player vote
    try {
        document.querySelector('.vote-player-btn').addEventListener('click', function() {
            const playerSelect = document.querySelector('.player-select');
            const selectedPlayer = playerSelect.options[playerSelect.selectedIndex].text;
            if (confirm(`Вы уверены, что хотите проголосовать за ${selectedPlayer}?`)) {
                sendVote('player', selectedPlayer);
            }
        });
    }
    catch (e) {
        console.error('Ошибка добавления обработчика события vote-player-btn:', e);
        alert('Ошибка: не удалось добавить обработчик события vote-player-btn. Пожалуйста, попробуйте позже: ' + e);
    }

    function updatePlayerList(players) {
        try {
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
        catch (e) {
            console.error('Ошибка обновления списка игроков:', e);
            alert('Ошибка: не удалось обновить список игроков. Пожалуйста, попробуйте позже: ' + e);
        }
    }
});