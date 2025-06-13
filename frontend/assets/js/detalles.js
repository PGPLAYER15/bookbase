import { likeBook, unlikeBook, fetchUserLikes } from './likes.js';

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const bookId = urlParams.get('id');

    if (!bookId) {
        window.location.href = 'landing.html';
        return;
    }

    try {
        const response = await fetch(`http://localhost:8000/api/v1/books/${bookId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Error al cargar los detalles del libro');
        }

        const book = await response.json();

        const driveUrl = book.link;
        const fileId = driveUrl.match(/[-\w]{25,}/);
        if (fileId) {
            document.getElementById('bookImage').src = `https://drive.google.com/thumbnail?id=${fileId[0]}&sz=w400`;
        } else {
            document.getElementById('bookImage').src = book.link;
        }

        document.getElementById('bookTitle').textContent = book.title;
        document.getElementById('bookAuthor').textContent = book.author;
        document.getElementById('bookCategory').textContent = book.category;
        document.getElementById('bookDescription').textContent = book.description;

        const readButton = document.getElementById('readButton');
        const bookFrame = document.getElementById('bookFrame');
        const loadingMessage = document.getElementById('loadingMessage');

        readButton.addEventListener('click', () => {
            loadingMessage.style.display = 'none';
            bookFrame.style.display = 'block';
            const driveUrl = book.link;
            const fileId = driveUrl.match(/[-\w]{25,}/);
            if (fileId) {
                bookFrame.src = `https://drive.google.com/file/d/${fileId[0]}/preview`;
            } else {
                bookFrame.src = book.link;
            }
        });

        const likeButton = document.getElementById('likeButton');
        const likedBooks = await fetchUserLikes();
        if (likedBooks.includes(parseInt(bookId))) {
            likeButton.textContent = '❤️';
            likeButton.classList.add('liked');
        }

        likeButton.addEventListener('click', async () => {
            if (likeButton.classList.contains('liked')) {
                await unlikeBook(bookId);
                likeButton.textContent = '🤍';
                likeButton.classList.remove('liked');
            } else {
                await likeBook(bookId);
                likeButton.textContent = '❤️';
                likeButton.classList.add('liked');
            }
        });

    } catch (error) {
        alert(error.message);
        window.location.href = 'landing.html';
    }
});

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

window.logout = logout; 