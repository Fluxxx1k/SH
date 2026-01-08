// JavaScript для лобби Secret Hitler

// Показать модальное окно создания игры
function showCreateGameModal() {
    document.getElementById('createGameModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

// Закрыть модальное окно создания игры
function closeCreateGameModal() {
    document.getElementById('createGameModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('createGameForm').reset();
}

// Показать модальное окно присоединения к игре
function showJoinGameModal() {
    document.getElementById('joinGameModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

// Закрыть модальное окно присоединения к игре
function closeJoinGameModal() {
    document.getElementById('joinGameModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('joinGameForm').reset();
}

// Обновление списка игр
function refreshGames() {
    loadAvailableGames();
}

// Закрытие модальных окон при клике вне их
document.addEventListener('DOMContentLoaded', function() {
    const createModal = document.getElementById('createGameModal');
    const joinModal = document.getElementById('joinGameModal');
    
    window.addEventListener('click', function(event) {
        if (event.target === createModal) {
            closeCreateGameModal();
        }
        if (event.target === joinModal) {
            closeJoinGameModal();
        }
    });
    
    // Закрытие при нажатии Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            if (createModal.style.display === 'block') {
                closeCreateGameModal();
            }
            if (joinModal.style.display === 'block') {
                closeJoinGameModal();
            }
        }
    });
});

// Обработка формы создания игры
document.addEventListener('DOMContentLoaded', function() {
    const createGameForm = document.getElementById('createGameForm');
    
    if (createGameForm) {
        createGameForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const gameData = {
                game_name: formData.get('game_name'),
                game_password: formData.get('game_password') || '',
                max_players: formData.get('max_players')
            };
            
            // Валидация
            if (!gameData.game_name || gameData.game_name.trim().length === 0) {
                alert('Пожалуйста, введите название игры');
                return;
            }
            
            if (gameData.max_players < 5 || gameData.max_players > 10) {
                alert('Количество игроков должно быть от 5 до 10');
                return;
            }
            
            // Отправка данных на сервер
            createGame(gameData);
        });
    }
});

// Обработка формы присоединения к игре
document.addEventListener('DOMContentLoaded', function() {
    const joinGameForm = document.getElementById('joinGameForm');
    
    if (joinGameForm) {
        joinGameForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const joinData = {
                game_name: formData.get('game_name'),
                game_password: formData.get('game_password') || ''
            };
            
            // Валидация
            if (!joinData.game_name || joinData.game_name.trim().length === 0) {
                alert('Пожалуйста, введите название игры');
                return;
            }
            
            // Отправка данных на сервер
            joinGame(joinData);
        });
    }
});

// Функция создания игры
function createGame(gameData) {
    // Показать индикатор загрузки
    const submitButton = document.querySelector('#createGameForm button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Создание...';
    submitButton.disabled = true;
    
    fetch('/create_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(gameData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Игра успешно создана!');
            closeCreateGameModal();
            loadAvailableGames(); // Обновить список игр
        } else {
            alert('Ошибка: ' + (data.error || 'Неизвестная ошибка'));
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при создании игры. Попробуйте еще раз.');
    })
    .finally(() => {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    });
}

// Функция присоединения к игре
function joinGame(joinData) {
    // Показать индикатор загрузки
    const submitButton = document.querySelector('#joinGameForm button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Присоединение...';
    submitButton.disabled = true;
    
    fetch('/join_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(joinData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Вы успешно присоединились к игре!');
            closeJoinGameModal();
            // Перенаправление в игру
            window.location.href = '/games/' + joinData.game_name;
        } else {
            alert('Ошибка: ' + (data.error || 'Неизвестная ошибка'));
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при присоединении к игре. Попробуйте еще раз.');
    })
    .finally(() => {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    });
}

// Загрузка доступных игр
function loadAvailableGames() {
    // Получаем реальные данные с сервера
    fetch('/api/games')
        .then(response => response.json())
        .then(data => {
            const gamesList = document.getElementById('gamesList');
            
            if (data.success && data.games && data.games.length > 0) {
                gamesList.innerHTML = data.games.map(game => {
                    const [name, currentPlayers, maxPlayers, status, hasPassword] = game;
                    return `
                        <div class="game-item" data-game-name="${name}">
                            <div class="game-name">${name}</div>
                            <div class="game-info">
                                <span class="game-status">Статус: ${status === 'waiting' ? 'Ожидание игроков' : 'В процессе'}</span>
                                <span class="game-password-status">${hasPassword ? '🔒' : '🔓'}</span>
                            </div>
                            <div class="game-players">
                                <span class="player-count">Игроки: ${currentPlayers}/${maxPlayers}</span>
                                <button class="join-btn" onclick="quickJoinGame('${name}', ${hasPassword})">Присоединиться</button>
                            </div>
                        </div>
                    `;
                }).join('');
            } else {
                gamesList.innerHTML = `
                    <div class="no-games-message">
                        <p>Нет доступных игр. Создайте новую игру!</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке игр:', error);
            showNotification('Ошибка при загрузке списка игр', 'error');
        });
}

// Быстрое присоединение к игре
function quickJoinGame(gameName, hasPassword) {
    if (hasPassword) {
        const password = prompt(`Введите пароль для игры "${gameName}":`);
        if (password === null) return;
        
        const joinData = {
            game_name: gameName,
            game_password: password
        };
        joinGame(joinData);
    } else {
        const joinData = {
            game_name: gameName,
            game_password: ''
        };
        joinGame(joinData);
    }
}

// Загрузка списка игр при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadAvailableGames();
});

// Обработка ошибок и предупреждений
function showNotification(message, type = 'info') {
    // Создать уведомление
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Стили для уведомления
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? 'linear-gradient(45deg, #8B0000, #DC143C)' : 'linear-gradient(45deg, #4169E1, #1E90FF)'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        max-width: 300px;
        animation: slideIn 0.3s ease;
    `;
    
    // Добавить анимацию
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Удалить уведомление через 5 секунд
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Предотвращение утечки памяти при уходе со страницы
window.addEventListener('beforeunload', function() {
    // Очистить интервалы
    const intervals = window.setInterval(function() {}, 0);
    for (let i = 0; i < intervals; i++) {
        window.clearInterval(i);
    }
});