document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío del formulario de manera tradicional

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const rol = document.getElementById('rol').value;

    fetch('http://127.0.0.1:5000/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
            rol: rol
        })
    })
    
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            const messageElement = document.getElementById('message');
            messageElement.textContent = 'Account created successfully! Please login.';
            
            // Estilos para el mensaje de éxito
            messageElement.style.color = 'green';
            messageElement.style.fontSize = '20px';
            messageElement.style.fontWeight = 'bold';
            messageElement.style.backgroundColor = '#e0f9e0';
            messageElement.style.padding = '10px'; 
            messageElement.style.borderRadius = '5px';
            setTimeout(() => {
                window.location.href = '/login';  // Redirige a la página de login
            }, 2000);
        } else {
            const messageElement = document.getElementById('message');
            messageElement.textContent = data.message;
        
            // Estilos para el mensaje de error
            messageElement.style.color = 'red';
            messageElement.style.fontSize = '20px'; 
            messageElement.style.fontWeight = 'bold';
            messageElement.style.backgroundColor = '#f9e0e0'; 
            messageElement.style.padding = '10px';
            messageElement.style.borderRadius = '5px';
        }        
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('message').textContent = 'An error occurred';
        document.getElementById('message').style.color = 'red';
    });
});
