/**
 * JavaScript для главной страницы с real-time обновлениями
 * Сохраняет стиль WebsiteEasiest и добавляет современные функции
 */

class IndexManager {
    constructor() {
        this.updateInterval = INDEX_CONFIG.updateInterval || 5000;
        this.cacheTimeout = INDEX_CONFIG.cacheTimeout || 300000;
        this.isAuthenticated = INDEX_CONFIG.isAuthenticated;
        this.username = INDEX_CONFIG.username;
        
        this.cache = new Map();
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
        this.checkConnectionStatus();
        
        console.log('IndexManager инициализирован');
    }

    setupDOMElements() {
        this.elements = {
            activeGamesCount: document.getElementById('activeGamesCount'),
            onlinePlayersCount: document.getElementById('onlinePlayersCount'),
            completedGamesCount: document.getElementById('completedGamesCount'),
            gamesPreview: document.getElementById('gamesPreview'),
            connectionStatus: document.getElementById('connectionStatus'),
            statusIndicator: document.getElementById('statusIndicator'),
            statusText: document.getElementById('statusText'),
            serverStatusIndicator: document.getElementById('serverStatusIndicator'),
            serverStatusText: document.getElementById('serverStatusText'),
            serverResponseTime: document.getElementById('serverResponseTime')
        };
    }

