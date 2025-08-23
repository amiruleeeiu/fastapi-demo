from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.controllers import post_controller
from app.controllers import auth_controller
from app.database import Base, engine, get_db
from app.models.user import User
from app.controllers.user_controller import router as user_router
import logging

from app.services.post_service import PostService
logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="FastAPI Demo", description="FastAPI Demo", version="1.0.3")

@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error"
        }
    )

# Include routers
app.include_router(user_router)
app.include_router(post_controller.router)
app.include_router(auth_controller.router)

@app.on_event("startup")
async def startup_event():
    # Database table create startup e korুন, import time e na
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users