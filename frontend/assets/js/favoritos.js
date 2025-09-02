import { fetchUserLikes, likeBook, unlikeBook } from './likes.js';

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    try {
        const likedBooks = await fetchUserLikes();
        if (likedBooks.length === 0) {
            document.getElementById('booksGrid').innerHTML = `
                <div class="empty-favorites">
                    <h2>No tienes libros favoritos</h2>
                    <p>¡Explora nuestra biblioteca y guarda tus libros favoritos!</p>
                    <a href="landing.html" class="btn">Explorar libros</a>
                </div>
            `;
            return;
        }

        const booksPromises = likedBooks.map(bookId => 
            fetch(`http://localhost:8000/api/v1/books/${bookId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }).then(res => res.json())
        );

        const books = await Promise.all(booksPromises);
        displayBooks(books);
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar los libros favoritos');
    }
});

function displayBooks(books) {
    const booksGrid = document.getElementById('booksGrid');
    booksGrid.innerHTML = books.map(book => createBookCard(book)).join('');

    // Configurar los botones de like
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', async () => {
            const bookId = parseInt(button.dataset.bookId);
            await unlikeBook(bookId);
            // Remover la tarjeta del libro
            button.closest('.book-card').remove();
            // Si no quedan libros, mostrar mensaje
            if (document.querySelectorAll('.book-card').length === 0) {
                booksGrid.innerHTML = `
                    <div class="empty-favorites">
                        <h2>No tienes libros favoritos</h2>
                        <p>¡Explora nuestra biblioteca y guarda tus libros favoritos!</p>
                        <a href="landing.html" class="btn">Explorar libros</a>
                    </div>
                `;
            }
        });
    });
}

function createBookCard(book) {
    const driveUrl = book.link;
    const fileId = driveUrl.match(/[-\w]{25,}/);
    const coverUrl = fileId ? 
        `https://drive.google.com/thumbnail?id=${fileId[0]}&sz=w400` : 
        book.link;

    return `
        <div class="book-card">
            <div class="book-image">
                <img
                    src="${coverUrl}" 
                    alt="${book.title}" 
                    onerror="this.onerror=null; this.src='../assets/img/no-image.png';"
                    loading="lazy">
            </div>
            <div class="book-info">
                <h3>${book.title}</h3>
                <p class="author">${book.author}</p>
                <p class="category">${book.category}</p>
                <p class="description">${book.description}</p>
            </div>
            <div class="book-actions">
                <button class="like-button liked" data-book-id="${book.id}">❤️</button>
                <button class="btn btn-secondary" onclick="viewDetails(${book.id})">Ver detalles</button>
            </div>
        </div>
    `;
}

function viewDetails(bookId) {
    window.location.href = `detalles.html?id=${bookId}`;
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

window.viewDetails = viewDetails;
window.logout = logout;
