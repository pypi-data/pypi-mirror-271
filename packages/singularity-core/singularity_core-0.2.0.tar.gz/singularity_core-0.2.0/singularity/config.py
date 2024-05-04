import os

# Application settings
APP_NAME = os.getenv("APP_NAME", "FastAPI app")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION")
APP_VERSION = os.getenv("APP_VERSION")
LICENSE_NAME = os.getenv("LICENSE")
CONTACT_NAME = os.getenv("CONTACT_NAME")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")

# Cryptography settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# SQLite settings
SQLITE_URI = os.getenv("SQLITE_URI", "./sql_app.db")
SQLITE_SYNC_PREFIX = os.getenv("SQLITE_SYNC_PREFIX", "sqlite:///")
SQLITE_ASYNC_PREFIX = os.getenv("SQLITE_ASYNC_PREFIX", "sqlite+aiosqlite:///")

# MySQL settings
MYSQL_USER = os.getenv("MYSQL_USER", "username")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_SERVER = os.getenv("MYSQL_SERVER", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 5432))
MYSQL_DB = os.getenv("MYSQL_DB", "dbname")
MYSQL_URI = f"{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
MYSQL_SYNC_PREFIX = os.getenv("MYSQL_SYNC_PREFIX", "mysql://")
MYSQL_ASYNC_PREFIX = os.getenv("MYSQL_ASYNC_PREFIX", "mysql+aiomysql://")

# PostgreSQL settings
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_URI = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_SYNC_PREFIX = os.getenv("POSTGRES_SYNC_PREFIX", "postgresql://")
POSTGRES_ASYNC_PREFIX = os.getenv("POSTGRES_ASYNC_PREFIX", "postgresql+asyncpg://")

# First user settings
ADMIN_NAME = os.getenv("ADMIN_NAME", "admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@admin.com")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "!Ch4ng3Th1sP4ssW0rd!")

# Test settings
TEST_NAME = os.getenv("TEST_NAME", "Tester User")
TEST_EMAIL = os.getenv("TEST_EMAIL", "test@tester.com")
TEST_USERNAME = os.getenv("TEST_USERNAME", "testeruser")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "Str1ng$t")

# Redis settings
REDIS_CACHE_HOST = os.getenv("REDIS_CACHE_HOST", "localhost")
REDIS_CACHE_PORT = int(os.getenv("REDIS_CACHE_PORT", 6379))
REDIS_CACHE_URL = f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}"

# Client-side cache settings
CLIENT_CACHE_MAX_AGE = int(os.getenv("CLIENT_CACHE_MAX_AGE", 60))

# Redis queue settings
REDIS_QUEUE_HOST = os.getenv("REDIS_QUEUE_HOST", "localhost")
REDIS_QUEUE_PORT = int(os.getenv("REDIS_QUEUE_PORT", 6379))

# Redis rate limiter settings
REDIS_RATE_LIMIT_HOST = os.getenv("REDIS_RATE_LIMIT_HOST", "localhost")
REDIS_RATE_LIMIT_PORT = int(os.getenv("REDIS_RATE_LIMIT_PORT", 6379))
REDIS_RATE_LIMIT_URL = f"redis://{REDIS_RATE_LIMIT_HOST}:{REDIS_RATE_LIMIT_PORT}"

# Default rate limit settings
DEFAULT_RATE_LIMIT_LIMIT = int(os.getenv("DEFAULT_RATE_LIMIT_LIMIT", 10))
DEFAULT_RATE_LIMIT_PERIOD = int(os.getenv("DEFAULT_RATE_LIMIT_PERIOD", 3600))

# Environment settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