    setupEventListeners() {
        // Обработка видимости вкладки
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseUpdates();
            } else {
                this.resumeUpdates();
            }
        });

        // Обработка событий для игровых карт
        if (this.elements.gamesPreview) {
            this.elements.gamesPreview.addEventListener('click', (e) => {
                const gameCard = e.target.closest('.game-preview-card');
                if (gameCard) {
                    this.handleGameCardClick(gameCard);
                }
            });
        }

        // Обработка изменения размера окна
        window.addEventListener('resize', this.debounce(() => {
            this.handleResize();
        }, 250));
    }

    setupSocketHandlers() {
        if (!window.gameSocket) {
            console.warn('WebSocket не доступен');
            return;
        }

        window.gameSocket.on('connect', () => {
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.updateConnectionStatus('connected');
            this.loadInitialData();
            console.log('Подключено к серверу');
        });

        window.gameSocket.on('disconnect', () => {
            this.isConnected = false;
            this.updateConnectionStatus('disconnected');
            console.log('Отключено от сервера');
        });

        window.gameSocket.on('reconnecting', (attempt) => {
            this.updateConnectionStatus('reconnecting', attempt);
            console.log(`Попытка переподключения ${attempt}`);
        });

        window.gameSocket.on('reconnect_failed', () => {
            this.updateConnectionStatus('error');
            console.error('Не удалось переподключиться');
        });

        // Обработка игровых событий
        window.gameSocket.on('game_created', (data) => {
            this.queueUpdate(() => {
                this.handleGameCreated(data);
            });
        });

        window.gameSocket.on('game_updated', (data) => {
            this.queueUpdate(() => {
                this.handleGameUpdated(data);
            });
        });

        window.gameSocket.on('game_deleted', (data) => {
            this.queueUpdate(() => {
                this.handleGameDeleted(data);
            });
        });

        window.gameSocket.on('player_online', (data) => {
            this.queueUpdate(() => {
                this.handlePlayerOnline(data);
            });
        });

        window.gameSocket.on('player_offline', (data) => {
            this.queueUpdate(() => {
                this.handlePlayerOffline(data);
            });
        });

        window.gameSocket.on('stats_updated', (data) => {
            this.queueUpdate(() => {
                this.handleStatsUpdated(data);
            });
        });
    }

    startPeriodicUpdates() {
        // Периодическое обновление статистики
        this.statsInterval = setInterval(() => {
            if (document.hidden) return;
            this.updateStats();
        }, this.updateInterval);

        // Периодическое обновление списка игр
        this.gamesInterval = setInterval(() => {
            if (document.hidden) return;
            this.updateGamesList();
        }, this.updateInterval * 2);

        // Проверка статуса сервера
        this.serverCheckInterval = setInterval(() => {
            this.checkServerStatus();
        }, 30000); // Каждые 30 секунд
    }

    pauseUpdates() {
        console.log('Обновления приостановлены');
        if (this.statsInterval) clearInterval(this.statsInterval);
        if (this.gamesInterval) clearInterval(this.gamesInterval);
    }

    resumeUpdates() {
        console.log('Обновления возобновлены');
        this.startPeriodicUpdates();
        this.loadInitialData();
    }

    loadInitialData() {
        this.updateStats();
        this.updateGamesList();
        this.checkServerStatus();
    }

    updateStats() {
        const cacheKey = 'stats';
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            this.renderStats(cached.data);
            return;
        }

        // Получение статистики с сервера
        this.fetchStats()
            .then(stats => {
                this.cache.set(cacheKey, {
                    data: stats,
                    timestamp: Date.now()
                });
                this.renderStats(stats);
            })
            .catch(error => {
                console.error('Ошибка обновления статистики:', error);
                this.renderStatsFromCache();
            });
    }

    async fetchStats() {
        try {
            const response = await fetch('/api/stats');
            if (!response.ok) throw new Error('Ошибка получения статистики');
            return await response.json();
        } catch (error) {
            // Fallback на статические данные
            return {
                active_games: parseInt(this.elements.activeGamesCount?.textContent || '0'),
                total_players: parseInt(this.elements.onlinePlayersCount?.textContent || '0'),
                complete_games: parseInt(this.elements.completedGamesCount?.textContent || '0')
            };
        }
    }

    renderStats(stats) {
        if (this.elements.activeGamesCount) {
            this.animateNumber(this.elements.activeGamesCount, stats.active_games);
        }
        if (this.elements.onlinePlayersCount) {
            this.animateNumber(this.elements.onlinePlayersCount, stats.total_players);
        }
        if (this.elements.completedGamesCount) {
            this.animateNumber(this.elements.completedGamesCount, stats.complete_games);
        }
    }

    renderStatsFromCache() {
        const cached = this.cache.get('stats');
        if (cached) {
            this.renderStats(cached.data);
        }
    }

    updateGamesList() {
        const cacheKey = 'games';
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            this.renderGamesList(cached.data);
            return;
        }

        this.fetchGamesList()
            .then(games => {
                this.cache.set(cacheKey, {
                    data: games,
                    timestamp: Date.now()
                });
                this.renderGamesList(games);
            })
            .catch(error => {
                console.error('Ошибка обновления списка игр:', error);
                this.renderGamesListFromCache();
            });
    }

    async fetchGamesList() {
        try {
            const response = await fetch('/api/games/active');
            if (!response.ok) throw new Error('Ошибка получения списка игр');
            return await response.json();
        } catch (error) {
            // Fallback на кэшированные данные
            const cached = this.cache.get('games');
            return cached ? cached.data : [];
        }
    }

    renderGamesList(games) {
        if (!this.elements.gamesPreview) return;

        const currentGames = Array.from(this.elements.gamesPreview.children)
            .filter(el => el.classList.contains('game-preview-card'))
            .map(el => el.dataset.gameId);

        const newGames = games.map(game => game.id);
        const gamesToRemove = currentGames.filter(id => !newGames.includes(id));
        const gamesToAdd = newGames.filter(id => !currentGames.includes(id));

        // Удаление старых игр
        gamesToRemove.forEach(gameId => {
            const element = this.elements.gamesPreview.querySelector(`[data-game-id="${gameId}"]`);
            if (element) {
                element.style.animation = 'fadeOut 0.3s ease-out';
                setTimeout(() => element.remove(), 300);
            }
        });

        // Добавление новых игр
        gamesToAdd.forEach(gameId => {
            const game = games.find(g => g.id === gameId);
            if (game) {
                const gameElement = this.createGameElement(game);
                this.elements.gamesPreview.appendChild(gameElement);
                gameElement.classList.add('new-item');
            }
        });

        // Обновление существующих игр
        games.forEach(game => {
            const element = this.elements.gamesPreview.querySelector(`[data-game-id="${gameId}"]`);
            if (element && this.hasGameChanged(game, this.findGameInCache(game.id))) {
                this.updateGameElement(element, game);
                element.classList.add('update-highlight');
                setTimeout(() => element.classList.remove('update-highlight'), 500);
            }
        });
    }

    renderGamesListFromCache() {
        const cached = this.cache.get('games');
        if (cached) {
            this.renderGamesList(cached.data);
        }
    }

    createGameElement(game) {
        const element = document.createElement('div');
        element.className = 'game-preview-card';
        element.dataset.gameId = game.id;
        
        const statusClass = game.status === 'waiting' ? 'status-waiting' : 'status-playing';
        const statusText = game.status === 'waiting' ? '⏳ Ожидание' : '▶️ В процессе';
        const joinText = game.status === 'waiting' && game.current_players < game.max_players ? '🎮 Присоединиться' : '👁️ Наблюдать';
        
        element.innerHTML = `
            <div class="game-preview-header">
                <h3>Игра #${game.id}</h3>
                <span class="game-status-badge ${statusClass}">${statusText}</span>
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
                    ${game.players.slice(0, 4).map(player => `<span class="player-tag">${player}</span>`).join('')}
                    ${game.players.length > 4 ? `<span class="player-tag more">+${game.players.length - 4}</span>` : ''}
                </div>
            </div>
            
            <div class="game-preview-actions">
                ${this.isAuthenticated ? 
                    `<a href="/game/${game.id}" class="action-btn action-btn-small">${joinText}</a>` :
                    `<a href="/login" class="action-btn action-btn-small">🔐 Войти чтобы играть</a>`
                }
            </div>
        `;
        
        return element;
    }

    updateGameElement(element, game) {
        // Обновление существующего элемента игры
        const statusElement = element.querySelector('.game-status-badge');
        const playersElement = element.querySelector('.info-value');
        const playersTags = element.querySelector('.info-players');
        
        if (statusElement) {
            const statusClass = game.status === 'waiting' ? 'status-waiting' : 'status-playing';
            const statusText = game.status === 'waiting' ? '⏳ Ожидание' : '▶️ В процессе';
            statusElement.className = `game-status-badge ${statusClass}`;
            statusElement.textContent = statusText;
        }
        
        if (playersElement) {
            playersElement.textContent = `${game.current_players}/${game.max_players}`;
        }
        
        if (playersTags) {
            playersTags.innerHTML = game.players.slice(0, 4).map(player => `<span class="player-tag">${player}</span>`).join('') +
                (game.players.length > 4 ? `<span class="player-tag more">+${game.players.length - 4}</span>` : '');
        }
    }

    checkConnectionStatus() {
        if (!window.gameSocket) {
            this.updateConnectionStatus('error');
            return;
        }

        if (this.isConnected) {
            this.updateConnectionStatus('connected');
        } else {
            this.updateConnectionStatus('disconnected');
        }
    }

    updateConnectionStatus(status, attempt = 0) {
        if (!this.elements.connectionStatus) return;

        this.elements.connectionStatus.className = 'connection-status';
        
        switch (status) {
            case 'connected':
                this.elements.connectionStatus.classList.add('connection-active');
                this.elements.statusIndicator.style.background = '#4ECDC4';
                this.elements.statusText.textContent = 'Подключено';
                break;
            case 'disconnected':
                this.elements.connectionStatus.classList.add('connection-error');
                this.elements.statusIndicator.style.background = '#ff6b6b';
                this.elements.statusText.textContent = 'Отключено';
                break;
            case 'reconnecting':
                this.elements.connectionStatus.classList.add('connection-reconnecting');
                this.elements.statusIndicator.style.background = '#ffa726';
                this.elements.statusText.textContent = `Переподключение ${attempt}/${this.maxReconnectAttempts}`;
                break;
            case 'error':
                this.elements.connectionStatus.classList.add('connection-error');
                this.elements.statusIndicator.style.background = '#ff6b6b';
                this.elements.statusText.textContent = 'Ошибка подключения';
                break;
        }
    }

    async checkServerStatus() {
        const startTime = Date.now();
        
        try {
            const response = await fetch('/api/health');
            const responseTime = Date.now() - startTime;
            
            if (response.ok) {
                this.updateServerStatus('online', responseTime);
            } else {
                this.updateServerStatus('error', responseTime);
            }
        } catch (error) {
            this.updateServerStatus('offline', Date.now() - startTime);
        }
    }

    updateServerStatus(status, responseTime = 0) {
        if (!this.elements.serverStatusIndicator || !this.elements.serverStatusText || !this.elements.serverResponseTime) return;

        switch (status) {
            case 'online':
                this.elements.serverStatusIndicator.style.background = '#4ECDC4';
                this.elements.serverStatusText.textContent = 'Онлайн';
                this.elements.serverResponseTime.textContent = `${responseTime}мс`;
                break;
            case 'error':
                this.elements.serverStatusIndicator.style.background = '#ffa726';
                this.elements.serverStatusText.textContent = 'Ошибка';
                this.elements.serverResponseTime.textContent = `${responseTime}мс`;
                break;
            case 'offline':
                this.elements.serverStatusIndicator.style.background = '#ff6b6b';
                this.elements.serverStatusText.textContent = 'Оффлайн';
                this.elements.serverResponseTime.textContent = '—';
                break;
        }
    }

    // Обработчики событий
    handleGameCreated(data) {
        console.log('Создана новая игра:', data);
        this.updateGamesList();
    }

    handleGameUpdated(data) {
        console.log('Обновлена игра:', data);
        this.updateGamesList();
    }

    handleGameDeleted(data) {
        console.log('Удалена игра:', data);
        this.updateGamesList();
    }

    handlePlayerOnline(data) {
        console.log('Игрок онлайн:', data);
        this.updateStats();
    }

    handlePlayerOffline(data) {
        console.log('Игрок оффлайн:', data);
        this.updateStats();
    }

    handleStatsUpdated(data) {
        console.log('Обновлена статистика:', data);
        this.renderStats(data);
    }

    handleGameCardClick(gameCard) {
        const gameId = gameCard.dataset.gameId;
        console.log('Клик по игре:', gameId);
        // Дополнительная логика при клике на игру
    }

    handleResize() {
        // Обработка изменения размера окна
        console.log('Размер окна изменен');
    }

    // Утилиты
    queueUpdate(callback) {
        this.updateQueue.push(callback);
        this.processUpdateQueue();
    }

    processUpdateQueue() {
        if (this.isUpdating || this.updateQueue.length === 0) return;
        
        this.isUpdating = true;
        const updates = this.updateQueue.splice(0, 5); // Обработать до 5 обновлений за раз
        
        updates.forEach(update => {
            try {
                update();
            } catch (error) {
                console.error('Ошибка обработки обновления:', error);
            }
        });
        
        this.isUpdating = false;
        
        if (this.updateQueue.length > 0) {
            setTimeout(() => this.processUpdateQueue(), 50);
        }
    }

    animateNumber(element, targetValue) {
        if (!element) return;
        
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = Math.round(startValue + (targetValue - startValue) * progress);
            element.textContent = currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    hasGameChanged(newGame, oldGame) {
        if (!oldGame) return true;
        return JSON.stringify(newGame) !== JSON.stringify(oldGame);
    }

    findGameInCache(gameId) {
        const cached = this.cache.get('games');
        if (cached && cached.data) {
            return cached.data.find(game => game.id === gameId);
        }
        return null;
    }

    // Очистка
    destroy() {
        if (this.statsInterval) clearInterval(this.statsInterval);
        if (this.gamesInterval) clearInterval(this.gamesInterval);
        if (this.serverCheckInterval) clearInterval(this.serverCheckInterval);
        
        this.cache.clear();
        this.updateQueue = [];
        
        console.log('IndexManager уничтожен');
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.indexManager = new IndexManager();
});

// Обработка выхода со страницы
window.addEventListener('beforeunload', () => {
    if (window.indexManager) {
        window.indexManager.destroy();
    }
});

// Добавление CSS анимаций
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-10px); }
    }
    
    .game-preview-card {
        animation: newItemSlideIn 0.3s ease-out;
    }
`;
document.head.appendChild(style);