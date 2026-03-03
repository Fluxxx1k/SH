/**
 * Упрощенное основное JavaScript приложение
 * Все данные загружаются через API, минимальная логика
 */

class SimpleApp {
    constructor() {
        this.currentPage = window.location.pathname;
        this.isAuthenticated = false;
        this.username = null;
        this.socket = null;
        
        this.init();
    }

    init() {
        this.setupAuthCheck();
        this.setupNavigation();
        this.setupPageSpecificLogic();
        
        console.log('SimpleApp инициализирован');
    }

    // Проверка аутентификации
    async setupAuthCheck() {
        try {
            const response = await fetch('/api/auth/status');
            const data = await response.json();
            
            this.isAuthenticated = data.authenticated;
            this.username = data.username;
            
            this.updateAuthUI();
        } catch (error) {
            console.error('Ошибка проверки аутентификации:', error);
        }
    }

    // Обновление UI в зависимости от аутентификации
    updateAuthUI() {
        const usernameDisplay = document.getElementById('usernameDisplay');
        const loginLink = document.getElementById('loginLink');
        const registerLink = document.getElementById('registerLink');
        const logoutLink = document.getElementById('logoutLink');
        const floatingAction = document.getElementById('floatingAction');
        
        if (this.isAuthenticated && usernameDisplay) {
            usernameDisplay.textContent = this.username;
            usernameDisplay.style.display = 'inline';
            loginLink.style.display = 'none';
            registerLink.style.display = 'none';
            logoutLink.style.display = 'inline';
            if (floatingAction) floatingAction.style.display = 'block';
            
            // Обработчик выхода
            if (logoutLink) {
                logoutLink.onclick = async (e) => {
                    e.preventDefault();
                    await this.logout();
                };
            }
        } else {
            if (usernameDisplay) usernameDisplay.style.display = 'none';
            if (loginLink) loginLink.style.display = 'inline';
            if (registerLink) registerLink.style.display = 'inline';
            if (logoutLink) logoutLink.style.display = 'none';
            if (floatingAction) floatingAction.style.display = 'none';
        }
    }

