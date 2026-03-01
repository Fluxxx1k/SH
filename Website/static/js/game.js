/**
 * Основной контроллер игры
 * Управляет игровым процессом и взаимодействием с сервером
 */

class GameManager {
    constructor() {
        this.gameId = null;
        this.username = null;
        this.players = new Map();
        this.gameState = 'waiting'; // waiting, playing, ended
        this.isHost = false;
        this.isInGame = false;
        
        // Настройки производительности
        this.updateInterval = 1000;
        this.lastUpdate = 0;
        this.updateThrottle = 100;
        
        // Кэш для оптимизации
        this.cache = new Map();
        this.cacheTimeout = 300000; // 5 минут
        
        this.init();
    }
    
    init() {
        this.loadGameConfig();
        this.setupEventListeners();
        this.setupSocketHandlers();
        this.startPeriodicUpdates();
        
        // Подключаемся к сокету
        if (window.gameSocket) {
            window.gameSocket.connect();
        }
    }
    
    loadGameConfig() {
        if (window.GAME_CONFIG) {
            this.gameId = window.GAME_CONFIG.gameId;
            this.username = window.GAME_CONFIG.username;
            this.isHost = window.GAME_CONFIG.createdBy === window.GAME_CONFIG.username;
            this.isInGame = window.GAME_CONFIG.inGame;
            this.gameState = window.GAME_CONFIG.isGameStarted ? 'playing' : 'waiting';
            
            // Загружаем игроков
            if (window.GAME_CONFIG.players) {
                window.GAME_CONFIG.players.forEach(player => {
                    this.players.set(player.name, {
                        ...player,
                        online: true,
                        lastSeen: Date.now()
                    });
                });
            }
        }
    }
    
