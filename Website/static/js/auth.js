/**
 * JavaScript для страниц авторизации (вход и регистрация)
 * Сохраняет стиль WebsiteEasiest и добавляет современные функции
 */

class AuthManager {
    constructor() {
        this.form = null;
        this.isLogin = AUTH_CONFIG.isLogin;
        this.csrfToken = AUTH_CONFIG.csrfToken;
        this.redirectUrl = AUTH_CONFIG.redirectUrl;
        
        this.validation = {
            username: {
                minLength: 3,
                maxLength: 20,
                pattern: /^[a-zA-Z0-9_-]+$/
            },
            email: {
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            },
            password: {
                minLength: 6
            }
        };
        
        this.init();
    }

    init() {
        this.setupForm();
        this.setupEventListeners();
        this.setupValidation();
        this.setupPasswordStrength();
        
        console.log('AuthManager инициализирован');
    }

    setupForm() {
        this.form = document.getElementById(this.isLogin ? 'loginForm' : 'registerForm');
        if (!this.form) {
            console.error('Форма не найдена');
            return;
        }
    }

    setupEventListeners() {
        if (!this.form) return;

        // Обработка отправки формы
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Валидация полей при вводе
        const inputs = this.form.querySelectorAll('.form-input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.validateField(input);
            });

            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });

        // Кнопки демо-режима
        const demoButtons = document.querySelectorAll('[onclick*="loginAsDemo"]');
        demoButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const demoType = button.getAttribute('onclick').match(/loginAsDemo\('(\w+)'\)/)?.[1];
                if (demoType) {
                    this.loginAsDemo(demoType);
                }
            });
        });

        // Обработка Enter в полях
        inputs.forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.handleSubmit();
                }
            });
        });
    }

    setupValidation() {
        if (!this.form) return;

        // Валидация имени пользователя
        const usernameInput = this.form.querySelector('#username');
        if (usernameInput) {
            usernameInput.addEventListener('input', () => {
                this.validateUsername(usernameInput);
            });
        }

        // Валидация email (только для регистрации)
        if (!this.isLogin) {
            const emailInput = this.form.querySelector('#email');
            if (emailInput) {
                emailInput.addEventListener('input', () => {
                    this.validateEmail(emailInput);
                });
            }

            // Валидация подтверждения пароля
            const confirmPasswordInput = this.form.querySelector('#confirm_password');
            if (confirmPasswordInput) {
                confirmPasswordInput.addEventListener('input', () => {
                    this.validatePasswordMatch();
                });
            }
        }
    }

    setupPasswordStrength() {
        if (this.isLogin) return;

        const passwordInput = this.form.querySelector('#password');
        const strengthFill = document.getElementById('strength-fill');
        const strengthText = document.getElementById('strength-text');

        if (!passwordInput || !strengthFill || !strengthText) return;

        passwordInput.addEventListener('input', () => {
            const password = passwordInput.value;
            const strength = this.calculatePasswordStrength(password);
            
            strengthFill.className = 'strength-fill';
            strengthFill.classList.add(`strength-${strength.level}`);
            strengthText.textContent = strength.text;
            strengthText.style.color = strength.color;
        });
    }

    calculatePasswordStrength(password) {
        let score = 0;
        
        // Длина
        if (password.length >= 6) score++;
        if (password.length >= 10) score++;
        if (password.length >= 14) score++;
        
        // Разнообразие символов
        if (/[a-z]/.test(password)) score++;
        if (/[A-Z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[^\w\s]/.test(password)) score++;
        
        // Определение уровня
        if (score <= 2) {
            return { level: 'weak', text: 'Слабый', color: '#ff6b6b' };
        } else if (score <= 4) {
            return { level: 'medium', text: 'Средний', color: '#ffa726' };
        } else {
            return { level: 'strong', text: 'Сильный', color: '#4ECDC4' };
        }
    }

    validateField(input) {
        const fieldName = input.name || input.id;
        const value = input.value.trim();
        
        let isValid = true;
        let errorMessage = '';

        switch (fieldName) {
            case 'username':
                isValid = this.validateUsername(input);
                break;
            case 'email':
                isValid = this.validateEmail(input);
                break;
            case 'password':
                isValid = this.validatePassword(input);
                break;
            case 'confirm_password':
                isValid = this.validatePasswordMatch();
                break;
            case 'terms':
                isValid = this.validateTerms();
                break;
        }

        this.showFieldError(fieldName, errorMessage);
        return isValid;
    }

    validateUsername(input) {
        const value = input.value.trim();
        const errorElement = document.getElementById('username-error');
        
        if (value.length < this.validation.username.minLength) {
            this.showFieldError('username', `Минимум ${this.validation.username.minLength} символа`);
            return false;
        }
        
        if (value.length > this.validation.username.maxLength) {
            this.showFieldError('username', `Максимум ${this.validation.username.maxLength} символов`);
            return false;
        }
        
        if (!this.validation.username.pattern.test(value)) {
            this.showFieldError('username', 'Только буквы, цифры, дефис и подчеркивание');
            return false;
        }
        
        this.showFieldError('username', '');
        return true;
    }

    validateEmail(input) {
        const value = input.value.trim();
        
        if (value && !this.validation.email.pattern.test(value)) {
            this.showFieldError('email', 'Введите корректный email');
            return false;
        }
        
        this.showFieldError('email', '');
        return true;
    }

    validatePassword(input) {
        const value = input.value;
        
        if (value.length < this.validation.password.minLength) {
            this.showFieldError('password', `Минимум ${this.validation.password.minLength} символов`);
            return false;
        }
        
        this.showFieldError('password', '');
        return true;
    }

    validatePasswordMatch() {
        const password = this.form.querySelector('#password')?.value || '';
        const confirmPassword = this.form.querySelector('#confirm_password')?.value || '';
        
        if (confirmPassword && password !== confirmPassword) {
            this.showFieldError('confirm_password', 'Пароли не совпадают');
            return false;
        }
        
        this.showFieldError('confirm_password', '');
        return true;
    }

    validateTerms() {
        const termsCheckbox = this.form.querySelector('input[name="terms"]');
        
        if (termsCheckbox && !termsCheckbox.checked) {
            this.showFieldError('terms', 'Необходимо принять условия использования');
            return false;
        }
        
        this.showFieldError('terms', '');
        return true;
    }

    showFieldError(fieldName, message) {
        const errorElement = document.getElementById(`${fieldName}-error`);
        const inputElement = this.form.querySelector(`#${fieldName}`);
        
        if (errorElement) {
            errorElement.textContent = message;
        }
        
        if (inputElement) {
            if (message) {
                inputElement.classList.add('error');
                inputElement.classList.remove('valid');
            } else {
                inputElement.classList.remove('error');
                inputElement.classList.add('valid');
            }
        }
    }

    async handleSubmit() {
        if (!this.form) return;

        // Валидация всех полей
        const inputs = this.form.querySelectorAll('.form-input[required], input[name="terms"]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        if (!isValid) {
            this.showFormError('Пожалуйста, исправьте ошибки в форме');
            return;
        }

        // Показать индикатор загрузки
        this.showLoading(true);

        try {
            const formData = new FormData(this.form);
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const result = await response.json();

            if (result.success) {
                this.showSuccess(result.message || 'Успешно!');
                
                // Перенаправление
                setTimeout(() => {
                    window.location.href = result.redirect || this.redirectUrl;
                }, 1000);
            } else {
                this.showFormError(result.message || 'Произошла ошибка');
                
                // Показать ошибки полей
                if (result.errors) {
                    Object.keys(result.errors).forEach(field => {
                        this.showFieldError(field, result.errors[field]);
                    });
                }
            }
        } catch (error) {
            console.error('Ошибка отправки формы:', error);
            this.showFormError('Произошла ошибка соединения с сервером');
        } finally {
            this.showLoading(false);
        }
    }

    showLoading(show) {
        const submitBtn = this.form.querySelector('.auth-submit');
        const submitText = submitBtn?.querySelector('.submit-text');
        const submitSpinner = submitBtn?.querySelector('.submit-spinner');
        const loadingIndicator = document.getElementById('loadingIndicator');

        if (show) {
            submitBtn?.setAttribute('disabled', 'disabled');
            if (submitText) submitText.style.display = 'none';
            if (submitSpinner) submitSpinner.style.display = 'block';
            if (loadingIndicator) loadingIndicator.style.display = 'flex';
        } else {
            submitBtn?.removeAttribute('disabled');
            if (submitText) submitText.style.display = 'block';
            if (submitSpinner) submitSpinner.style.display = 'none';
            if (loadingIndicator) loadingIndicator.style.display = 'none';
        }
    }

    showFormError(message) {
        // Удалить предыдущие сообщения
        const existingMessages = document.querySelectorAll('.auth-message');
        existingMessages.forEach(msg => msg.remove());

        if (!message) return;

        const messagesContainer = document.querySelector('.auth-messages') || this.createMessagesContainer();
        const messageElement = document.createElement('div');
        messageElement.className = 'auth-message auth-message-error';
        messageElement.innerHTML = `
            <span class="message-icon">❌</span>
            <span class="message-text">${message}</span>
            <button class="message-close" onclick="this.parentElement.remove()">×</button>
        `;
        
        messagesContainer.appendChild(messageElement);
        
        // Прокрутка к сообщению
        messageElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    showSuccess(message) {
        const messagesContainer = document.querySelector('.auth-messages') || this.createMessagesContainer();
        const messageElement = document.createElement('div');
        messageElement.className = 'auth-message auth-message-success';
        messageElement.innerHTML = `
            <span class="message-icon">✅</span>
            <span class="message-text">${message}</span>
            <button class="message-close" onclick="this.parentElement.remove()">×</button>
        `;
        
        messagesContainer.appendChild(messageElement);
    }

    createMessagesContainer() {
        const container = document.createElement('div');
        container.className = 'auth-messages';
        this.form.parentNode.insertBefore(container, this.form);
        return container;
    }

    async loginAsDemo(type) {
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/auth/demo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({ type })
            });

            const result = await response.json();

            if (result.success) {
                this.showSuccess('Демо-режим активирован!');
                setTimeout(() => {
                    window.location.href = this.redirectUrl;
                }, 1000);
            } else {
                this.showFormError(result.message || 'Не удалось активировать демо-режим');
            }
        } catch (error) {
            console.error('Ошибка демо-режима:', error);
            this.showFormError('Произошла ошибка соединения с сервером');
        } finally {
            this.showLoading(false);
        }
    }

    // Утилиты
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
}

