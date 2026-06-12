"""Quick PostgreSQL connection check.

Run from the project root:

    py -3 -m db.test_connection
"""

from db.connection import connect


def main():
    """Open a connection and print the current database name."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database()")
            database_name = cur.fetchone()[0]
    print(f"db connected: {database_name}")


if __name__ == "__main__":
    main()
