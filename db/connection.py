"""PostgreSQL connection helpers."""

import os

import psycopg
from dotenv import load_dotenv


def database_url():
    """Return DATABASE_URL from environment or .env."""
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set. Create a .env file first.")
    return url


def connect():
    """Open a PostgreSQL connection."""
    return psycopg.connect(database_url())
