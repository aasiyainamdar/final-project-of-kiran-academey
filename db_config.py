"""Database configuration.
If the MySQL password changes, THIS is the only file you must modify
(or set the environment variable RPMS_DB_PASSWORD)."""
import os

DB_CONFIG = {
    "host": os.getenv("RPMS_DB_HOST", "localhost"),
    "port": int(os.getenv("RPMS_DB_PORT", "3306")),
    "user": os.getenv("RPMS_DB_USER", "root"),
    "password": os.getenv("RPMS_DB_PASSWORD", "root"),
    "database": os.getenv("RPMS_DB_NAME", "recruitment_db"),
}
