document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío del formulario de manera tradicional

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://localhost:5000/api/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Login successful') {
            document.getElementById('message').textContent = 'Login successful!';
            document.getElementById('message').style.color = 'green';
            // Redirigir a otra página o almacenar información del usuario si es necesario
        } else {
            document.getElementById('message').textContent = data.message;
            document.getElementById('message').style.color = 'red';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('message').textContent = 'An error occurred';
        document.getElementById('message').style.color = 'red';
    });
});
