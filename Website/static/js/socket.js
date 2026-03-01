/**
 * Socket.IO клиент для real-time обновлений
 * Управляет подключением и обработкой событий
 */

class GameSocket {
    constructor() {
        this.socket = null;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        this.eventHandlers = new Map();
        this.messageQueue = [];
        this.isProcessingQueue = false;
        
        // Настройки производительности
        this.batchSize = 10;
        this.batchTimeout = 50;
        this.batchTimer = null;
        this.pendingEvents = [];
        
        // Кэш для избежания дублирования
        this.eventCache = new Map();
        this.cacheTimeout = 5000;
        
        this.init();
    }
    
    init() {
        this.setupSocket();
        this.setupEventListeners();
        this.setupVisibilityHandling();
        this.startBatchProcessor();
    }
    
    setupSocket() {
        try {
            this.socket = io({
                transports: ['websocket', 'polling'],
                timeout: 20000,
                forceNew: true,
                reconnection: true,
                reconnectionDelay: this.reconnectDelay,
                reconnectionAttempts: this.maxReconnectAttempts,
                randomizationFactor: 0.5,
                autoConnect: false // Подключаемся вручную для лучшего контроля
            });
            
            this.setupSocketEvents();
        } catch (error) {
            console.error('Ошибка при создании Socket.IO:', error);
            this.scheduleReconnect();
        }
    }
    
    setupSocketEvents() {
        if (!this.socket) return;
        
        this.socket.on('connect', () => {
            console.log('Socket.IO подключен');
            this.connected = true;
            this.reconnectAttempts = 0;
            this.updateConnectionStatus('connected');
            this.processMessageQueue();
            this.joinGameRoom();
        });
        
        this.socket.on('disconnect', (reason) => {
            console.log('Socket.IO отключен:', reason);
            this.connected = false;
            this.updateConnectionStatus('disconnected');
            
            if (reason === 'io server disconnect') {
                // Сервер инициировал отключение, пробуем переподключиться
                this.scheduleReconnect();
            }
        });
        
        this.socket.on('connect_error', (error) => {
            console.error('Ошибка подключения Socket.IO:', error);
            this.connected = false;
            this.updateConnectionStatus('error');
            this.scheduleReconnect();
        });
        
        this.socket.on('reconnect', (attemptNumber) => {
            console.log('Переподключение успешно, попытка:', attemptNumber);
            this.connected = true;
            this.updateConnectionStatus('connected');
        });
        
        this.socket.on('reconnect_failed', () => {
            console.error('Не удалось переподключиться после всех попыток');
            this.updateConnectionStatus('failed');
        });
        
        // Обработка событий игры
        this.socket.on('game_update', (data) => {
            this.handleGameUpdate(data);
        });
        
        this.socket.on('player_joined', (data) => {
            this.handlePlayerJoined(data);
        });
        
        this.socket.on('player_left', (data) => {
            this.handlePlayerLeft(data);
        });
        
        this.socket.on('chat_message', (data) => {
            this.handleChatMessage(data);
        });
        
        this.socket.on('vote_update', (data) => {
            this.handleVoteUpdate(data);
        });
        
        this.socket.on('log_update', (data) => {
            this.handleLogUpdate(data);
        });
        
        this.socket.on('game_started', (data) => {
            this.handleGameStarted(data);
        });
        
        this.socket.on('game_ended', (data) => {
            this.handleGameEnded(data);
        });
    }
    
