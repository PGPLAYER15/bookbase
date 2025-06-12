
# 📚 Biblioteca Digital - BookBase

## 📋 Descripción del Proyecto
**BookBase** es una aplicación web de biblioteca digital que permite a los usuarios gestionar libros, escribir reseñas y dar "me gusta" a sus libros favoritos. El proyecto implementa una arquitectura limpia con separación de responsabilidades usando el patrón Repository y Service Layer.

---

## 🏗️ Arquitectura del Sistema

### Backend (Python - FastAPI)
- **Framework**: FastAPI  
- **ORM**: SQLAlchemy 2.0  
- **Base de datos**: PostgreSQL (usando PyMySQL)  
- **Arquitectura**: Clean Architecture con patrones Repository y Service Layer  
- **Autenticación**: JWT tokens con `bcrypt` para hash de contraseñas

### Frontend
- **Tecnologías**: HTML5, CSS3, JavaScript (vanilla)  
- **Diseño**: Responsive con gradientes modernos y efectos *glassmorphism*  
- **Funcionalidades**: Búsqueda, filtros, visualización de libros

---

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── interfaces/
│   │   ├── Ibook_repository.py
│   │   ├── Ireview_repository.py
│   │   ├── Iuser_repository.py
│   │   └── Iuser_likes_repository.py
│   ├── models/
│   │   ├── book.py
│   │   ├── review.py
│   │   ├── user.py
│   │   └── user_likes.py
│   ├── schemas/
│   │   ├── book.py
│   │   ├── review.py
│   │   ├── user.py
│   │   └── user_likes.py
│   ├── repositories/
│   │   ├── book_repositor.py
│   │   ├── review_repository.py
│   │   ├── user_repository.py
│   │   └── user_likes_repository.py
│   └── services/
│       ├── book_service.py
│       ├── review_service.py
│       ├── user_service.py
│       └── user_likes_service.py
└── requirements.txt

frontend/
├── pages/
│   ├── landing.html
│   ├── login.html
│   └── registro.html
└── style.css
```

---

## 🗃️ Modelo de Datos

### Entidades Principales

#### User (Usuario)
```python
- id: int (PK)
- username: str (unique, 3-50 chars)
- email: str (unique)
- admin: bool (default: False)
- hashed_password: str
- reviews: List[Review] (relación 1:N)
- liked_books: List[Book] (relación N:M)
```

#### Book (Libro)
```python
- id: int (PK)
- title: str (unique, max 255 chars)
- link: HttpUrl (unique, opcional)
- description: str (max 1000 chars, opcional)
- reviews: List[Review] (relación 1:N)
- liked_by_users: List[User] (relación N:M)
```

#### Review (Reseña)
```python
- id: int (PK)
- comment: str (max 500 chars, opcional)
- rating: float (1.0-5.0)
- created_at: datetime
- book_id: int (FK)
- user_id: int (FK)
- book: Book (relación N:1)
- user: User (relación N:1)
```

#### UserLikes (Tabla de asociación)
```python
- user_id: int (FK, PK)
- book_id: int (FK, PK)
```

---

## 🔧 Configuración e Instalación

### Prerrequisitos
- Python 3.8+
- MySQL Server
- pip (gestor de paquetes de Python)

### Instalación del Backend
```bash
git clone <repository-url>
cd biblioteca-digital/backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Configurar base de datos
Crear archivo `.env`:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost/biblioteca_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Ejecutar migraciones
```bash
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

#### Iniciar servidor
```bash
uvicorn app.main:app --reload
```

### Configuración del Frontend
Frontend estático. Puede abrirse directamente en el navegador.

---

## 📚 API Endpoints

### Autenticación
- `POST /auth/login` - Iniciar sesión
- `POST /auth/register` - Registrar usuario

### Usuarios
- `GET /users/{user_id}`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

### Libros
- `GET /books/`
- `GET /books/{book_id}`
- `POST /books/`
- `PUT /books/{book_id}`
- `DELETE /books/{book_id}`

### Reseñas
- `GET /reviews/book/{book_id}`
- `GET /reviews/user/{user_id}`
- `POST /reviews/`
- `PUT /reviews/{review_id}`
- `DELETE /reviews/{review_id}`

### Likes
- `POST /likes/`
- `DELETE /likes/{user_id}/{book_id}`
- `GET /likes/user/{user_id}`
- `GET /likes/book/{book_id}/count`

---

## 🔒 Seguridad

### Autenticación y Autorización
- JWT Tokens
- bcrypt para hash de contraseñas
- Validación con Pydantic

### Validaciones Implementadas
- Email único
- Username (3-50 caracteres)
- Rating (1.0-5.0)
- URLs válidas
- Sanitización de entrada

---

## 🎨 Características del Frontend

### Diseño Moderno
- Efecto Glassmorphism
- Gradientes suaves
- Responsive
- Animaciones suaves

### Funcionalidades
- Búsqueda en tiempo real
- Filtros por categoría
- Cards interactivas
- Estados visuales

---

## 🧪 Testing

### Estructura Recomendada
```
tests/
├── unit/
│   ├── test_repositories/
│   ├── test_services/
│   └── test_schemas/
├── integration/
│   ├── test_api/
│   └── test_database/
└── fixtures/
    └── test_data.py
```

### Comandos
```bash
pip install pytest pytest-asyncio httpx
pytest
pytest --cov=app
```

---

## 🚀 Despliegue

### Producción
- Configurar `.env`
- Usar Gunicorn + Uvicorn
- Logging, monitoreo
- Seguridad: CORS, middleware

### Dockerfile
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📝 Dependencias Principales

- FastAPI (0.115.12)
- SQLAlchemy (2.0.40)
- Pydantic (2.11.4)
- PyMySQL (1.1.1)
- Uvicorn (0.34.2)
