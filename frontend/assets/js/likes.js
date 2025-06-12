const API_URL = 'http://localhost:8000/api/v1';

export async function likeBook(bookId) {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }

    const token = getToken();
    console.log('Token:', token); // Debug: Ver el token

    try {
        const response = await fetch(`${API_URL}/books/${bookId}/like`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('Response status:', response.status); // Debug: Ver el status de la respuesta

        if (response.ok) {
            const likeButton = document.querySelector(`[data-book-id="${bookId}"]`);
            if (likeButton) {
                likeButton.innerHTML = '❤️';
                likeButton.classList.add('liked');
            }
        } else if (response.status === 400) {
            await unlikeBook(bookId);
        } else if (response.status === 401) {
            console.log('Token inválido o expirado'); // Debug: Ver si el token es inválido
            localStorage.removeItem('token'); // Limpiar el token inválido
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Error al actualizar el like. Por favor, intenta de nuevo.');
    }
}

export async function unlikeBook(bookId) {
    try {
        const response = await fetch(`${API_URL}/books/${bookId}/like`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (response.ok) {
            const likeButton = document.querySelector(`[data-book-id="${bookId}"]`);
            if (likeButton) {
                console.log("likeButton", likeButton);
                likeButton.innerHTML = '🤍';
                likeButton.classList.remove('liked');
                
            }
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Error al actualizar el like. Por favor, intenta de nuevo.');
    }
}

export let likedBooks = new Set();

export async function fetchUserLikes() {
    try {
        const response = await fetch(`${API_URL}/users/me/likes`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (!response.ok) {
            throw new Error('Error al obtener los likes');
        }

        const likedBooks = await response.json();
        return likedBooks;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

export function updateLikeButtons(likedBooks) {
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        const bookId = button.dataset.bookId;
        if (likedBooks.includes(parseInt(bookId))) {
            button.classList.add('liked');
            button.innerHTML = '❤️';
        } else {
            button.classList.remove('liked');
            button.innerHTML = '🤍';
        }
    });
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 3000);
}

function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

function getToken() {
    return localStorage.getItem('token');
}

// Inicializar los likes cuando se carga la página
document.addEventListener('DOMContentLoaded', async () => {
    if (isAuthenticated()) {
        const likedBooks = await fetchUserLikes();
        updateLikeButtons(likedBooks);
    }
});