    setupEventListeners() {
        // Глобальные обработчики событий
        window.addEventListener('beforeunload', () => {
            this.disconnect();
        });
        
        // Обработка ошибок
        window.addEventListener('error', (event) => {
            console.error('Глобальная ошибка:', event.error);
            if (this.connected) {
                this.emit('client_error', {
                    message: event.error.message,
                    stack: event.error.stack,
                    url: window.location.href,
                    timestamp: Date.now()
                });
            }
        });
        
        // Обработка неперехваченных промисов
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Необработанное отклонение промиса:', event.reason);
            if (this.connected) {
                this.emit('client_error', {
                    message: event.reason?.message || 'Unhandled promise rejection',
                    stack: event.reason?.stack,
                    url: window.location.href,
                    timestamp: Date.now()
                });
            }
        });
    }
    
    setupVisibilityHandling() {
        // Приостановка обновлений при скрытии вкладки
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseUpdates();
            } else {
                this.resumeUpdates();
            }
        });
        
        // Обработка перехода в офлайн
        window.addEventListener('online', () => {
            console.log('Соединение восстановлено');
            this.connect();
        });
        
        window.addEventListener('offline', () => {
            console.log('Соединение потеряно');
            this.updateConnectionStatus('offline');
        });
    }
    
    startBatchProcessor() {
        // Пакетная обработка событий для оптимизации
        this.batchTimer = setInterval(() => {
            if (this.pendingEvents.length > 0) {
                this.processEventBatch();
            }
        }, this.batchTimeout);
    }
    
    processEventBatch() {
        if (this.pendingEvents.length === 0) return;
        
        const batch = this.pendingEvents.splice(0, this.batchSize);
        
        // Группируем события по типу
        const groupedEvents = batch.reduce((groups, event) => {
            const type = event.type;
            if (!groups[type]) groups[type] = [];
            groups[type].push(event.data);
            return groups;
        }, {});
        
        // Обрабатываем сгруппированные события
        Object.entries(groupedEvents).forEach(([type, data]) => {
            this.processGroupedEvent(type, data);
        });
    }
    
    processGroupedEvent(type, dataArray) {
        // Оптимизированная обработка групп событий
        switch (type) {
            case 'chat_message':
                this.processChatMessages(dataArray);
                break;
            case 'log_update':
                this.processLogUpdates(dataArray);
                break;
            case 'vote_update':
                this.processVoteUpdates(dataArray);
                break;
            default:
                dataArray.forEach(data => this.dispatchEvent(type, data));
        }
    }
    
    // Публичные методы
    connect() {
        if (this.socket && !this.connected) {
            try {
                this.socket.connect();
            } catch (error) {
                console.error('Ошибка при подключении:', error);
                this.scheduleReconnect();
            }
        }
    }
    
    disconnect() {
        if (this.socket && this.connected) {
            this.socket.disconnect();
        }
        
        if (this.batchTimer) {
            clearInterval(this.batchTimer);
            this.batchTimer = null;
        }
    }
    
    emit(event, data) {
        if (this.connected && this.socket) {
            try {
                // Проверяем кэш для избежания дублирования
                const cacheKey = `${event}:${JSON.stringify(data)}`;
                const now = Date.now();
                
                if (this.eventCache.has(cacheKey)) {
                    const cached = this.eventCache.get(cacheKey);
                    if (now - cached.timestamp < this.cacheTimeout) {
                        return; // Игнорируем дублирующее событие
                    }
                }
                
                this.eventCache.set(cacheKey, { timestamp: now });
                
                // Очищаем старый кэш
                if (this.eventCache.size > 1000) {
                    const oldest = Array.from(this.eventCache.entries())
                        .sort((a, b) => a[1].timestamp - b[1].timestamp)
                        .slice(0, 100);
                    
                    oldest.forEach(([key]) => this.eventCache.delete(key));
                }
                
                this.socket.emit(event, data);
            } catch (error) {
                console.error('Ошибка при отправке события:', error);
                this.queueMessage(event, data);
            }
        } else {
            this.queueMessage(event, data);
        }
    }
    
    on(event, handler) {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, []);
        }
        this.eventHandlers.get(event).push(handler);
    }
    
    off(event, handler) {
        if (this.eventHandlers.has(event)) {
            const handlers = this.eventHandlers.get(event);
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
        }
    }
    
    // Приватные методы
    queueMessage(event, data) {
        this.messageQueue.push({ event, data, timestamp: Date.now() });
        
        // Ограничиваем размер очереди
        if (this.messageQueue.length > 1000) {
            this.messageQueue = this.messageQueue.slice(-500);
        }
    }
    
    processMessageQueue() {
        if (this.messageQueue.length === 0 || !this.connected) return;
        
        const messages = this.messageQueue.splice(0);
        messages.forEach(({ event, data }) => {
            this.emit(event, data);
        });
    }
    
    dispatchEvent(event, data) {
        if (this.eventHandlers.has(event)) {
            this.eventHandlers.get(event).forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error('Ошибка в обработчике события:', error);
                }
            });
        }
    }
    
    joinGameRoom(gameId = null) {
        const currentGameId = gameId || window.GAME_CONFIG?.gameId;
        if (currentGameId && this.connected) {
            this.emit('join_game', { game_id: currentGameId });
        }
    }
    
    leaveGameRoom(gameId = null) {
        const currentGameId = gameId || window.GAME_CONFIG?.gameId;
        if (currentGameId && this.connected) {
            this.emit('leave_game', { game_id: currentGameId });
        }
    }
    
    updateConnectionStatus(status) {
        const statusElement = document.getElementById('connectionStatus');
        const indicator = document.getElementById('statusIndicator');
        const text = document.getElementById('statusText');
        
        if (statusElement && indicator && text) {
            indicator.className = `status-indicator ${status}`;
            
            const statusMessages = {
                'connected': 'Подключено',
                'disconnected': 'Отключено',
                'connecting': 'Подключение...',
                'error': 'Ошибка подключения',
                'failed': 'Не удалось подключиться',
                'offline': 'Офлайн'
            };
            
            text.textContent = statusMessages[status] || 'Неизвестный статус';
        }
    }
    
    scheduleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempts), 30000);
            
            setTimeout(() => {
                if (!this.connected) {
                    this.connect();
                }
            }, delay);
        }
    }
    
    pauseUpdates() {
        if (this.socket) {
            this.socket.disconnect();
        }
    }
    
    resumeUpdates() {
        if (!this.connected) {
            this.connect();
        }
    }
    
    // Обработчики событий игры
    handleGameUpdate(data) {
        this.pendingEvents.push({ type: 'game_update', data });
    }
    
    handlePlayerJoined(data) {
        this.pendingEvents.push({ type: 'player_joined', data });
    }
    
    handlePlayerLeft(data) {
        this.pendingEvents.push({ type: 'player_left', data });
    }
    
    handleChatMessage(data) {
        this.pendingEvents.push({ type: 'chat_message', data });
    }
    
    handleVoteUpdate(data) {
        this.pendingEvents.push({ type: 'vote_update', data });
    }
    
    handleLogUpdate(data) {
        this.pendingEvents.push({ type: 'log_update', data });
    }
    
    handleGameStarted(data) {
        this.pendingEvents.push({ type: 'game_started', data });
    }
    
    handleGameEnded(data) {
        this.pendingEvents.push({ type: 'game_ended', data });
    }
    
    // Оптимизированные обработчики групп событий
    processChatMessages(messages) {
        // Пакетная обработка сообщений чата
        if (window.ChatManager) {
            window.ChatManager.batchAddMessages(messages);
        }
    }
    
    processLogUpdates(updates) {
        // Пакетная обработка обновлений логов
        if (window.LogManager) {
            window.LogManager.batchAddEntries(updates);
        }
    }
    
    processVoteUpdates(updates) {
        // Пакетная обработка обновлений голосования
        if (window.VoteManager) {
            const latestUpdate = updates[updates.length - 1]; // Берем последнее обновление
            window.VoteManager.updateVoteStatus(latestUpdate);
        }
    }
    
    // Утилиты
    isConnected() {
        return this.connected;
    }
    
    getConnectionState() {
        return {
            connected: this.connected,
            socketId: this.socket?.id || null,
            reconnectAttempts: this.reconnectAttempts
        };
    }
}

// Инициализация глобального сокет-менеджера
window.gameSocket = new GameSocket();