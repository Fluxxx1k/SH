/**
 * Менеджер чата с real-time обновлениями
 * Поддерживает отправку сообщений, историю и уведомления
 */

class ChatManager {
    constructor() {
        this.messages = [];
        this.maxMessages = 100;
        this.unreadCount = 0;
        this.isScrolledToBottom = true;
        this.lastMessageTime = 0;
        this.messageThrottle = 500; // Минимальный интервал между сообщениями
        
        // Настройки производительности
        this.batchSize = 10;
        this.renderBatchSize = 5;
        this.renderDelay = 16; // ~60fps
        
        // Кэш для оптимизации
        this.messageCache = new Map();
        this.cacheTimeout = 300000; // 5 минут
        
        // Элементы DOM
        this.chatMessages = null;
        this.chatInput = null;
        this.sendButton = null;
        
        this.init();
    }
    
    init() {
        this.setupDOMElements();
        this.setupEventListeners();
        this.setupSocketHandlers();
        this.loadChatHistory();
        this.startPeriodicCleanup();
        
        // Делаем глобальным для доступа из других модулей
        window.ChatManager = this;
    }
    
    setupDOMElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendButton = document.getElementById('sendChatBtn');
        
        if (!this.chatMessages || !this.chatInput || !this.sendButton) {
            console.warn('Элементы чата не найдены');
            return;
        }
        
