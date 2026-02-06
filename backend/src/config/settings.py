import logging
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# CRITICAL: Set Google Cloud environment variables IMMEDIATELY for Vertex AI
# These must be set before any Google imports happen
GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

if GOOGLE_GENAI_USE_VERTEXAI:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = GOOGLE_GENAI_USE_VERTEXAI
if GOOGLE_CLOUD_PROJECT:
    os.environ["GOOGLE_CLOUD_PROJECT"] = GOOGLE_CLOUD_PROJECT
if GOOGLE_CLOUD_LOCATION:
    os.environ["GOOGLE_CLOUD_LOCATION"] = GOOGLE_CLOUD_LOCATION


# Configuration for the application
# Password policy
# These settings are used to enforce password complexity requirements
MIN_PASSWORD_LENGTH = 3
REQUIRE_UPPERCASE = False
REQUIRE_LOWERCASE = False
REQUIRE_DIGIT = False
REQUIRE_SPECIAL_CHAR = False
SPECIAL_CHARACTERS_REGEX_PATTERN = r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~`]"

# FREE TEER SETTINGS

MAX_COURSE_CREATIONS = 10
MAX_CHAT_USAGE = 100
MAX_PRESENT_COURSES = 5



# JWT settings
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_please_change_me")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "fallback-key-for-dev")


######
#ALGORITHM: str = "RS256"
#### Private Key (zum Signieren)
# openssl genrsa -out private.pem 2048
#### Public Key (zum Verifizieren)
# openssl rsa -in private.pem -pubout -out public.pem
PUBLIC_KEY: str = os.getenv("PUBLIC_KEY", "")
PRIVATE_KEY: str =  os.getenv("PRIVATE_KEY", "")
######


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "360000")) # 100h
SECURE_COOKIE = os.getenv("SECURE_COOKIE", "true").lower() == "true"


# Database settings
DB_USER = os.getenv("DB_USER", "nexora_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_secure_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306") 
DB_NAME = os.getenv("DB_NAME", "nexora_db")

# Allow direct override via DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    # Fallback to construction from components
    # Check if we should use MySQL or PostgreSQL based on port or another env var
    if DB_PORT == "3306" or "mysql" in DB_USER or "nexora_db" in DB_NAME:
        # Use MySQL with pymysql driver
        SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # Default to PostgreSQL (Supabase)
        SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Derive async URL for ADK and other async needs
ASYNC_SQLALCHEMY_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
if not ASYNC_SQLALCHEMY_DATABASE_URL:
    ASYNC_SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL
    if ASYNC_SQLALCHEMY_DATABASE_URL.startswith("sqlite://"):
        ASYNC_SQLALCHEMY_DATABASE_URL = ASYNC_SQLALCHEMY_DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
    elif ASYNC_SQLALCHEMY_DATABASE_URL.startswith("postgresql+psycopg2://"):
        ASYNC_SQLALCHEMY_DATABASE_URL = ASYNC_SQLALCHEMY_DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    elif ASYNC_SQLALCHEMY_DATABASE_URL.startswith("mysql+pymysql://"):
        ASYNC_SQLALCHEMY_DATABASE_URL = ASYNC_SQLALCHEMY_DATABASE_URL.replace("mysql+pymysql://", "mysql+aiomysql://")

# DB Pooling Settings
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", 3600))
DB_POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 5))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 10))
DB_CONNECT_TIMEOUT = int(os.getenv("DB_CONNECT_TIMEOUT", 10))  # Optional


# Google OAuth settings
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://www.learnweave.ai/api/google/callback")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "https://www.learnweave.ai/google/callback")

# Note: GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION are set at the top of this file

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "https://www.learnweave.ai/api/github/callback")

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "https://www.learnweave.ai/api/discord/callback")



UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_SECRET_KEY = os.getenv("UNSPLASH_SECRET_KEY")


CHROMA_DB_URL = os.getenv("CHROMA_DB_URL", "http://localhost:8000")


AGENT_DEBUG_MODE = os.getenv("AGENT_DEBUG_MODE", "true").lower() == "true"