// Глобальные функции для HTML
function togglePassword(fieldId) {
    const input = document.getElementById(fieldId);
    const toggle = input?.parentNode?.querySelector('.password-toggle .toggle-icon');
    
    if (input && toggle) {
        if (input.type === 'password') {
            input.type = 'text';
            toggle.textContent = '🙈';
        } else {
            input.type = 'password';
            toggle.textContent = '👁️';
        }
    }
}

function showDemoLogin() {
    const modal = document.getElementById('demoModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeDemoModal() {
    const modal = document.getElementById('demoModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function showTerms() {
    const modal = document.getElementById('termsModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeTermsModal() {
    const modal = document.getElementById('termsModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function acceptTerms() {
    const termsCheckbox = document.querySelector('input[name="terms"]');
    if (termsCheckbox) {
        termsCheckbox.checked = true;
        closeTermsModal();
    }
}

function loginAsDemo(type) {
    if (window.authManager) {
        window.authManager.loginAsDemo(type);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager();
    
    // Закрытие модальных окон по клику вне их
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
    
    // Закрытие модальных окон по Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (modal.style.display === 'flex') {
                    modal.style.display = 'none';
                }
            });
        }
    });
});

// Обработка выхода со страницы
window.addEventListener('beforeunload', () => {
    if (window.authManager) {
        // Очистка при необходимости
    }
});