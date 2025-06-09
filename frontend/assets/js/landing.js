const API_URL = 'http://localhost:8000/api/v1';

const booksGrid = document.getElementById('booksGrid');
const searchInput = document.getElementById('searchInput');
const filterButtons = document.querySelectorAll('.filter-btn');
const darkModeToggle = document.getElementById('darkModeToggle');

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

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

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
        const matchesFilter = currentFilter === 'all' || book.category === currentFilter;
        const matchesSearch = book.title.toLowerCase().includes(currentSearch.toLowerCase()) ||
                            book.author.toLowerCase().includes(currentSearch.toLowerCase()) ||
                            book.description.toLowerCase().includes(currentSearch.toLowerCase());
        return matchesFilter && matchesSearch;
    });

    if (filteredBooks.length === 0) {
        booksGrid.innerHTML = '<div class="no-books">No se encontraron libros</div>';
        return;
    }

    booksGrid.innerHTML = filteredBooks.map(book => `
        <div class="book-card">
            <img src="${book.link}" alt="${book.title}" onerror="this.src='../assets/img/default-book.jpg'">
            <div class="book-card-content">
                <h3>${book.title}</h3>
                <p class="author">${book.author}</p>
                <p class="description">${book.description || 'Sin descripción'}</p>
                <p class="category">${book.category || 'Sin categoría'}</p>
                <p class="date">${new Date(book.created_at).toLocaleDateString()}</p>
            </div>
            <div class="book-actions">
                <button class="btn btn-primary" onclick="likeBook(${book.id})">❤️ </button>
                <button class="btn btn-secondary" onclick="viewDetails(${book.id})">Ver detalles</button>
            </div>
        </div>
    `).join('');
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

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
    darkModeToggle.textContent = isDarkMode ? '☀️' : '🌙';
}

searchInput.addEventListener('input', debounce(handleSearch, 500));
filterButtons.forEach(btn => {
    btn.addEventListener('click', () => handleFilter(btn.dataset.filter));
});
window.addEventListener('scroll', handleScroll);

const savedDarkMode = localStorage.getItem('darkMode') === 'true';
if (savedDarkMode) {
    document.body.classList.add('dark-mode');
    darkModeToggle.textContent = '☀️';
}
darkModeToggle.addEventListener('click', toggleDarkMode);

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
});
