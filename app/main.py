from fastapi import FastAPI
import logging
from app.routers import post, user, auth, vote  # Adjust imports as necessary
from app.database import engine, Base
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Log the database username to verify the environment is loaded correctly
print("Database Username:", settings.database_username)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Startup and shutdown event handlers using FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    # Automatically create all tables from models
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Application shutdown")

# Initialize FastAPI app with lifespan for startup/shutdown events
app = FastAPI(lifespan=lifespan)

# Configure CORS for development (allow all origins)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for various endpoints
app.include_router(post.router, prefix="/posts", tags=["Posts"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(vote.router, tags=["Votes"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to swypify!"}  # Updated the message to reflect swypify

# Test endpoint
@app.get("/test")
def test():
    return {"message": "Server is running"}



















