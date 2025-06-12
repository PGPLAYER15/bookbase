import { fetchUserLikes, likeBook ,unlikeBook,likedBooks} from '../js/likes.js';

const API_URL = 'http://localhost:8000/api/v1';
const favoritesGrid = document.getElementById('favoritesGrid');

function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

function getToken() {
    return localStorage.getItem('token');
}

function redirectToLogin() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}

async function fetchFavoriteBooks() {
    try {
        const response = await fetch(`${API_URL}/users/me/likes`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                redirectToLogin();
                return;
            }
            throw new Error('Error al obtener los libros favoritos');
        }

        const likedBookIds = await response.json();
        
        // Obtener los detalles de cada libro
        const books = await Promise.all(
            likedBookIds.map(async (bookId) => {
                const bookResponse = await fetch(`${API_URL}/books/${bookId}`, {
                    headers: {
                        'Authorization': `Bearer ${getToken()}`
                    }
                });
                if (bookResponse.ok) {
                    return bookResponse.json();
                }
                return null;
            })
        );

        return books.filter(book => book !== null);
    } catch (error) {
        console.error('Error:', error);
        showError('Error al cargar los libros favoritos');
        return [];
    }
}

function renderFavoriteBooks(books) {
    if (books.length === 0) {
        favoritesGrid.innerHTML = `
            <div class="empty-favorites">
                <h2>No tienes libros favoritos</h2>
                <p>¡Explora nuestra biblioteca y guarda tus libros favoritos!</p>
                <a href="landing.html" class="btn">Explorar libros</a>
            </div>
        `;
        return;
    }

    favoritesGrid.innerHTML = books.map(book => `
        <div class="book-card">
            <img src="${book.link}" alt="${book.title}" onerror="this.src='../assets/img/no-image.png'">
            <div class="book-card-content">
                <h3>${book.title}</h3>
                <p class="author">${book.author}</p>
                <p class="description">${book.description || 'Sin descripción'}</p>
                <p class="category">${book.category || 'Sin categoría'}</p>
                <p class="date">${new Date(book.created_at).toLocaleDateString()}</p>
            </div>
            <div class="book-actions">
                <button class="like-button liked" data-book-id="${book.id}">❤️</button>
                <button class="btn btn-secondary" onclick="viewDetails(${book.id})">Ver detalles</button>
            </div>
        </div>
    `).join('');

    
    // Agregar event listeners a los botones de like
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', async () => {
            const bookId = parseInt(button.dataset.bookId);
    
            if (likedBooks.has(bookId)) {
                console.log('Este libro ya tiene like.');
                unlikeBook(bookId);
                return; 
            }
            likeBook(bookId);
    
            likedBooks.add(bookId);
        });
    });

    
}

function showError(message) {
    favoritesGrid.innerHTML = `<div class="error">${message}</div>`;
}

document.addEventListener('DOMContentLoaded', async () => {
    redirectToLogin();
    const favoriteBooks = await fetchFavoriteBooks();
    renderFavoriteBooks(favoriteBooks);
});
