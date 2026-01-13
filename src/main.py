from fastapi import FastAPI
from src.config import settings
from src.routes.health import router as health_router
from src.routes.ping import router as ping_router
from src.errors import global_exception_handler

app = FastAPI(title=settings.APP_NAME)

# Register routers
app.include_router(health_router)
app.include_router(ping_router)

# Register global error handler
app.add_exception_handler(Exception, global_exception_handler)
