// Datos de ejemplo de libros (normalmente vendrían de tu backend Python)
const books = [
  {
    id: 1,
    title: "Cien años de soledad",
    author: "Gabriel García Márquez",
    publisher: "Editorial Sudamericana",
    year: "1967",
    edition: "Primera edición",
    pages: "471",
    isbn: "978-84-376-0494-7",
    category: "ficcion",
    available: true,
  },
  {
    id: 2,
    title: "Sapiens: De animales a dioses",
    author: "Yuval Noah Harari",
    publisher: "Editorial Debate",
    year: "2014",
    edition: "Segunda edición",
    pages: "496",
    isbn: "978-84-9992-552-1",
    category: "historia",
    available: true,
  },
  {
    id: 3,
    title: "El arte de la programación",
    author: "Donald E. Knuth",
    publisher: "Addison-Wesley",
    year: "1968",
    edition: "Cuarta edición",
    pages: "652",
    isbn: "978-0-201-89683-1",
    category: "tecnologia",
    available: false,
  },
  {
    id: 4,
    title: "Breve historia del tiempo",
    author: "Stephen Hawking",
    publisher: "Bantam Books",
    year: "1988",
    edition: "Edición ilustrada",
    pages: "256",
    isbn: "978-84-08-06095-3",
    category: "ciencia",
    available: true,
  },
  {
    id: 5,
    title: "Historia del arte",
    author: "Ernst Gombrich",
    publisher: "Phaidon Press",
    year: "1950",
    edition: "16ª edición",
    pages: "688",
    isbn: "978-0-7148-3355-2",
    category: "arte",
    available: true,
  },
  {
    id: 6,
    title: "1984",
    author: "George Orwell",
    publisher: "Secker & Warburg",
    year: "1949",
    edition: "Edición conmemorativa",
    pages: "328",
    isbn: "978-84-376-0523-4",
    category: "ficcion",
    available: true,
  },
];

let filteredBooks = [...books];

function renderBooks(booksToRender) {
  const grid = document.getElementById("booksGrid");
  grid.innerHTML = "";

  booksToRender.forEach((book) => {
    const bookCard = document.createElement("div");
    bookCard.className = "book-card";
    bookCard.innerHTML = `
                    <div class="book-cover">
                        <img src="${book.cover}" alt="${book.title}">
                        <div class="availability-badge ${
                          book.available ? "" : "unavailable"
                        }">
                            ${book.available ? "Disponible" : "No disponible"}
                        </div>
                    </div>
                    <div class="book-info">
                        <h3 class="book-title">${book.title}</h3>
                        <p class="book-author">por ${book.author}</p>
                        <div class="book-details">
                            <div class="detail-row">
                                <span class="detail-label">Editorial:</span>
                                <span class="detail-value">${
                                  book.publisher
                                }</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Año:</span>
                                <span class="detail-value">${book.year}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Edición:</span>
                                <span class="detail-value">${
                                  book.edition
                                }</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Páginas:</span>
                                <span class="detail-value">${book.pages}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">ISBN:</span>
                                <span class="detail-value">${book.isbn}</span>
                            </div>
                        </div>
                    </div>
                    <div class="book-actions">
                        <button class="btn btn-primary" ${
                          !book.available ? "disabled" : ""
                        }>
                            ${book.available ? "Leer ahora" : "No disponible"}
                        </button>
                        <button class="btn btn-secondary">Ver detalles</button>
                    </div>
                `;
    grid.appendChild(bookCard);
  });
}

// Filtros
document.querySelectorAll(".filter-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document
      .querySelectorAll(".filter-btn")
      .forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");

    const filter = btn.dataset.filter;
    if (filter === "all") {
      filteredBooks = [...books];
    } else {
      filteredBooks = books.filter((book) => book.category === filter);
    }
    renderBooks(filteredBooks);
  });
});

// Búsqueda
document.getElementById("searchInput").addEventListener("input", (e) => {
  const searchTerm = e.target.value.toLowerCase();
  const activeFilter =
    document.querySelector(".filter-btn.active").dataset.filter;

  let booksToFilter =
    activeFilter === "all"
      ? books
      : books.filter((book) => book.category === activeFilter);

  filteredBooks = booksToFilter.filter(
    (book) =>
      book.title.toLowerCase().includes(searchTerm) ||
      book.author.toLowerCase().includes(searchTerm)
  );

  renderBooks(filteredBooks);
});

// Renderizar libros iniciales
renderBooks(books);
