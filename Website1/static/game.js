// Глобальные переменные игры
let currentVote = null;
let selectedPlayer = null;
let gameData = {};

// Функции для работы с голосованием
function castVote(vote) {
    // Снимаем активное состояние со всех кнопок
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Делаем выбранную кнопку активной
    const voteButtons = {
        'yes': document.querySelector('.vote-yes'),
        'abstain': document.querySelector('.vote-abstain'),
        'no': document.querySelector('.vote-no')
    };
    
    if (voteButtons[vote]) {
        voteButtons[vote].classList.add('active');
        currentVote = vote;
        
        // Логируем действие
        addGameLog(`Вы выбрали голос: ${getVoteText(vote)}`);
    }
}

function getVoteText(vote) {
    const voteTexts = {
        'yes': 'За',
        'abstain': 'Пас',
        'no': 'Против'
    };
    return voteTexts[vote] || vote;
}

function confirmVote() {
    if (!currentVote) {
        alert('Пожалуйста, выберите вариант голосования');
        return;
    }
    
    // Отключаем кнопки во время отправки
    const confirmBtn = document.querySelector('.confirm-vote-btn');
    const originalText = confirmBtn.textContent;
    confirmBtn.textContent = 'Отправка...';
    confirmBtn.disabled = true;
    
    // Отправляем голос на сервер
    fetch('/api/game/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            vote: currentVote,
            game_name: getGameName()
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            addGameLog(`Ваш голос "${getVoteText(currentVote)}" принят`);
            
            // Сбрасываем выбор
            currentVote = null;
            document.querySelectorAll('.vote-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Обновляем данные игры
            updateGameData(data.game_data);
        } else {
            alert('Ошибка при отправке голоса: ' + (data.error || 'Неизвестная ошибка'));
        }
    })
    .catch(error => {
        console.error('Ошибка при отправке голоса:', error);
        alert('Произошла ошибка при отправке голоса. Попробуйте еще раз.');
    })
    .finally(() => {
        confirmBtn.textContent = originalText;
        confirmBtn.disabled = false;
    });
}

// Функции для выбора игрока
function confirmPlayerSelection() {
    const select = document.getElementById('playerSelect');
    selectedPlayer = select.value;
    
    if (!selectedPlayer) {
        alert('Пожалуйста, выберите игрока');
        return;
    }
    
    // Отключаем кнопки во время отправки
    const confirmBtn = document.querySelector('.confirm-selection-btn');
    const originalText = confirmBtn.textContent;
    confirmBtn.textContent = 'Отправка...';
    confirmBtn.disabled = true;
    
    // Отправляем выбор на сервер
    fetch('/api/game/select_player', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            selected_player: selectedPlayer,
            game_name: getGameName()
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            addGameLog(`Вы выбрали игрока: ${selectedPlayer}`);
            
            // Сбрасываем выбор
            select.value = '';
            selectedPlayer = null;
            
            // Обновляем данные игры
            updateGameData(data.game_data);
        } else {
            alert('Ошибка при выборе игрока: ' + (data.error || 'Неизвестная ошибка'));
        }
    })
    .catch(error => {
        console.error('Ошибка при выборе игрока:', error);
        alert('Произошла ошибка при выборе игрока. Попробуйте еще раз.');
    })
    .finally(() => {
        confirmBtn.textContent = originalText;
        confirmBtn.disabled = false;
    });
}

// Функции для работы с логом игры
function addGameLog(message) {
    const logContainer = document.getElementById('gameLog');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = `[${getCurrentTime()}] ${message}`;
    
    logContainer.appendChild(logEntry);
    
    // Прокручиваем к последнему сообщению
    logContainer.scrollTop = logContainer.scrollHeight;
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('ru-RU');
}

// Функции для обновления данных игры
function updateGameData(data) {
    gameData = data;
    
    // Обновляем информацию на странице
    if (data.current_turn) {
        document.getElementById('currentTurn').textContent = data.current_turn;
    }
    
    if (data.game_phase) {
        document.getElementById('gamePhase').textContent = data.game_phase;
    }
    
    if (data.player_count) {
        document.getElementById('playerCount').textContent = data.player_count;
    }
    
    // Обновляем таблицу игры
    updateGameTable(data);
}

function updateGameTable(data) {
    const tableElement = document.getElementById('gameTable');
    
    // Здесь будет логика обновления таблицы в зависимости от данных игры
    // Пока просто показываем, что данные обновились
    if (data.last_action) {
        addGameLog(`Данные игры обновлены: ${data.last_action}`);
    }
}

// Вспомогательные функции
function getGameName() {
    // Получаем название игры из URL или данных страницы
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1] || 'unknown';
}

// Функция для загрузки данных игры
function loadGameData() {
    fetch(`/api/game/${getGameName()}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateGameData(data.game_data);
                addGameLog('Данные игры загружены');
            } else {
                addGameLog('Ошибка загрузки данных игры');
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке данных игры:', error);
            addGameLog('Ошибка соединения с сервером');
        });
}

// Функция для обновления списка игроков
function updatePlayerList(players) {
    const select = document.getElementById('playerSelect');
    const currentValue = select.value;
    
    // Очищаем текущие опции, кроме первой
    while (select.options.length > 1) {
        select.remove(1);
    }
    
    // Добавляем новых игроков
    players.forEach(player => {
        if (player !== getCurrentUsername()) {
            const option = document.createElement('option');
            option.value = player;
            option.textContent = player;
            select.appendChild(option);
        }
    });
    
    // Восстанавливаем выбор, если игрок все еще в списке
    if (currentValue && players.includes(currentValue)) {
        select.value = currentValue;
    }
}

function getCurrentUsername() {
    // Получаем имя текущего пользователя из DOM или данных страницы
    const welcomeElement = document.querySelector('.welcome-message');
    return welcomeElement ? welcomeElement.textContent : 'unknown';
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    addGameLog('Страница игры загружена');
    
    // Загружаем начальные данные игры
    loadGameData();
    
    // Устанавливаем автоматическое обновление каждые 5 секунд
    setInterval(loadGameData, 5000);
    
    // Добавляем обработчики событий
    setupEventListeners();
});

function setupEventListeners() {
    // Обработчик изменения выбора игрока
    const playerSelect = document.getElementById('playerSelect');
    if (playerSelect) {
        playerSelect.addEventListener('change', function() {
            selectedPlayer = this.value;
            if (selectedPlayer) {
                addGameLog(`Выбран игрок: ${selectedPlayer}`);
            }
        });
    }
    
    // Обработчики для клавиатуры
    document.addEventListener('keydown', function(event) {
        // Горячие клавиши для голосования
        switch(event.key) {
            case '1':
                castVote('yes');
                break;
            case '2':
                castVote('abstain');
                break;
            case '3':
                castVote('no');
                break;
            case 'Enter':
                if (event.ctrlKey) {
                    event.preventDefault();
                    if (currentVote) {
                        confirmVote();
                    }
                }
                break;
        }
    });
}

// Функции для работы с WebSocket (если потребуется)
function connectWebSocket() {
    // Здесь будет логика подключения к WebSocket для реального времени
    // Пока заглушка
    console.log('WebSocket connection not implemented yet');
}

// Экспортируем функции для глобального использования
window.castVote = castVote;
window.confirmVote = confirmVote;
window.confirmPlayerSelection = confirmPlayerSelection;