"""MySQL connection helper + transaction context manager."""
from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error

from config.db_config import DB_CONFIG
from exception.custom_exceptions import DatabaseException
from util.logger import get_logger

log = get_logger(__name__)


def get_connection():
    """Open a new MySQL connection using DB_CONFIG."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        log.error("DB connection failed: %s", e)
        raise DatabaseException(f"Cannot connect to database: {e.msg}") from e


@contextmanager
def transaction():
    """Run several DAO calls atomically: commit on success, rollback on error."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        log.exception("Transaction rolled back")
        raise
    finally:
        conn.close()
