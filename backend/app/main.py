from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.core.api import api_router

# --------------------------
# 1. Configuración Inicial
# --------------------------
app = FastAPI(
    title="Book API",
    description="API para gestión de libros, usuarios y reseñas",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

# --------------------------
# 2. Configuración CORS (Comunicación entre frontend/backend)
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# 3. Conexión con Base de Datos
# --------------------------
@app.on_event("startup")
async def startup():
    # Crea las tablas si no existen (solo para desarrollo)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Base de datos conectada")

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    print("❌ Conexión con base de datos cerrada")

# --------------------------
# 4. Incluir Routers
# --------------------------
app.include_router(api_router, prefix="/api/v1")

# --------------------------
# 5. Health Check (Endpoint básico de prueba)
# --------------------------
@app.get("/")
def health_check():
    return {
        "status": "running",
        "version": app.version,
        "docs": "/docs"
    }