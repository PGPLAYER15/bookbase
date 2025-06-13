import { fetchUserLikes, updateLikeButtons, likeBook, unlikeBook, likedBooks } from './likes.js';

const API_URL = 'http://localhost:8000/api/v1';

const booksGrid = document.getElementById('booksGrid');
const searchInput = document.getElementById('searchInput');
const filterButtons = document.querySelectorAll('.filter-btn');

let currentFilter = 'all';
let currentSearch = '';
let books = [];
let currentPage = 0;
const booksPerPage = 12;
let isLoading = false;
let hasMoreBooks = true;

function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}

function redirectToLogin() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}

function getToken() {
    return localStorage.getItem('token');
}

export function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

window.logout = logout;

async function fetchBooks(reset = false) {
    if (isLoading || (!hasMoreBooks && !reset)) return;
    
    try {
        isLoading = true;
        if (reset) {
            currentPage = 0;
            books = [];
            hasMoreBooks = true;
        }

        const skip = currentPage * booksPerPage;
        let url = `${API_URL}/books?skip=${skip}&limit=${booksPerPage}`;

        if (currentFilter !== 'all') {
            url += `&category=${currentFilter}`;
        }

        if (currentSearch.length > 0) {
            url += `&search=${encodeURIComponent(currentSearch)}`;
        }

        const headers = {
            'Authorization': `Bearer ${getToken()}`
        };

        const response = await fetch(url, { headers });
        if (!response.ok) {
            if (response.status === 401) {
                redirectToLogin();
                return;
            }
            throw new Error('Error al obtener los libros');
        }

        const newBooks = await response.json();
        if (newBooks.length < booksPerPage) {
            hasMoreBooks = false;
        }

        books = reset ? newBooks : [...books, ...newBooks];
        currentPage++;

        renderBooks();
    } catch (error) {
        console.error('Error:', error);
        showError('Error al cargar los libros. Por favor, intenta de nuevo.');
    } finally {
        isLoading = false;
    }
}

function renderBooks() {
    const filteredBooks = books.filter(book => {
        const matchesSearch = book.title.toLowerCase().includes(currentSearch.toLowerCase()) ||
                              book.author.toLowerCase().includes(currentSearch.toLowerCase()) ||
                              book.description.toLowerCase().includes(currentSearch.toLowerCase());
        return matchesSearch;
    });

    if (filteredBooks.length === 0) {
        booksGrid.innerHTML = '<div class="no-books">No se encontraron libros</div>';
        return;
    }

    booksGrid.innerHTML = filteredBooks.map(book => createBookCard(book)).join('');

    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', async () => {
            const bookId = parseInt(button.dataset.bookId);
    
            if (likedBooks.has(bookId)) {
                console.log('Este libro ya tiene like.');
                unlikeBook(bookId);
                likedBooks.delete(bookId);
                return; 
            }
            likeBook(bookId);
            likedBooks.add(bookId);
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
                <button class="like-button" data-book-id="${book.id}">🤍</button>
                <button class="btn btn-secondary" onclick="viewDetails(${book.id})">Ver detalles</button>
            </div>
        </div>
    `;
}

function handleSearch() {
    const searchTerm = searchInput.value.trim();
    if (searchTerm.length >= 2 || searchTerm.length === 0) {
        currentSearch = searchTerm;
        fetchBooks(true);
    }
}

function handleFilter(filter) {
    currentFilter = filter;
    filterButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
    });
    fetchBooks(true);
}

function showError(message) {
    booksGrid.innerHTML = `<div class="error">${message}</div>`;
}

function handleScroll() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
        fetchBooks();
    }
}

searchInput.addEventListener('input', debounce(handleSearch, 500));
filterButtons.forEach(btn => {
    btn.addEventListener('click', () => handleFilter(btn.dataset.filter));
});
window.addEventListener('scroll', handleScroll);

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

document.addEventListener('DOMContentLoaded', () => {
    redirectToLogin();
    fetchBooks();
    const addBookBtn = document.getElementById('addBookBtn');
    const userType = localStorage.getItem('user_type');
    if (addBookBtn) {
        if (userType === 'writer') {
            addBookBtn.style.display = 'inline-block';
        } else {
            addBookBtn.style.display = 'none';
        }
    }
});

function viewDetails(bookId) {
    window.location.href = `detalles.html?id=${bookId}`;
}

window.viewDetails = viewDetails;
