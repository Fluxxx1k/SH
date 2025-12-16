document.addEventListener('DOMContentLoaded', () => {
    const startGameBtn = document.getElementById('startGameBtn');

    startGameBtn.addEventListener('click', () => {
        window.location.href = 'account.html';
    });
});