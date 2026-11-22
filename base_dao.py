"""BaseDAO: one place that runs parameterised SQL, handles errors and connections."""
from mysql.connector import Error

from exception.custom_exceptions import DatabaseException, DuplicateRecordException
from util.db_connection import get_connection
from util.logger import get_logger

log = get_logger(__name__)


class BaseDAO:
    def _run(self, query, params=(), conn=None, mode="all"):
        """mode: all | one | insert | update.  If conn is given the caller controls commit."""
        own = conn is None
        conn = conn or get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(query, params)          # parameterised SQL -> prevents SQL injection
            if mode == "all":
                result = cur.fetchall()
            elif mode == "one":
                result = cur.fetchone()
            elif mode == "insert":
                result = cur.lastrowid
            else:
                result = cur.rowcount
            if own:
                conn.commit()
            return result
        except Error as e:
            if own:
                conn.rollback()
            log.error("SQL error %s : %s", e.errno, e.msg)
            if e.errno == 1062:
                raise DuplicateRecordException("Duplicate record: " + e.msg) from e
            raise DatabaseException(e.msg) from e
        finally:
            cur.close()
            if own:
                conn.close()

    def fetch_all(self, q, p=(), conn=None):
        return self._run(q, p, conn, "all")

    def fetch_one(self, q, p=(), conn=None):
        return self._run(q, p, conn, "one")

    def insert(self, q, p=(), conn=None):
        return self._run(q, p, conn, "insert")

    def update(self, q, p=(), conn=None):
        return self._run(q, p, conn, "update")
