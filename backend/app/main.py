from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.core.api import api_router


app = FastAPI(
    title="Book API",
    description="API para gestión de libros, usuarios y reseñas",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bookbase-nine.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Base de datos conectada")

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
    print("❌ Conexión con base de datos cerrada")


app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {
        "status": "running",
        "version": app.version,
        "docs": "/docs"
    }