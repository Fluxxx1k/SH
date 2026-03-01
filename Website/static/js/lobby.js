/**
 * Лобби с real-time обновлениями
 * Следит за изменениями в списке игр, онлайн-игроках и статистике
 */

class LobbyManager {
    constructor() {
        this.games = new Map();
        this.onlinePlayers = new Set();
        this.updateInterval = 2000;
        this.cacheTimeout = 300000;
        this.maxGames = 50;
        this.lastUpdate = 0;
        this.updateQueue = [];
        this.isUpdating = false;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        
        this.init();
    }

    init() {
        this.setupDOMElements();
        this.setupEventListeners();
        this.setupSocketHandlers();
        this.startPeriodicUpdates();
        this.loadInitialData();
        
        // Подключение к WebSocket
        if (window.gameSocket) {
            window.gameSocket.connect();
        }
        
        console.log('LobbyManager инициализирован');
    }

    setupDOMElements() {
        this.elements = {
            // Статистика
            activeGamesCount: document.getElementById('activeGamesCount'),
            onlinePlayersCount: document.getElementById('onlinePlayersCount'),
            completedGamesCount: document.getElementById('completedGamesCount'),
            
            // Списки
            gamesList: document.getElementById('gamesList'),
            onlinePlayersList: document.getElementById('onlinePlayersList'),
            eventsList: document.getElementById('eventsList'),
            
            // Контролы
            gameFilter: document.getElementById('gameFilter'),
            gameSort: document.getElementById('gameSort'),
            refreshGamesBtn: document.getElementById('refreshGamesBtn'),
            createGameBtn: document.getElementById('createGameBtn'),
            clearEventsBtn: document.getElementById('clearEventsBtn'),
            
            // Быстрые действия
            quickJoinBtn: document.getElementById('quickJoinBtn'),
            randomGameBtn: document.getElementById('randomGameBtn'),
            showRulesBtn: document.getElementById('showRulesBtn'),
            
            // Модальное окно
            createGameModal: document.getElementById('createGameModal'),
            modalOverlay: document.getElementById('modalOverlay'),
            closeModalBtn: document.getElementById('closeModalBtn'),
            cancelCreateBtn: document.getElementById('cancelCreateBtn'),
            createGameForm: document.getElementById('createGameForm'),
            
            // Индикаторы загрузки
            gamesLoading: document.getElementById('gamesLoading'),
            eventsLoading: document.getElementById('eventsLoading')
        };
    }

