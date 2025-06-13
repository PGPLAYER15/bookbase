document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('publicarForm');
    const token = localStorage.getItem('token');

    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = document.getElementById('titulo').value;
        const author = document.getElementById('autor').value;
        const category = document.getElementById('genero').value;
        const description = document.getElementById('descripcion').value;
        const link = document.getElementById('link').value;

        if (!/^[a-zA-Z\s]+$/.test(title)) {
            alert('El título solo puede contener letras y espacios');
            return;
        }

        if (title.length > 255) {
            alert('El título no puede tener más de 255 caracteres');
            return;
        }

        if (author.length > 255) {
            alert('El autor no puede tener más de 255 caracteres');
            return;
        }

        if (description && description.length > 1000) {
            alert('La descripción no puede tener más de 1000 caracteres');
            return;
        }

        if (category && category.length > 50) {
            alert('La categoría no puede tener más de 50 caracteres');
            return;
        }

        try {
            new URL(link);
        } catch (e) {
            alert('Por favor, ingresa una URL válida');
            return;
        }

        const bookData = {
            title: title,
            author: author,
            category: category,
            description: description,
            link: link
        };

        try {
            const response = await fetch('http://localhost:8000/api/v1/books', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(bookData)
            });

            if (response.ok) {
                alert('Libro publicado exitosamente');
                window.location.href = 'landing.html';
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Error al publicar el libro');
            }
        } catch (error) {
            alert(error.message);
        }
    });
}); 