        // Настройка автоматической прокрутки
        this.setupAutoScroll();
    }
    
    setupEventListeners() {
        if (!this.chatInput || !this.sendButton) return;
        
        // Отправка сообщения
        this.sendButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Отправка по Enter
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Автоматическая высота textarea
        this.chatInput.addEventListener('input', () => {
            this.adjustTextareaHeight();
        });
        
        // Предотвращение слишком частой отправки
        this.chatInput.addEventListener('input', this.throttle(() => {
            this.updateSendButtonState();
        }, 100));
        
        // Обработка вставки текста
        this.chatInput.addEventListener('paste', (e) => {
            this.handlePaste(e);
        });
        
        // Обработка потери фокуса
        this.chatInput.addEventListener('blur', () => {
            this.resetUnreadCount();
        });
    }
    
    setupSocketHandlers() {
        if (!window.gameSocket) return;
        
        window.gameSocket.on('chat_message', (data) => {
            this.handleIncomingMessage(data);
        });
        
        window.gameSocket.on('chat_history', (data) => {
            this.handleChatHistory(data);
        });
        
        window.gameSocket.on('chat_clear', () => {
            this.clearChat();
        });
        
        window.gameSocket.on('user_typing', (data) => {
            this.handleUserTyping(data);
        });
    }
    
    setupAutoScroll() {
        if (!this.chatMessages) return;
        
        // Отслеживаем прокрутку
        this.chatMessages.addEventListener('scroll', () => {
            const { scrollTop, scrollHeight, clientHeight } = this.chatMessages;
            this.isScrolledToBottom = scrollHeight - scrollTop - clientHeight < 10;
        });
        
        // MutationObserver для автоматической прокрутки
        const observer = new MutationObserver(() => {
            if (this.isScrolledToBottom) {
                this.scrollToBottom();
            }
        });
        
        observer.observe(this.chatMessages, {
            childList: true,
            subtree: true
        });
    }
    
    sendMessage() {
        if (!this.chatInput || !window.gameSocket) return;
        
        const message = this.chatInput.value.trim();
        
        // Валидация сообщения
        if (!this.validateMessage(message)) {
            return;
        }
        
        // Проверка троттлинга
        const now = Date.now();
        if (now - this.lastMessageTime < this.messageThrottle) {
            this.showNotification('Подождите немного перед отправкой следующего сообщения', 'warning');
            return;
        }
        
        // Создаем сообщение
        const messageData = {
            content: message,
            timestamp: now,
            game_id: window.GAME_CONFIG?.gameId,
            username: window.GAME_CONFIG?.username
        };
        
        // Локальное добавление для немедленной обратной связи
        this.addMessage({
            ...messageData,
            type: 'own',
            status: 'sending'
        });
        
        // Отправляем на сервер
        window.gameSocket.emit('chat_message', messageData);
        
        // Обновляем состояние
        this.lastMessageTime = now;
        this.chatInput.value = '';
        this.adjustTextareaHeight();
        this.updateSendButtonState();
        
        // Сбрасываем счетчик непрочитанных
        this.resetUnreadCount();
    }
    
    validateMessage(message) {
        if (!message) {
            return false;
        }
        
        if (message.length > 200) {
            this.showNotification('Сообщение слишком длинное (максимум 200 символов)', 'warning');
            return false;
        }
        
        // Проверка на спам
        if (this.isSpam(message)) {
            this.showNotification('Пожалуйста, не спамьте', 'warning');
            return false;
        }
        
        return true;
    }
    
    isSpam(message) {
        // Простая проверка на спам
        const recentMessages = this.messages.slice(-5);
        const duplicateCount = recentMessages.filter(msg => 
            msg.content === message && Date.now() - msg.timestamp < 10000
        ).length;
        
        return duplicateCount >= 3;
    }
    
    handleIncomingMessage(data) {
        // Проверяем кэш для избежания дублирования
        const cacheKey = `msg_${data.id || data.timestamp}_${data.username}`;
        if (this.messageCache.has(cacheKey)) {
            return;
        }
        
        // Определяем тип сообщения
        const messageType = this.determineMessageType(data);
        
        // Создаем полное сообщение
        const message = {
            ...data,
            type: messageType,
            status: 'received',
            id: data.id || this.generateMessageId()
        };
        
        // Добавляем в кэш
        this.messageCache.set(cacheKey, {
            message: message,
            timestamp: Date.now()
        });
        
        // Добавляем сообщение
        this.addMessage(message);
        
        // Показываем уведомление если вкладка не активна
        if (document.hidden) {
            this.incrementUnreadCount();
            this.showNotification(`${data.username}: ${data.content}`, 'info');
        }
    }
    
    handleChatHistory(data) {
        if (data.messages && Array.isArray(data.messages)) {
            // Очищаем текущие сообщения
            this.clearMessages();
            
            // Добавляем историю пакетами для производительности
            this.batchAddMessages(data.messages);
        }
    }
    
    batchAddMessages(messages) {
        if (!messages || messages.length === 0) return;
        
        // Сортируем по времени
        const sortedMessages = messages.sort((a, b) => a.timestamp - b.timestamp);
        
        // Обрабатываем пакетами
        const processBatch = (startIndex) => {
            const endIndex = Math.min(startIndex + this.renderBatchSize, sortedMessages.length);
            
            for (let i = startIndex; i < endIndex; i++) {
                const message = sortedMessages[i];
                this.addMessage(message, false); // Не прокручиваем для каждого сообщения
            }
            
            if (endIndex < sortedMessages.length) {
                setTimeout(() => processBatch(endIndex), this.renderDelay);
            } else {
                // Прокручиваем к последнему сообщению после обработки всех пакетов
                this.scrollToBottom();
            }
        };
        
        processBatch(0);
    }
    
    addMessage(message, scrollToBottom = true) {
        this.messages.push(message);
        
        // Ограничиваем количество сообщений
        if (this.messages.length > this.maxMessages) {
            this.messages = this.messages.slice(-this.maxMessages);
        }
        
        // Отображаем сообщение
        this.renderMessage(message);
        
        // Прокручиваем если нужно
        if (scrollToBottom && this.isScrolledToBottom) {
            setTimeout(() => this.scrollToBottom(), 10);
        }
        
        // Обновляем счетчик непрочитанных
        if (!document.hidden && message.type !== 'own') {
            this.incrementUnreadCount();
        }
    }
    
    renderMessage(message) {
        if (!this.chatMessages) return;
        
        const messageElement = this.createMessageElement(message);
        if (messageElement) {
            this.chatMessages.appendChild(messageElement);
        }
    }
    
    createMessageElement(message) {
        const div = document.createElement('div');
        div.className = `chat-message ${message.type || 'regular'}`;
        div.dataset.messageId = message.id;
        
        // Форматируем время
        const time = this.formatTime(message.timestamp);
        
        // Определяем аватары и цвета
        const avatar = this.getAvatar(message.username);
        const usernameColor = this.getUsernameColor(message.username);
        
        div.innerHTML = `
            <div class="chat-message-header">
                <span class="chat-message-author" style="color: ${usernameColor}">
                    ${avatar} ${message.username}
                </span>
                <span class="chat-message-time">${time}</span>
            </div>
            <div class="chat-message-content">${this.escapeHtml(message.content)}</div>
        `;
        
        // Добавляем индикатор статуса для собственных сообщений
        if (message.type === 'own') {
            const statusIndicator = document.createElement('div');
            statusIndicator.className = 'message-status';
            statusIndicator.textContent = this.getStatusText(message.status);
            div.appendChild(statusIndicator);
        }
        
        return div;
    }
    
    formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        // Если сообщение отправлено сегодня
        if (date.toDateString() === now.toDateString()) {
            return date.toLocaleTimeString('ru-RU', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
        }
        
        // Если сообщение отправлено вчера
        const yesterday = new Date(now);
        yesterday.setDate(yesterday.getDate() - 1);
        if (date.toDateString() === yesterday.toDateString()) {
            return `Вчера ${date.toLocaleTimeString('ru-RU', { 
                hour: '2-digit', 
                minute: '2-digit' 
            })}`;
        }
        
        // Для более старых сообщений
        return date.toLocaleDateString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    getAvatar(username) {
        // Простая генерация аватара по имени пользователя
        const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'];
        const colorIndex = username.charCodeAt(0) % colors.length;
        const color = colors[colorIndex];
        const initial = username.charAt(0).toUpperCase();
        
        return `<span class="avatar" style="background-color: ${color}">${initial}</span>`;
    }
    
    getUsernameColor(username) {
        // Генерация цвета по имени пользователя для консистентности
        const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];
        let hash = 0;
        for (let i = 0; i < username.length; i++) {
            hash = username.charCodeAt(i) + ((hash << 5) - hash);
        }
        return colors[Math.abs(hash) % colors.length];
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    getStatusText(status) {
        const statusTexts = {
            'sending': 'Отправка...',
            'sent': 'Отправлено',
            'delivered': 'Доставлено',
            'failed': 'Ошибка отправки'
        };
        return statusTexts[status] || '';
    }
    
    determineMessageType(data) {
        if (data.username === window.GAME_CONFIG?.username) {
            return 'own';
        }
        
        if (data.type === 'system') {
            return 'system';
        }
        
        return 'regular';
    }
    
    generateMessageId() {
        return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    adjustTextareaHeight() {
        if (!this.chatInput) return;
        
        this.chatInput.style.height = 'auto';
        const newHeight = Math.min(this.chatInput.scrollHeight, 120); // Максимум 5 строк
        this.chatInput.style.height = newHeight + 'px';
    }
    
    updateSendButtonState() {
        if (!this.sendButton || !this.chatInput) return;
        
        const hasText = this.chatInput.value.trim().length > 0;
        const canSend = hasText && (Date.now() - this.lastMessageTime >= this.messageThrottle);
        
        this.sendButton.disabled = !canSend;
        this.sendButton.textContent = canSend ? 'Отправить' : 'Подождите...';
    }
    
    handlePaste(e) {
        e.preventDefault();
        
        const text = (e.clipboardData || window.clipboardData).getData('text');
        const sanitizedText = this.sanitizePastedText(text);
        
        // Вставляем текст в текущую позицию курсора
        const start = this.chatInput.selectionStart;
        const end = this.chatInput.selectionEnd;
        const currentText = this.chatInput.value;
        
        this.chatInput.value = currentText.substring(0, start) + sanitizedText + currentText.substring(end);
        this.chatInput.selectionStart = this.chatInput.selectionEnd = start + sanitizedText.length;
        
        this.adjustTextareaHeight();
        this.updateSendButtonState();
    }
    
    sanitizePastedText(text) {
        // Удаляем лишние пробелы и переносы строк
        return text
            .replace(/\r\n/g, '\n')
            .replace(/\r/g, '\n')
            .replace(/\n{3,}/g, '\n\n')
            .trim()
            .substring(0, 200); // Ограничиваем длину
    }
    
    scrollToBottom() {
        if (!this.chatMessages) return;
        
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    incrementUnreadCount() {
        this.unreadCount++;
        this.updateUnreadIndicator();
    }
    
    resetUnreadCount() {
        this.unreadCount = 0;
        this.updateUnreadIndicator();
    }
    
    updateUnreadIndicator() {
        // Можно добавить индикатор непрочитанных сообщений в заголовок страницы
        if (this.unreadCount > 0) {
            document.title = `(${this.unreadCount}) Чат - Игра`;
        } else {
            document.title = 'Чат - Игра';
        }
    }
    
    clearChat() {
        this.messages = [];
        if (this.chatMessages) {
            this.chatMessages.innerHTML = '';
        }
        this.resetUnreadCount();
    }
    
    clearMessages() {
        this.messages = [];
        if (this.chatMessages) {
            this.chatMessages.innerHTML = '';
        }
    }
    
    handleUserTyping(data) {
        // Можно реализовать индикатор "печатает..."
        console.log(`${data.username} печатает...`);
    }
    
    loadChatHistory() {
        // Запрашиваем историю чата при подключении
        if (window.gameSocket && window.gameSocket.isConnected()) {
            window.gameSocket.emit('request_chat_history', {
                game_id: window.GAME_CONFIG?.gameId,
                limit: 50
            });
        }
    }
    
    startPeriodicCleanup() {
        // Периодическая очистка кэша и старых сообщений
        setInterval(() => {
            this.cleanupCache();
            this.cleanupOldMessages();
        }, 60000); // Каждую минуту
    }
    
    cleanupCache() {
        const now = Date.now();
        for (const [key, value] of this.messageCache.entries()) {
            if (now - value.timestamp > this.cacheTimeout) {
                this.messageCache.delete(key);
            }
        }
    }
    
    cleanupOldMessages() {
        if (this.messages.length > this.maxMessages) {
            this.messages = this.messages.slice(-this.maxMessages);
            
            // Обновляем отображение
            if (this.chatMessages) {
                const messages = this.chatMessages.querySelectorAll('.chat-message');
                const excessCount = messages.length - this.maxMessages;
                
                for (let i = 0; i < excessCount; i++) {
                    if (messages[i] && messages[i].parentNode) {
                        messages[i].parentNode.removeChild(messages[i]);
                    }
                }
            }
        }
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
    
    showNotification(message, type = 'info') {
        // Простое уведомление (можно заменить на более сложную систему)
        console.log(`[${type.toUpperCase()}] ${message}`);
        
        // Можно добавить визуальные уведомления
        if (window.gameManager && window.gameManager.showNotification) {
            window.gameManager.showNotification(message, type);
        }
    }
    
    // Публичные методы
    getMessages() {
        return [...this.messages];
    }
    
    getUnreadCount() {
        return this.unreadCount;
    }
    
    isConnected() {
        return window.gameSocket && window.gameSocket.isConnected();
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Ждем загрузки gameManager
    const initChat = () => {
        if (window.GAME_CONFIG) {
            new ChatManager();
        } else {
            setTimeout(initChat, 100);
        }
    };
    
    initChat();
});