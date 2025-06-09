const API_URL = 'http://localhost:8000/api/v1';

// Función para mostrar mensajes de error
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message show';
    errorDiv.textContent = message;
    
    const form = document.querySelector('form');
    form.insertBefore(errorDiv, form.firstChild);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Función para guardar el token en localStorage
function saveToken(token) {
    localStorage.setItem('token', token);
}

// Función para verificar si el usuario está autenticado
function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

// Función para redirigir si el usuario está autenticado
function redirectIfAuthenticated() {
    if (isAuthenticated()) {
        window.location.href = 'landing.html';
    }
}

// Manejar el formulario de login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);
            
            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData.toString(),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al iniciar sesión');
            }
            
            const data = await response.json();
            saveToken(data.access_token);
            window.location.href = 'landing.html';
            
        } catch (error) {
            showError(error.message || 'Error de conexión');
            console.error('Error de login:', error);
        }
    });
}

// Manejar el formulario de registro
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (password !== confirmPassword) {
            showError('Las contraseñas no coinciden');
            return;
        }
        
        try {
            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    username,
                    password,
                }),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al registrar usuario');
            }
            
            window.location.href = 'login.html';
            
        } catch (error) {
            showError(error.message || 'Error de conexión');
            console.error('Error de registro:', error);
        }
    });
}

// Verificar autenticación al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    redirectIfAuthenticated();
}); 