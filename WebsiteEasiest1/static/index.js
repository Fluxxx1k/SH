// JavaScript для главной страницы Secret Hitler

// Показать правила игры
function showRules() {
    document.getElementById('rulesModal').style.display = 'block';
    document.body.style.overflow = 'hidden'; // Предотвратить прокрутку фона
}

// Закрыть правила игры
function closeRules() {
    document.getElementById('rulesModal').style.display = 'none';
    document.body.style.overflow = 'auto'; // Включить прокрутку обратно
}

// Закрыть модальное окно при клике вне его
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('rulesModal');
    
    // Закрытие при клике вне модального окна
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeRules();
        }
    });
    
    // Закрытие при нажатии Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            closeRules();
        }
    });
});

// Анимация статистики при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    animateNumbers();
});

// Анимация чисел статистики
function animateNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(function(element) {
        if (element.textContent in ['0', '---', 'N/A']) {
            console.log(`Element with text ${element.textContent} skip`);
            return;
        }
        const finalValue = parseInt(element.textContent) || -1;
        if (finalValue === -1) {
            console.log(`Element with text ${element.textContent} is not a number`);
            element.textContent = '---';
            return;
        }
        let currentValue = 0;
        const increment = finalValue / 50; // 50 шагов анимации
        
        const timer = setInterval(function() {
            currentValue += increment;
            if (currentValue >= finalValue) {
                currentValue = finalValue;
                clearInterval(timer);
            }
            element.textContent = Math.floor(currentValue);
        }, 30); // Обновление каждые 30ms
    });
}

// Плавная прокрутка для внутренних ссылок
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Добавление эффектов при наведении на карточки ролей
document.addEventListener('DOMContentLoaded', function() {
    const roleCards = document.querySelectorAll('.role');
    
    roleCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});


// Обработка ошибок загрузки изображений
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    
    images.forEach(function(img) {
        img.addEventListener('error', function() {
            // Скрыть сломанные изображения или заменить на placeholder
            this.style.display = 'none';
        });
    });
});

// Предотвращение двойной отправки форм (если они есть)
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Обработка...';
            }
        });
    });
});