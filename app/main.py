"""
Este archivo corresponde al punto de entrada principal de la aplicación.
Se encarga de configurar la API con FastAPI, inicializar la base de datos,
registrar los controladores del sistema, habilitar la comunicación entre el
frontend y el backend mediante CORS, y ejecutar el servidor de la
aplicación.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import init_db
from app.controller.auth_controller_api import router as auth_router
from app.controller.beneficiario_controller_api import router as beneficiario_router
from app.controller.recurso_alimenticio_controller_api import router as recurso_router
from app.controller.entrega_alimentaria_controller_api import router as entrega_router
from app.controller.reporte_controller_api import router as reporte_router
from app.service.auth_service import AuthService

app = FastAPI(title="Manos Solidarias API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
AuthService().asegurar_admin_por_defecto()

app.include_router(auth_router)
app.include_router(beneficiario_router)
app.include_router(recurso_router)
app.include_router(entrega_router)
app.include_router(reporte_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
