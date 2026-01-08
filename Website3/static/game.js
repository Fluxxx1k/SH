// WebSocket connection for real-time game updates
const socket = new WebSocket(`ws://${window.location.host}/game`);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'role_assignment':
            document.getElementById('roleInfo').innerHTML = `
                <p>You are: <strong>${data.role}</strong></p>
                ${data.party ? `<p>Party: ${data.party}</p>` : ''}
            `;
            break;
            
        case 'players_update':
            updatePlayersList(data.players);
            break;
            
        case 'government_track':
            updateGovernmentTrack(data.track);
            break;
            
        case 'game_action':
            showGameAction(data.action, data.options);
            break;
    }
};

function updatePlayersList(players) {
    const playersList = document.querySelector('.players-list');
    playersList.innerHTML = players.map(player => 
        `<div class="player-card">
            <h3>${player.username}</h3>
            ${player.role ? `<p>Role: ${player.role}</p>` : ''}
        </div>`
    ).join('');
}

function updateGovernmentTrack(track) {
    const trackElement = document.querySelector('.government-track');
    trackElement.innerHTML = track.map((item, index) => 
        `<div class="track-item ${item.active ? 'active' : ''}">
            <span>${index + 1}</span>
            <span>${item.president || ''}</span>
            <span>${item.chancellor || ''}</span>
            <span>${item.policy || ''}</span>
        </div>`
    ).join('');
}

function showGameAction(action, options) {
    const actionsElement = document.querySelector('.actions');
    actionsElement.innerHTML = `
        <p>${action}</p>
        ${options ? options.map(option => 
            `<button onclick="handleAction('${option}')">${option}</button>`
        ).join('') : ''}
    `;
}

function handleAction(action) {
    socket.send(JSON.stringify({
        type: 'player_action',
        action: action
    }));
}