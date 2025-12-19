document.addEventListener('DOMContentLoaded', () => {
    const startGameBtn = document.getElementById('startGameBtn');
    const viewLogsBtn = document.getElementById('viewLogsBtn');

    startGameBtn.addEventListener('click', () => {
        window.location.href = 'game.html';
    });

    viewLogsBtn.addEventListener('click', () => {
        window.location.href = 'game_logs';
    });
});