    setupEventListeners() {
        // Кнопки голосования
        const voteButtons = document.querySelectorAll('.vote-btn');
        voteButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleVoteClick(btn.dataset.vote);
            });
        });
        
        // Кнопки цвета
        const colorButtons = document.querySelectorAll('.color-btn');
        colorButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleColorClick(btn.dataset.color);
            });
        });
        
        // Кнопки управления цветом
        const clearColorBtn = document.getElementById('clearColorBtn');
        const submitColorBtn = document.getElementById('submitColorBtn');
        
        if (clearColorBtn) {
            clearColorBtn.addEventListener('click', () => this.clearColorInput());
        }
        
        if (submitColorBtn) {
            submitColorBtn.addEventListener('click', () => this.submitColorVote());
        }
        
        // Кнопки игрового управления
        const startGameBtn = document.getElementById('startGameBtn');
        const deleteGameBtn = document.getElementById('deleteGameBtn');
        const joinGameBtn = document.getElementById('joinGameBtn');
        
        if (startGameBtn) {
            startGameBtn.addEventListener('click', () => this.startGame());
        }
        
        if (deleteGameBtn) {
            deleteGameBtn.addEventListener('click', () => this.deleteGame());
        }
        
        if (joinGameBtn) {
            joinGameBtn.addEventListener('click', () => this.joinGame());
        }
        
        // Кнопка обновления логов
        const refreshLogsBtn = document.getElementById('refreshLogsBtn');
        if (refreshLogsBtn) {
            refreshLogsBtn.addEventListener('click', () => this.refreshLogs());
        }
        
        // Обработка нажатия Enter в полях ввода
        const colorInput = document.getElementById('colorInput');
        if (colorInput) {
            colorInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.submitColorVote();
                }
            });
        }
        
        // Обработка выбора игрока
        const playerSelect = document.getElementById('playerSelect');
        const votePlayerBtn = document.getElementById('votePlayerBtn');
        
        if (playerSelect && votePlayerBtn) {
            votePlayerBtn.addEventListener('click', () => {
                const selectedPlayer = playerSelect.value;
                if (selectedPlayer) {
                    this.voteForPlayer(selectedPlayer);
                }
            });
        }
    }
    
    setupSocketHandlers() {
        if (!window.gameSocket) return;
        
        // Подписка на события сокета
        window.gameSocket.on('game_update', (data) => {
            this.handleGameUpdate(data);
        });
        
        window.gameSocket.on('player_joined', (data) => {
            this.handlePlayerJoined(data);
        });
        
        window.gameSocket.on('player_left', (data) => {
            this.handlePlayerLeft(data);
        });
        
        window.gameSocket.on('game_started', (data) => {
            this.handleGameStarted(data);
        });
        
        window.gameSocket.on('game_ended', (data) => {
            this.handleGameEnded(data);
        });
        
        window.gameSocket.on('vote_result', (data) => {
            this.handleVoteResult(data);
        });
    }
    
    // Обработчики событий
    handleVoteClick(voteType) {
        if (!this.canVote()) {
            this.showNotification('Вы не можете голосовать сейчас', 'warning');
            return;
        }
        
        // Визуальная обратная связь
        const button = document.querySelector(`[data-vote="${voteType}"]`);
        if (button) {
            button.classList.add('voted');
            setTimeout(() => button.classList.remove('voted'), 300);
        }
        
        // Отправляем голос на сервер
        this.submitVote(voteType);
    }
    
    handleColorClick(color) {
        const colorInput = document.getElementById('colorInput');
        if (colorInput) {
            colorInput.value = color;
            
            // Визуальная обратная связь
            document.querySelectorAll('.color-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            
            const button = document.querySelector(`[data-color="${color}"]`);
            if (button) {
                button.classList.add('selected');
                setTimeout(() => button.classList.remove('selected'), 300);
            }
        }
    }
    
    handleGameUpdate(data) {
        console.log('Обновление игры:', data);
        
        // Обновляем состояние игры
        if (data.game_state) {
            this.gameState = data.game_state;
        }
        
        // Обновляем игроков
        if (data.players) {
            this.updatePlayers(data.players);
        }
        
        // Обновляем UI
        this.updateGameUI();
        
        // Кэшируем обновление
        this.cache.set(`game_update_${Date.now()}`, {
            data: data,
            timestamp: Date.now()
        });
    }
    
    handlePlayerJoined(data) {
        console.log('Игрок присоединился:', data);
        
        this.players.set(data.player.name, {
            ...data.player,
            online: true,
            lastSeen: Date.now()
        });
        
        this.updatePlayersList();
        this.showNotification(`Игрок ${data.player.name} присоединился к игре`, 'info');
    }
    
    handlePlayerLeft(data) {
        console.log('Игрок покинул игру:', data);
        
        const player = this.players.get(data.player_name);
        if (player) {
            player.online = false;
            player.lastSeen = Date.now();
        }
        
        this.updatePlayersList();
        this.showNotification(`Игрок ${data.player_name} покинул игру`, 'info');
    }
    
    handleGameStarted(data) {
        console.log('Игра началась:', data);
        
        this.gameState = 'playing';
        this.updateGameUI();
        this.showNotification('Игра началась!', 'success');
        
        // Обновляем кнопки
        const startGameBtn = document.getElementById('startGameBtn');
        if (startGameBtn) {
            startGameBtn.style.display = 'none';
        }
    }
    
    handleGameEnded(data) {
        console.log('Игра завершена:', data);
        
        this.gameState = 'ended';
        this.updateGameUI();
        this.showNotification('Игра завершена!', 'info');
    }
    
    handleVoteResult(data) {
        console.log('Результат голосования:', data);
        
        // Обновляем UI голосования
        this.updateVoteResults(data);
        
        // Показываем уведомление
        if (data.result) {
            this.showNotification(`Результат голосования: ${data.result}`, 'info');
        }
    }
    
    // Методы взаимодействия с сервером
    submitVote(voteType) {
        if (!window.gameSocket || !window.gameSocket.isConnected()) {
            this.showNotification('Нет подключения к серверу', 'error');
            return;
        }
        
        window.gameSocket.emit('vote', {
            game_id: this.gameId,
            vote_type: voteType,
            timestamp: Date.now()
        });
        
        // Локальное обновление UI для немедленной обратной связи
        this.updateLocalVote(voteType);
    }
    
    voteForPlayer(playerName) {
        if (!this.canVote()) {
            this.showNotification('Вы не можете голосовать сейчас', 'warning');
            return;
        }
        
        if (!window.gameSocket || !window.gameSocket.isConnected()) {
            this.showNotification('Нет подключения к серверу', 'error');
            return;
        }
        
        window.gameSocket.emit('vote_player', {
            game_id: this.gameId,
            target_player: playerName,
            timestamp: Date.now()
        });
        
        this.showNotification(`Голос против ${playerName} отправлен`, 'info');
    }
    
    submitColorVote() {
        const colorInput = document.getElementById('colorInput');
        if (!colorInput || !colorInput.value.trim()) {
            this.showNotification('Введите цвет', 'warning');
            return;
        }
        
        if (!window.gameSocket || !window.gameSocket.isConnected()) {
            this.showNotification('Нет подключения к серверу', 'error');
            return;
        }
        
        window.gameSocket.emit('color_vote', {
            game_id: this.gameId,
            color: colorInput.value.trim().toUpperCase(),
            timestamp: Date.now()
        });
        
        // Очищаем поле ввода
        colorInput.value = '';
        this.showNotification('Цвет отправлен', 'success');
    }
    
    clearColorInput() {
        const colorInput = document.getElementById('colorInput');
        if (colorInput) {
            colorInput.value = '';
        }
        
        // Снимаем выделение с кнопок цвета
        document.querySelectorAll('.color-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
    }
    
    startGame() {
        if (!this.isHost) {
            this.showNotification('Только хост может начать игру', 'warning');
            return;
        }
        
        if (this.players.size < 2) {
            this.showNotification('Недостаточно игроков для начала игры', 'warning');
            return;
        }
        
        if (!window.gameSocket || !window.gameSocket.isConnected()) {
            this.showNotification('Нет подключения к серверу', 'error');
            return;
        }
        
        if (confirm('Начать игру?')) {
            window.gameSocket.emit('start_game', {
                game_id: this.gameId,
                timestamp: Date.now()
            });
        }
    }
    
    joinGame() {
        if (this.isInGame) {
            this.showNotification('Вы уже в игре', 'warning');
            return;
        }
        
        if (!window.gameSocket || !window.gameSocket.isConnected()) {
            this.showNotification('Нет подключения к серверу', 'error');
            return;
        }
        
        window.gameSocket.emit('join_game_request', {
            game_id: this.gameId,
            timestamp: Date.now()
        });
    }
    
    deleteGame() {
        if (!this.isHost) {
            this.showNotification('Только хост может удалить игру', 'warning');
            return;
        }
        
        if (confirm('Удалить игру? Это действие нельзя отменить.')) {
            if (!window.gameSocket || !window.gameSocket.isConnected()) {
                this.showNotification('Нет подключения к серверу', 'error');
                return;
            }
            
            window.gameSocket.emit('delete_game', {
                game_id: this.gameId,
                timestamp: Date.now()
            });
        }
    }
    
    refreshLogs() {
        if (!window.gameSocket || !window.gameSocket.isConnected()) {
            this.showNotification('Нет подключения к серверу', 'error');
            return;
        }
        
        window.gameSocket.emit('request_logs', {
            game_id: this.gameId,
            timestamp: Date.now()
        });
        
        // Показываем индикатор загрузки
        const loadingElement = document.getElementById('logLoading');
        if (loadingElement) {
            loadingElement.style.display = 'flex';
        }
    }
    
    // Утилиты
    canVote() {
        return this.gameState === 'playing' && this.isInGame;
    }
    
    updatePlayers(playersData) {
        this.players.clear();
        
        playersData.forEach(player => {
            this.players.set(player.name, {
                ...player,
                online: true,
                lastSeen: Date.now()
            });
        });
        
        this.updatePlayersList();
    }
    
    updatePlayersList() {
        const playersList = document.getElementById('playersList');
        const playerCount = document.getElementById('playerCount');
        
        if (playersList) {
            playersList.innerHTML = '';
            
            this.players.forEach((player, name) => {
                const playerElement = document.createElement('div');
                playerElement.className = `player-item ${player.online ? 'online' : 'offline'}`;
                playerElement.dataset.playerName = name;
                
                playerElement.innerHTML = `
                    <span class="player-name">${name}</span>
                    <span class="player-role">${player.role || 'Неизвестно'}</span>
                    <span class="player-status ${player.online ? 'online' : 'offline'}"></span>
                `;
                
                playersList.appendChild(playerElement);
            });
        }
        
        if (playerCount) {
            playerCount.textContent = this.players.size;
        }
        
        // Обновляем выпадающий список игроков для голосования
        const playerSelect = document.getElementById('playerSelect');
        if (playerSelect) {
            playerSelect.innerHTML = '<option value="">Выберите игрока</option>';
            
            this.players.forEach((player, name) => {
                if (name !== this.username) {
                    const option = document.createElement('option');
                    option.value = name;
                    option.textContent = name;
                    playerSelect.appendChild(option);
                }
            });
        }
    }
    
    updateGameUI() {
        // Обновляем видимость элементов в зависимости от состояния игры
        const votingSection = document.querySelector('.voting-section');
        const gameControls = document.querySelector('.game-controls');
        
        if (votingSection) {
            if (this.gameState === 'playing') {
                votingSection.style.display = 'block';
            } else {
                votingSection.style.display = this.isHost ? 'block' : 'none';
            }
        }
        
        // Обновляем кнопки управления
        this.updateControlButtons();
    }
    
    updateControlButtons() {
        const startGameBtn = document.getElementById('startGameBtn');
        const joinGameBtn = document.getElementById('joinGameBtn');
        
        if (startGameBtn) {
            startGameBtn.style.display = 
                (this.isHost && this.gameState === 'waiting' && this.players.size >= 2) ? 'block' : 'none';
        }
        
        if (joinGameBtn) {
            joinGameBtn.style.display = 
                (!this.isInGame && this.gameState === 'waiting') ? 'block' : 'none';
        }
    }
    
    updateLocalVote(voteType) {
        // Локальное обновление UI для немедленной обратной связи
        // Это временное обновление, реальные данные придут с сервера
        console.log(`Локальный голос: ${voteType}`);
    }
    
    updateVoteResults(data) {
        // Обновляем UI с результатами голосования
        const voteResults = document.getElementById('voteResults');
        if (voteResults) {
            voteResults.innerHTML = '';
            
            if (data.votes) {
                Object.entries(data.votes).forEach(([voteType, count]) => {
                    const resultItem = document.createElement('div');
                    resultItem.className = 'vote-result-item';
                    resultItem.innerHTML = `
                        <span>${this.getVoteTypeText(voteType)}</span>
                        <span>${count}</span>
                    `;
                    voteResults.appendChild(resultItem);
                });
            }
        }
        
        // Обновляем счетчик голосов
        const voteCount = document.getElementById('voteCount');
        if (voteCount && data.total_votes !== undefined) {
            voteCount.textContent = data.total_votes;
        }
    }
    
    getVoteTypeText(voteType) {
        const voteTypes = {
            'yes': 'ЗА',
            'no': 'ПРОТИВ',
            'pass': 'ПАС'
        };
        return voteTypes[voteType] || voteType;
    }
    
    showNotification(message, type = 'info') {
        // Создаем уведомление
        const notification = document.createElement('div');
        notification.className = `flash flash-${type}`;
        notification.textContent = message;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '1000';
        notification.style.animation = 'slideIn 0.3s ease-out';
        
        document.body.appendChild(notification);
        
        // Удаляем через 5 секунд
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }
    
    startPeriodicUpdates() {
        // Периодическое обновление данных (с throttling)
        setInterval(() => {
            const now = Date.now();
            if (now - this.lastUpdate >= this.updateThrottle) {
                this.performPeriodicUpdate();
                this.lastUpdate = now;
            }
        }, this.updateInterval);
    }
    
    performPeriodicUpdate() {
        // Обновляем статус онлайн игроков
        this.players.forEach((player, name) => {
            if (Date.now() - player.lastSeen > 300000) { // 5 минут
                player.online = false;
            }
        });
        
        this.updatePlayersList();
        
        // Очищаем старый кэш
        const now = Date.now();
        for (const [key, value] of this.cache.entries()) {
            if (now - value.timestamp > this.cacheTimeout) {
                this.cache.delete(key);
            }
        }
    }
    
    // Утилиты
    getCacheKey(type, data) {
        return `${type}:${JSON.stringify(data)}`;
    }
    
    setCache(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }
    
    getCache(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }
        return null;
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.gameManager = new GameManager();
});

// Дополнительные стили для уведомлений
const notificationStyles = `
@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOut {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}
`;

// Добавляем стили в DOM
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);