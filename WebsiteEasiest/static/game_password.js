document.getElementById('passwordForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`/game/${gameName}/verify_password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });

        const result = await response.json();

        if (result.success) {
            window.location.href = `/game/${gameName}`;
        } else {
            document.getElementById('message').textContent = result.message;
            document.getElementById('message').style.color = 'red';
        }
    } catch (error) {
        document.getElementById('message').textContent = 'Ошибка соединения';
        document.getElementById('message').style.color = 'red';
    }
});