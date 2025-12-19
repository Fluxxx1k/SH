let currentVote = null;

function castVote(vote) {
    currentVote = vote;
    const resultDiv = document.getElementById('vote-result');
    
    // Убираем предыдущие классы
    resultDiv.className = '';
    
    switch(vote) {
        case 'yes':
            resultDiv.textContent = 'Вы проголосовали: ДА';
            resultDiv.classList.add('vote-success');
            break;
        case 'no':
            resultDiv.textContent = 'Вы проголосовали: НЕТ';
            resultDiv.classList.add('vote-fail');
            break;
        case 'abstain':
            resultDiv.textContent = 'Вы воздержались от голосования';
            resultDiv.classList.add('vote-abstain');
            break;
    }
    
    // Отправляем голос на сервер (заглушка)
    sendVoteToServer(vote);
}

function sendVoteToServer(vote) {
    // Заглушка для отправки голоса на сервер
    fetch('/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ vote: vote })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Голос отправлен:', data);
    })
    .catch(error => {
        console.error('Ошибка при отправке голоса:', error);
    });
}

function refreshLogs() {
    const refreshBtn = document.getElementById('refreshBtn');
    refreshBtn.textContent = 'Обновление...';
    refreshBtn.disabled = true;
    
    // Получаем обновленные логи
    fetch('/get_game_logs')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('game-table-container').innerHTML = data.game_table;
                console.log('Логи обновлены');
            } else {
                console.error('Ошибка при обновлении логов');
            }
        })
        .catch(error => {
            console.error('Ошибка при получении логов:', error);
        })
        .finally(() => {
            refreshBtn.textContent = 'Обновить логи';
            refreshBtn.disabled = false;
        });
}

// Автоматическое обновление каждые 5 секунд
// setInterval(refreshLogs, 5000);

// Функция для вызова из SH2 для обновления логов
function updateGameLogs(newLogs) {
    // Эта функция может быть вызвана из SH2 для обновления логов
    console.log('Обновление логов из SH2:', newLogs);
    
    // Если есть новые логи, можно отправить их на сервер
    if (newLogs && Array.isArray(newLogs)) {
        fetch('/update_game_logs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ logs: newLogs })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Ответ сервера:', data);
            // Обновляем отображение
            refreshLogs();
        })
        .catch(error => {
            console.error('Ошибка при обновлении логов из SH2:', error);
            // Все равно обновляем отображение
            refreshLogs();
        });
    } else {
        // Просто обновляем отображение
        refreshLogs();
    }
}

// Экспортируем функцию для использования из других скриптов
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { updateGameLogs };
}