    // Выход из системы
    async logout() {
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                this.isAuthenticated = false;
                this.username = null;
                this.updateAuthUI();
                window.location.href = '/';
            }
        } catch (error) {
            console.error('Ошибка выхода:', error);
        }
    }

    // Настройка навигации
    setupNavigation() {
        // Динамическая загрузка страниц
        const loadPageContent = async (path) => {
            try {
                const response = await fetch(path);
                if (response.ok) {
                    const html = await response.text();
                    document.getElementById('mainContent').innerHTML = html;
                    this.setupPageSpecificLogic();
                }
            } catch (error) {
                console.error('Ошибка загрузки страницы:', error);
            }
        };

        // Обработка кликов по ссылкам
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'A' && e.target.href.startsWith(window.location.origin)) {
                e.preventDefault();
                const path = e.target.getAttribute('href');
                window.history.pushState({}, '', path);
                loadPageContent(path);
            }
        });
    }

    // Настройка логики для конкретной страницы
    setupPageSpecificLogic() {
        const path = window.location.pathname;
        
        switch (path) {
            case '/':
                this.setupIndexPage();
                break;
            case '/login':
                this.setupLoginPage();
                break;
            case '/register':
                this.setupRegisterPage();
                break;
            case '/lobby':
                this.setupLobbyPage();
                break;
            default:
                if (path.startsWith('/game/')) {
                    this.setupGamePage();
                }
        }
    }

    // Настройка главной страницы
    setupIndexPage() {
        this.loadGameStats();
        this.loadActiveGames();
        this.setupConnectionStatus();
        
        // Обновление каждые 10 секунд
        setInterval(() => {
            this.loadGameStats();
            this.loadActiveGames();
        }, 10000);
    }

    // Загрузка статистики игр
    async loadGameStats() {
        try {
            // Простая имитация статистики для демонстрации
            const stats = {
                active_games: Math.floor(Math.random() * 10) + 5,
                total_players: Math.floor(Math.random() * 50) + 20,
                complete_games: Math.floor(Math.random() * 100) + 50
            };
            
            document.getElementById('activeGamesCount').textContent = stats.active_games;
            document.getElementById('onlinePlayersCount').textContent = stats.total_players;
            document.getElementById('completedGamesCount').textContent = stats.complete_games;
            
        } catch (error) {
            console.error('Ошибка загрузки статистики:', error);
        }
    }

    // Загрузка активных игр
    async loadActiveGames() {
        try {
            const response = await fetch('/api/games');
            const data = await response.json();
            
            const gamesPreview = document.getElementById('gamesPreview');
            const showAllGames = document.getElementById('showAllGames');
            
            if (data.games && data.games.length > 0) {
                gamesPreview.innerHTML = data.games.slice(0, 6).map(game => `
                    <div class="game-preview-card" data-game-id="${game.id}">
                        <div class="game-preview-header">
                            <h3>Игра #${game.id}</h3>
                            <span class="game-status-badge status-${game.status}">
                                ${game.status === 'waiting' ? '⏳ Ожидание' : '▶️ В процессе'}
                            </span>
                        </div>
                        
                        <div class="game-preview-info">
                            <div class="info-item">
                                <span class="info-label">Создатель:</span>
                                <span class="info-value">${game.creator}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Игроков:</span>
                                <span class="info-value">${game.current_players}/${game.max_players}</span>
                            </div>
                            <div class="info-players">
                                ${game.players.map(player => `<span class="player-tag">${player}</span>`).join('')}
                            </div>
                        </div>
                        
                        <div class="game-preview-actions">
                            ${this.isAuthenticated ? 
                                `<a href="/game/${game.id}" class="action-btn action-btn-small">
                                    ${game.status === 'waiting' && game.current_players < game.max_players ? '🎮 Присоединиться' : '👁️ Наблюдать'}
                                </a>` :
                                `<a href="/login" class="action-btn action-btn-small">🔐 Войти чтобы играть</a>`
                            }
                        </div>
                    </div>
                `).join('');
                
                if (data.games.length > 6) {
                    showAllGames.style.display = 'block';
                }
            } else {
                gamesPreview.innerHTML = `
                    <div class="no-games-message">
                        <div class="no-games-icon">🎮</div>
                        <h3>Сейчас нет активных игр</h3>
                        <p>Станьте первым, кто создаст новую игру!</p>
                        ${this.isAuthenticated ? 
                            '<a href="/lobby" class="action-btn action-btn-primary">➕ Создать игру</a>' :
                            '<a href="/register" class="action-btn action-btn-primary">🎯 Зарегистрироваться</a>'
                        }
                    </div>
                `;
            }
            
        } catch (error) {
            console.error('Ошибка загрузки игр:', error);
        }
    }

    // Настройка статуса подключения
    setupConnectionStatus() {
        const updateStatus = () => {
            const statusIndicator = document.getElementById('statusIndicator');
            const statusText = document.getElementById('statusText');
            
            if (statusIndicator && statusText) {
                statusIndicator.className = 'status-indicator connected';
                statusText.textContent = 'Подключено';
            }
        };
        
        updateStatus();
        setInterval(updateStatus, 5000);
    }

    // Настройка страницы входа
    setupLoginPage() {
        const loginForm = document.getElementById('loginForm');
        if (!loginForm) return;
        
        loginForm.onsubmit = async (e) => {
            e.preventDefault();
            
            const formData = new FormData(loginForm);
            const data = {
                username: formData.get('username'),
                password: formData.get('password')
            };
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    this.isAuthenticated = true;
                    this.username = result.username;
                    window.location.href = '/';
                } else {
                    this.showError(result.error || 'Ошибка входа');
                }
            } catch (error) {
                console.error('Ошибка входа:', error);
                this.showError('Ошибка соединения с сервером');
            }
        };
    }

    // Настройка страницы регистрации
    setupRegisterPage() {
        const registerForm = document.getElementById('registerForm');
        if (!registerForm) return;
        
        registerForm.onsubmit = async (e) => {
            e.preventDefault();
            
            const formData = new FormData(registerForm);
            const data = {
                username: formData.get('username'),
                email: formData.get('email'),
                password: formData.get('password'),
                confirmPassword: formData.get('confirmPassword')
            };
            
            if (data.password !== data.confirmPassword) {
                this.showError('Пароли не совпадают');
                return;
            }
            
            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: data.username,
                        email: data.email,
                        password: data.password
                    })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    this.isAuthenticated = true;
                    this.username = result.username;
                    window.location.href = '/';
                } else {
                    this.showError(result.error || 'Ошибка регистрации');
                }
            } catch (error) {
                console.error('Ошибка регистрации:', error);
                this.showError('Ошибка соединения с сервером');
            }
        };
    }

    // Настройка страницы лобби
    setupLobbyPage() {
        if (!this.isAuthenticated) {
            window.location.href = '/login';
            return;
        }
        
        this.loadLobbyGames();
        this.setupCreateGameModal();
        
        // Обновление каждые 5 секунд
        setInterval(() => {
            this.loadLobbyGames();
        }, 5000);
    }

    // Загрузка игр для лобби
    async loadLobbyGames() {
        try {
            const response = await fetch('/api/games');
            const data = await response.json();
            
            const gamesList = document.getElementById('gamesList');
            
            if (data.games && data.games.length > 0) {
                gamesList.innerHTML = data.games.map(game => `
                    <div class="game-card" data-game-id="${game.id}">
                        <div class="game-info">
                            <h3>Игра #${game.id}</h3>
                            <div class="game-details">
                                <span>Создатель: ${game.creator}</span>
                                <span>Игроков: ${game.current_players}/${game.max_players}</span>
                                <span class="status-${game.status}">${game.status === 'waiting' ? 'Ожидание' : 'В процессе'}</span>
                            </div>
                        </div>
                        <div class="game-actions">
                            <a href="/game/${game.id}" class="action-btn action-btn-small">
                                ${game.status === 'waiting' && game.current_players < game.max_players ? 'Присоединиться' : 'Наблюдать'}
                            </a>
                        </div>
                    </div>
                `).join('');
            } else {
                gamesList.innerHTML = `
                    <div class="no-games-message">
                        <div class="no-games-icon">🎮</div>
                        <h3>Нет доступных игр</h3>
                        <p>Создайте новую игру или подождите других игроков</p>
                    </div>
                `;
            }
            
        } catch (error) {
            console.error('Ошибка загрузки игр лобби:', error);
        }
    }

    // Настройка модального окна создания игры
    setupCreateGameModal() {
        const createGameBtn = document.getElementById('createGameBtn');
        const createGameModal = document.getElementById('createGameModal');
        const closeModal = document.getElementById('closeModal');
        const cancelCreateGame = document.getElementById('cancelCreateGame');
        const createGameForm = document.getElementById('createGameForm');
        
        if (!createGameBtn || !createGameModal) return;
        
        createGameBtn.onclick = () => {
            createGameModal.style.display = 'block';
        };
        
        closeModal.onclick = () => {
            createGameModal.style.display = 'none';
        };
        
        cancelCreateGame.onclick = () => {
            createGameModal.style.display = 'none';
        };
        
        createGameForm.onsubmit = async (e) => {
            e.preventDefault();
            
            const formData = new FormData(createGameForm);
            const maxPlayers = parseInt(formData.get('max_players'));
            
            try {
                const response = await fetch('/api/games', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ max_players: maxPlayers })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    window.location.href = `/game/${result.game_id}`;
                } else {
                    this.showError(result.error || 'Ошибка создания игры');
                }
            } catch (error) {
                console.error('Ошибка создания игры:', error);
                this.showError('Ошибка соединения с сервером');
            }
        };
    }

    // Настройка страницы игры
    setupGamePage() {
        if (!this.isAuthenticated) {
            window.location.href = '/login';
            return;
        }
        
        const gameId = window.location.pathname.split('/').pop();
        this.setupWebSocket(gameId);
        this.loadGameData(gameId);
        this.setupGameControls(gameId);
    }

    // Настройка WebSocket
    setupWebSocket(gameId) {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('WebSocket подключен');
            this.socket.emit('join_game', { game_id: gameId });
        });
        
        this.socket.on('chat_message', (data) => {
            this.addChatMessage(data);
        });
        
        this.socket.on('player_joined', (data) => {
            this.loadGameData(gameId);
        });
        
        this.socket.on('player_left', (data) => {
            this.loadGameData(gameId);
        });
    }

    // Загрузка данных игры
    async loadGameData(gameId) {
        try {
            const response = await fetch(`/api/games/${gameId}`);
            const game = await response.json();
            
            if (response.ok) {
                this.updateGameUI(game);
            } else {
                console.error('Игра не найдена');
            }
        } catch (error) {
            console.error('Ошибка загрузки данных игры:', error);
        }
    }

    // Обновление UI игры
    updateGameUI(game) {
        document.getElementById('gameStatus').textContent = 
            game.status === 'waiting' ? 'Ожидание игроков' : 'Игра идет';
        document.getElementById('gamePlayers').textContent = 
            `${game.current_players}/${game.max_players}`;
        
        const playersList = document.getElementById('playersList');
        playersList.innerHTML = game.players.map(player => `
            <div class="player-item">
                <div class="player-avatar">${player[0].toUpperCase()}</div>
                <span class="player-name">${player}</span>
                ${player === game.creator ? '<span class="creator-badge">Создатель</span>' : ''}
            </div>
        `).join('');
        
        // Показать кнопку начала игры для создателя
        if (game.creator === this.username && game.status === 'waiting' && game.current_players >= 2) {
            document.getElementById('startGameBtn').style.display = 'block';
        }
    }

    // Настройка управления игрой
    setupGameControls(gameId) {
        // Отправка сообщений в чат
        const chatInput = document.getElementById('chatInput');
        const sendMessageBtn = document.getElementById('sendMessageBtn');
        
        const sendMessage = () => {
            const message = chatInput.value.trim();
            if (message && this.socket) {
                this.socket.emit('chat_message', {
                    game_id: gameId,
                    message: message
                });
                chatInput.value = '';
            }
        };
        
        if (sendMessageBtn) {
            sendMessageBtn.onclick = sendMessage;
        }
        
        if (chatInput) {
            chatInput.onkeypress = (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            };
        }
        
        // Кнопка покинуть игру
        const leaveGameBtn = document.getElementById('leaveGameBtn');
        if (leaveGameBtn) {
            leaveGameBtn.onclick = () => {
                if (this.socket) {
                    this.socket.emit('leave_game', { game_id: gameId });
                }
                window.location.href = '/lobby';
            };
        }
    }

    // Добавление сообщения в чат
    addChatMessage(data) {
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            const messageElement = document.createElement('div');
            messageElement.className = 'chat-message';
            messageElement.innerHTML = `
                <span class="message-author">${data.username}:</span>
                <span class="message-text">${data.message}</span>
            `;
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Показать ошибку
    showError(message) {
        const errorElement = document.getElementById('errorMessage') || 
                             document.getElementById('createGameError');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            setTimeout(() => {
                errorElement.style.display = 'none';
            }, 5000);
        }
    }
}

// Инициализация приложения при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.app = new SimpleApp();
});