    setupEventListeners() {
        // Фильтрация и сортировка
        if (this.elements.gameFilter) {
            this.elements.gameFilter.addEventListener('change', () => this.filterAndSortGames());
        }
        
        if (this.elements.gameSort) {
            this.elements.gameSort.addEventListener('change', () => this.filterAndSortGames());
        }
        
        // Кнопки обновления
        if (this.elements.refreshGamesBtn) {
            this.elements.refreshGamesBtn.addEventListener('click', () => this.refreshGames());
        }
        
        // Быстрые действия
        if (this.elements.quickJoinBtn) {
            this.elements.quickJoinBtn.addEventListener('click', () => this.quickJoinGame());
        }
        
        if (this.elements.randomGameBtn) {
            this.elements.randomGameBtn.addEventListener('click', () => this.joinRandomGame());
        }
        
        if (this.elements.showRulesBtn) {
            this.elements.showRulesBtn.addEventListener('click', () => this.showRules());
        }
        
        // Модальное окно создания игры
        if (this.elements.createGameBtn) {
            this.elements.createGameBtn.addEventListener('click', () => this.showCreateGameModal());
        }
        
        if (this.elements.closeModalBtn) {
            this.elements.closeModalBtn.addEventListener('click', () => this.hideCreateGameModal());
        }
        
        if (this.elements.cancelCreateBtn) {
            this.elements.cancelCreateBtn.addEventListener('click', () => this.hideCreateGameModal());
        }
        
        if (this.elements.modalOverlay) {
            this.elements.modalOverlay.addEventListener('click', () => this.hideCreateGameModal());
        }
        
        // Форма создания игры
        if (this.elements.createGameForm) {
            this.elements.createGameForm.addEventListener('submit', (e) => this.handleCreateGame(e));
        }
        
        // Очистка событий
        if (this.elements.clearEventsBtn) {
            this.elements.clearEventsBtn.addEventListener('click', () => this.clearEvents());
        }
        
        // Обработка visibilitychange для приостановки обновлений
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseUpdates();
            } else {
                this.resumeUpdates();
            }
        });
        
        // Обработка ухода со страницы
        window.addEventListener('beforeunload', () => {
            this.disconnect();
        });
        
        // Обработка ошибок
        window.addEventListener('error', (e) => {
            console.error('Ошибка в LobbyManager:', e.error);
            this.addEvent('Ошибка: ' + e.error.message, 'error');
        });
    }

    setupSocketHandlers() {
        if (!window.gameSocket) {
            console.warn('WebSocket не доступен');
            return;
        }
        
        // Обработка подключения
        window.gameSocket.on('connect', () => {
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.addEvent('Подключено к серверу', 'success');
            this.joinLobbyRoom();
        });
        
        window.gameSocket.on('disconnect', () => {
            this.isConnected = false;
            this.addEvent('Отключено от сервера', 'warning');
            this.attemptReconnect();
        });
        
        // Обновления игр
        window.gameSocket.on('game_created', (data) => {
            this.handleGameCreated(data);
        });
        
        window.gameSocket.on('game_updated', (data) => {
            this.handleGameUpdated(data);
        });
        
        window.gameSocket.on('game_deleted', (data) => {
            this.handleGameDeleted(data);
        });
        
        window.gameSocket.on('player_joined_game', (data) => {
            this.handlePlayerJoinedGame(data);
        });
        
        window.gameSocket.on('player_left_game', (data) => {
            this.handlePlayerLeftGame(data);
        });
        
        // Обновления онлайн-игроков
        window.gameSocket.on('player_online', (data) => {
            this.handlePlayerOnline(data);
        });
        
        window.gameSocket.on('player_offline', (data) => {
            this.handlePlayerOffline(data);
        });
        
        // Обновления статистики
        window.gameSocket.on('stats_updated', (data) => {
            this.handleStatsUpdated(data);
        });
        
        // Общие события
        window.gameSocket.on('lobby_event', (data) => {
            this.addEvent(data.message, data.type || 'info');
        });
    }

    joinLobbyRoom() {
        if (window.gameSocket && this.isConnected) {
            window.gameSocket.emit('join_lobby', {
                username: LOBBY_CONFIG.username
            });
        }
    }

    loadInitialData() {
        this.showLoading('games');
        this.showLoading('events');
        
        // Загрузка начальных данных с задержкой для подключения WebSocket
        setTimeout(() => {
            this.requestLobbyData();
        }, 1000);
    }

    requestLobbyData() {
        if (window.gameSocket && this.isConnected) {
            window.gameSocket.emit('get_lobby_data', {
                timestamp: this.lastUpdate
            });
        } else {
            // Fallback на HTTP запрос если WebSocket недоступен
            this.loadDataViaHTTP();
        }
    }

    loadDataViaHTTP() {
        // Загрузка данных через HTTP как fallback
        fetch('/api/lobby/data')
            .then(response => response.json())
            .then(data => {
                this.updateGamesList(data.games);
                this.updateOnlinePlayers(data.online_players);
                this.updateStats(data.stats);
                this.hideLoading('games');
                this.addEvent('Данные загружены', 'info');
            })
            .catch(error => {
                console.error('Ошибка загрузки данных:', error);
                this.addEvent('Ошибка загрузки данных', 'error');
                this.hideLoading('games');
            });
    }

    startPeriodicUpdates() {
        this.updateIntervalId = setInterval(() => {
            if (!document.hidden && this.isConnected) {
                this.processUpdateQueue();
            }
        }, this.updateInterval);
    }

    pauseUpdates() {
        if (this.updateIntervalId) {
            clearInterval(this.updateIntervalId);
        }
        if (window.gameSocket && this.isConnected) {
            window.gameSocket.emit('pause_lobby_updates');
        }
    }

    resumeUpdates() {
        this.startPeriodicUpdates();
        if (window.gameSocket && this.isConnected) {
            window.gameSocket.emit('resume_lobby_updates');
        }
        this.refreshGames(); // Обновить данные при возвращении
    }

    disconnect() {
        if (this.updateIntervalId) {
            clearInterval(this.updateIntervalId);
        }
        if (window.gameSocket && this.isConnected) {
            window.gameSocket.emit('leave_lobby');
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.addEvent('Превышено количество попыток переподключения', 'error');
            return;
        }
        
        this.reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
        
        this.addEvent(`Попытка переподключения ${this.reconnectAttempts}/${this.maxReconnectAttempts}`, 'warning');
        
        setTimeout(() => {
            if (window.gameSocket && !this.isConnected) {
                window.gameSocket.connect();
            }
        }, delay);
    }

    // Обработка событий WebSocket
    handleGameCreated(data) {
        const gameCard = this.createGameCard(data.game);
        if (this.elements.gamesList) {
            this.elements.gamesList.insertBefore(gameCard, this.elements.gamesList.firstChild);
        }
        
        this.games.set(data.game.id, data.game);
        this.addEvent(`Создана новая игра #${data.game.id}`, 'info');
        
        // Анимация новой игры
        gameCard.classList.add('new');
        setTimeout(() => gameCard.classList.remove('new'), 2000);
    }

    handleGameUpdated(data) {
        const existingGame = this.games.get(data.game.id);
        if (existingGame) {
            Object.assign(existingGame, data.game);
            this.updateGameCard(data.game);
            this.addEvent(`Игра #${data.game.id} обновлена`, 'info');
        }
    }

    handleGameDeleted(data) {
        this.games.delete(data.game_id);
        const gameCard = document.querySelector(`[data-game-id="${data.game_id}"]`);
        if (gameCard) {
            gameCard.style.opacity = '0.5';
            setTimeout(() => gameCard.remove(), 500);
        }
        this.addEvent(`Игра #${data.game_id} удалена`, 'info');
    }

    handlePlayerJoinedGame(data) {
        this.addEvent(`${data.player_name} присоединился к игре #${data.game_id}`, 'info');
        
        // Обновить счетчик игроков в реальном времени
        const gameCard = document.querySelector(`[data-game-id="${data.game_id}"]`);
        if (gameCard) {
            const playersElement = gameCard.querySelector('.info-value');
            if (playersElement) {
                const game = this.games.get(data.game_id);
                if (game) {
                    game.current_players++;
                    playersElement.textContent = `${game.current_players}/${game.max_players}`;
                }
            }
        }
    }

    handlePlayerLeftGame(data) {
        this.addEvent(`${data.player_name} покинул игру #${data.game_id}`, 'info');
        
        // Обновить счетчик игроков в реальном времени
        const gameCard = document.querySelector(`[data-game-id="${data.game_id}"]`);
        if (gameCard) {
            const playersElement = gameCard.querySelector('.info-value');
            if (playersElement) {
                const game = this.games.get(data.game_id);
                if (game && game.current_players > 0) {
                    game.current_players--;
                    playersElement.textContent = `${game.current_players}/${game.max_players}`;
                }
            }
        }
    }

    handlePlayerOnline(data) {
        this.onlinePlayers.add(data.username);
        this.updateOnlinePlayer(data.username, true);
        this.updateOnlineCount();
    }

    handlePlayerOffline(data) {
        this.onlinePlayers.delete(data.username);
        this.updateOnlinePlayer(data.username, false);
        this.updateOnlineCount();
    }

    handleStatsUpdated(data) {
        this.updateStats(data.stats);
    }

    // Методы обновления UI
    updateGamesList(games) {
        if (!this.elements.gamesList) return;
        
        // Очистить существующий список
        this.elements.gamesList.innerHTML = '';
        
        if (!games || games.length === 0) {
            this.showNoGamesMessage();
            return;
        }
        
        // Добавить игры
        games.forEach(game => {
            const gameCard = this.createGameCard(game);
            this.elements.gamesList.appendChild(gameCard);
            this.games.set(game.id, game);
        });
        
        this.filterAndSortGames();
    }

    createGameCard(game) {
        const card = document.createElement('div');
        card.className = 'game-card';
        card.dataset.gameId = game.id;
        card.dataset.gameStatus = game.status;
        
        const statusClass = this.getStatusClass(game.status);
        const statusText = this.getStatusText(game.status);
        
        card.innerHTML = `
            <div class="game-card-header">
                <h3 class="game-title">Игра #${game.id}</h3>
                <div class="game-status">
                    <span class="status-badge ${statusClass}">${statusText}</span>
                </div>
            </div>
            
            <div class="game-card-body">
                <div class="game-info">
                    <div class="info-row">
                        <span class="info-label">Создатель:</span>
                        <span class="info-value">${game.creator || 'Неизвестен'}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Игроков:</span>
                        <span class="info-value">${game.current_players || 0}/${game.max_players || 0}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Создана:</span>
                        <span class="info-value">${this.formatDate(game.created_at)}</span>
                    </div>
                    ${game.status === 'waiting' && game.current_players < game.max_players ? `
                    <div class="info-row">
                        <span class="info-label">Доступно мест:</span>
                        <span class="info-value">${game.max_players - game.current_players}</span>
                    </div>
                    ` : ''}
                </div>
                
                <div class="game-players">
                    <span class="players-label">Игроки:</span>
                    <div class="players-list">
                        ${this.renderPlayersList(game.players || [], game.max_players || 0)}
                    </div>
                </div>
            </div>
            
            <div class="game-card-actions">
                ${this.renderGameActions(game)}
            </div>
        `;
        
        return card;
    }

    renderPlayersList(players, maxPlayers) {
        let html = '';
        
        // Существующие игроки
        players.forEach(player => {
            html += `<span class="player-tag online">${player}</span>`;
        });
        
        // Пустые слоты
        const emptySlots = maxPlayers - players.length;
        for (let i = 0; i < emptySlots; i++) {
            html += '<span class="player-slot empty">+</span>';
        }
        
        return html;
    }

    renderGameActions(game) {
        if (game.status === 'waiting' && game.current_players < game.max_players) {
            return `
                <a href="/game/${game.id}" class="action-btn action-btn-primary">
                    🎮 Присоединиться
                </a>
                <button class="action-btn action-btn-info" onclick="showGameDetails('${game.id}')">
                    ℹ️ Подробности
                </button>
            `;
        } else if (game.status === 'playing') {
            return `
                <a href="/game/${game.id}" class="action-btn action-btn-secondary">
                    👁️ Наблюдать
                </a>
                <button class="action-btn action-btn-info" onclick="showGameDetails('${game.id}')">
                    ℹ️ Подробности
                </button>
            `;
        } else {
            return `
                <button class="action-btn" disabled>
                    🔒 Недоступно
                </button>
                <button class="action-btn action-btn-info" onclick="showGameDetails('${game.id}')">
                    ℹ️ Подробности
                </button>
            `;
        }
    }

    updateGameCard(game) {
        const card = document.querySelector(`[data-game-id="${game.id}"]`);
        if (!card) return;
        
        // Обновить только изменившиеся элементы
        const statusBadge = card.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.className = `status-badge ${this.getStatusClass(game.status)}`;
            statusBadge.textContent = this.getStatusText(game.status);
        }
        
        // Обновить информацию об игроках
        const playersElement = card.querySelector('.info-value');
        if (playersElement) {
            playersElement.textContent = `${game.current_players || 0}/${game.max_players || 0}`;
        }
        
        // Обновить действия
        const actionsElement = card.querySelector('.game-card-actions');
        if (actionsElement) {
            actionsElement.innerHTML = this.renderGameActions(game);
        }
        
        // Добавить анимацию обновления
        card.style.transform = 'scale(1.02)';
        setTimeout(() => {
            card.style.transform = 'scale(1)';
        }, 200);
    }

    filterAndSortGames() {
        const filter = this.elements.gameFilter ? this.elements.gameFilter.value : 'all';
        const sort = this.elements.gameSort ? this.elements.gameSort.value : 'newest';
        
        const cards = document.querySelectorAll('.game-card');
        const visibleCards = [];
        
        cards.forEach(card => {
            const gameId = card.dataset.gameId;
            const game = this.games.get(gameId);
            
            if (!game) {
                card.style.display = 'none';
                return;
            }
            
            // Фильтрация
            let shouldShow = true;
            if (filter === 'waiting' && game.status !== 'waiting') shouldShow = false;
            if (filter === 'playing' && game.status !== 'playing') shouldShow = false;
            if (filter === 'full' && game.status !== 'full') shouldShow = false;
            
            if (shouldShow) {
                visibleCards.push({ card, game });
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
        
        // Сортировка видимых карточек
        visibleCards.sort((a, b) => {
            switch (sort) {
                case 'oldest':
                    return new Date(a.game.created_at) - new Date(b.game.created_at);
                case 'players':
                    return b.game.current_players - a.game.current_players;
                case 'name':
                    return a.game.id.localeCompare(b.game.id);
                case 'newest':
                default:
                    return new Date(b.game.created_at) - new Date(a.game.created_at);
            }
        });
        
        // Переместить карточки в правильном порядке
        if (this.elements.gamesList) {
            visibleCards.forEach(({ card }) => {
                this.elements.gamesList.appendChild(card);
            });
        }
    }

    updateOnlinePlayers(players) {
        if (!this.elements.onlinePlayersList) return;
        
        this.elements.onlinePlayersList.innerHTML = '';
        
        if (!players || players.length === 0) {
            this.elements.onlinePlayersList.innerHTML = `
                <div class="no-players">
                    <div class="no-players-icon">👤</div>
                    <p>Нет других игроков онлайн</p>
                </div>
            `;
            return;
        }
        
        players.forEach(player => {
            const playerElement = document.createElement('div');
            playerElement.className = 'player-item';
            playerElement.dataset.username = player;
            
            playerElement.innerHTML = `
                <div class="player-avatar">
                    ${player[0].toUpperCase()}
                </div>
                <span class="player-name">${player}</span>
                <div class="player-status-indicator online"></div>
            `;
            
            this.elements.onlinePlayersList.appendChild(playerElement);
        });
        
        this.updateOnlineCount();
    }

    updateOnlinePlayer(username, isOnline) {
        const playerElement = document.querySelector(`[data-username="${username}"]`);
        if (playerElement) {
            const indicator = playerElement.querySelector('.player-status-indicator');
            if (indicator) {
                indicator.className = `player-status-indicator ${isOnline ? 'online' : 'offline'}`;
            }
        }
    }

    updateOnlineCount() {
        if (this.elements.onlineCount) {
            this.elements.onlineCount.textContent = this.onlinePlayers.size;
        }
    }

    updateStats(stats) {
        if (this.elements.activeGamesCount) {
            this.elements.activeGamesCount.textContent = stats.active_games || 0;
        }
        
        if (this.elements.onlinePlayersCount) {
            this.elements.onlinePlayersCount.textContent = stats.total_players || 0;
        }
        
        if (this.elements.completedGamesCount) {
            this.elements.completedGamesCount.textContent = stats.complete_games || 0;
        }
    }

    addEvent(message, type = 'info') {
        if (!this.elements.eventsList) return;
        
        const eventElement = document.createElement('div');
        eventElement.className = 'event-item';
        
        const time = new Date().toLocaleTimeString();
        
        eventElement.innerHTML = `
            <div class="event-time">${time}</div>
            <div class="event-text">${message}</div>
        `;
        
        // Добавить в начало списка
        this.elements.eventsList.insertBefore(eventElement, this.elements.eventsList.firstChild);
        
        // Ограничить количество событий
        const events = this.elements.eventsList.querySelectorAll('.event-item');
        if (events.length > 20) {
            events[events.length - 1].remove();
        }
        
        // Анимация добавления
        eventElement.style.opacity = '0';
        setTimeout(() => {
            eventElement.style.opacity = '1';
        }, 100);
    }

    clearEvents() {
        if (this.elements.eventsList) {
            this.elements.eventsList.innerHTML = `
                <div class="event-item">
                    <div class="event-time">${new Date().toLocaleTimeString()}</div>
                    <div class="event-text">События очищены</div>
                </div>
            `;
        }
    }

    // Методы действий
    refreshGames() {
        this.showLoading('games');
        this.addEvent('Обновление списка игр...', 'info');
        
        if (window.gameSocket && this.isConnected) {
            window.gameSocket.emit('refresh_games');
        } else {
            this.loadDataViaHTTP();
        }
    }

    quickJoinGame() {
        const availableGames = Array.from(this.games.values()).filter(game => 
            game.status === 'waiting' && game.current_players < game.max_players
        );
        
        if (availableGames.length === 0) {
            this.addEvent('Нет доступных игр для быстрого подключения', 'warning');
            return;
        }
        
        // Выбрать игру с наибольшим количеством игроков
        const bestGame = availableGames.reduce((best, current) => 
            current.current_players > best.current_players ? current : best
        );
        
        this.addEvent(`Быстрое подключение к игре #${bestGame.id}`, 'info');
        window.location.href = `/game/${bestGame.id}`;
    }

    joinRandomGame() {
        const availableGames = Array.from(this.games.values()).filter(game => 
            game.status === 'waiting' && game.current_players < game.max_players
        );
        
        if (availableGames.length === 0) {
            this.addEvent('Нет доступных игр', 'warning');
            return;
        }
        
        const randomGame = availableGames[Math.floor(Math.random() * availableGames.length)];
        this.addEvent(`Подключение к случайной игре #${randomGame.id}`, 'info');
        window.location.href = `/game/${randomGame.id}`;
    }

    showRules() {
        // Показать правила игры
        alert('Правила игры:\n\n1. Играют 3-8 игроков\n2. Каждый игрок голосует за действия\n3. Большинство голосов побеждает\n4. Цель - выиграть игру!');
    }

    showCreateGameModal() {
        if (this.elements.createGameModal && this.elements.modalOverlay) {
            this.elements.createGameModal.classList.add('active');
            this.elements.modalOverlay.classList.add('active');
            
            // Фокус на первом поле
            const firstInput = this.elements.createGameModal.querySelector('input');
            if (firstInput) {
                setTimeout(() => firstInput.focus(), 100);
            }
        }
    }

    hideCreateGameModal() {
        if (this.elements.createGameModal && this.elements.modalOverlay) {
            this.elements.createGameModal.classList.remove('active');
            this.elements.modalOverlay.classList.remove('active');
            
            // Очистить форму
            if (this.elements.createGameForm) {
                this.elements.createGameForm.reset();
            }
        }
    }

    handleCreateGame(event) {
        event.preventDefault();
        
        const formData = new FormData(this.elements.createGameForm);
        const gameData = {
            game_name: formData.get('game_name'),
            max_players: parseInt(formData.get('max_players')),
            password: formData.get('password'),
            private: formData.has('private')
        };
        
        this.addEvent('Создание новой игры...', 'info');
        
        if (window.gameSocket && this.isConnected) {
            window.gameSocket.emit('create_game', gameData);
        } else {
            // Fallback на HTTP запрос
            fetch('/api/games/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(gameData)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    this.addEvent('Игра создана успешно!', 'success');
                    this.hideCreateGameModal();
                    window.location.href = `/game/${result.game_id}`;
                } else {
                    this.addEvent('Ошибка создания игры: ' + result.error, 'error');
                }
            })
            .catch(error => {
                console.error('Ошибка создания игры:', error);
                this.addEvent('Ошибка создания игры', 'error');
            });
        }
    }

    // Вспомогательные методы
    showLoading(type) {
        const element = this.elements[type + 'Loading'];
        if (element) {
            element.classList.add('active');
        }
    }

    hideLoading(type) {
        const element = this.elements[type + 'Loading'];
        if (element) {
            element.classList.remove('active');
        }
    }

    showNoGamesMessage() {
        if (!this.elements.gamesList) return;
        
        this.elements.gamesList.innerHTML = `
            <div class="no-games">
                <div class="no-games-icon">🎮</div>
                <h3>Нет активных игр</h3>
                <p>Создайте новую игру или подождите, пока кто-то создаст</p>
                <button class="action-btn action-btn-primary" onclick="document.getElementById('createGameBtn').click()">
                    Создать игру
                </button>
            </div>
        `;
    }

    processUpdateQueue() {
        if (this.isUpdating || this.updateQueue.length === 0) return;
        
        this.isUpdating = true;
        const updates = this.updateQueue.splice(0, 10); // Обработать до 10 обновлений за раз
        
        updates.forEach(update => {
            try {
                update.callback();
            } catch (error) {
                console.error('Ошибка обработки обновления:', error);
            }
        });
        
        this.isUpdating = false;
        
        // Если остались обновления, обработать их в следующем цикле
        if (this.updateQueue.length > 0) {
            setTimeout(() => this.processUpdateQueue(), 50);
        }
    }

    queueUpdate(callback, priority = 0) {
        this.updateQueue.push({ callback, priority });
        this.updateQueue.sort((a, b) => b.priority - a.priority);
    }

    getStatusClass(status) {
        switch (status) {
            case 'waiting': return 'status-waiting';
            case 'playing': return 'status-playing';
            case 'full': return 'status-full';
            default: return 'status-waiting';
        }
    }

    getStatusText(status) {
        switch (status) {
            case 'waiting': return '⏳ Ожидание';
            case 'playing': return '▶️ В процессе';
            case 'full': return '🔒 Полная';
            default: return '⏳ Ожидание';
        }
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Только что';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} мин назад`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} ч назад`;
        
        return date.toLocaleDateString();
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.lobbyManager = new LobbyManager();
});

// Глобальные функции для HTML
globalThis.showGameDetails = function(gameId) {
    alert(`Подробности игры #${gameId}:\n\nФункция в разработке...`);
};