function coloring(text) {
    let new_text = ''
    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        if (char === 'B') {
            new_text += '<span style="color: green;">' + char + '</span>';
        } else if (char === 'R') {
            new_text += '<span style="color: red;">' + char + '</span>';
        } else if (char === 'V' || char === 'P') {
            new_text += '<span style="color: violet;">' + char + '</span>';
        } else if (char === 'X') {
            new_text += char;
        } else {
            new_text += '<span style="color: darkorange;">' + char + '</span>';
        }
    }
    return new_text;
}


function processLogs(logData) {
    console.log(logData)
    if(!logData.success) {
        alert(logData.message)
    }
    logData = logData.logs;
    const logTable = document.querySelector('.log-table');
    logTable.innerHTML = '';
    
    const table = document.createElement('table');
    table.className = 'log-table-content';
    
    // Create table header
    const headerRow = document.createElement('tr');
    ['President', 'Chancellor', 'CPS', 'CCS', "CCP", "CPSA", 'SPECIAL'].forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);
    
    // Process each log entry
    logData.forEach(log => {
        const row = document.createElement('tr');

        // Player
        const playerCell = document.createElement('td');
        if(log.prs !== undefined) {
            playerCell.innerHTML = '<span style="color: cyan;">' + (players[log.prs]?.name ||  log.prs)   +'</span>';
        }
        row.appendChild(playerCell);
        
        // Target player
        const targetCell = document.createElement('td');
        if(log.cnc !== undefined) {
            targetCell.innerHTML = '<span style="color:' + (log.special === undefined ? 'yellow' : 'magenta') + ';">' +  (players[log.cnc]?.name || log.cnc)  + '</span>';

        }
        row.appendChild(targetCell);
        
        // President's cards
        const cards_president_said = document.createElement('td');
        if(log.cps !== undefined) {
            cards_president_said.innerHTML = coloring(log.cps);
        }
        row.appendChild(cards_president_said);

        // Chancellor's cards
        const cards_chancellor_said = document.createElement('td');
        if(log.ccs !== undefined) {
            cards_chancellor_said.innerHTML = coloring(log.ccs);
        }
        row.appendChild(cards_chancellor_said);

        // Chancellor's card
        const card_chancellor_placed = document.createElement('td');
        if(log.ccp !== undefined) {
            card_chancellor_placed.innerHTML = coloring(log.ccp);
        }
        row.appendChild(card_chancellor_placed);

        const cards_president_said_after = document.createElement('td');
        if(log.cpsa !== undefined) {
            cards_president_said_after.innerHTML = coloring(log.cpsa);
        }
        row.appendChild(cards_president_said_after);

        // Event type
        const eventCell = document.createElement('td');
        if(log.special !== undefined) {
        eventCell.innerHTML = log.special;
        }
        row.appendChild(eventCell);

        table.appendChild(row);
    });
    
    logTable.appendChild(table);
}

// Add event listener for refresh button
document.getElementById('refreshLogsBtn')?.addEventListener('click', () => {
    fetch(`/game/${gameId}/logs`)
        .then(response => response.json())
        .then(data => processLogs(data))
        .catch(error => console.error('Error fetching logs:', error));
});