import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
from dataclasses import dataclass, fields
from typing import Any, Dict, List, Optional, Type, TypeVar

from services.environment_service import get_env_var

# die zwei unteren Klassen können gelöscht werden, sobald eigene Cases implementiert sind.
# solange dienen sie noch als Vorlage

@dataclass
class Person:
    id: int
    name: str
    age: int

@dataclass
class Product:
    id: int
    name: str
    price: float

T = TypeVar('T')

class PostgresRepository:
    def __init__(self, dbname: str, host: str: str, port: int = 5432) -> None:
        self.dbname = dbname
        self.user = get_env_var('DB_USER')
        self.password = get_env_var('DB_PASSWORD')
        self.host = host
        self.port = port

    @contextmanager
    def _get_connection(self) -> psycopg2.extensions.connection:
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        try:
            yield conn
        except psycopg2.DatabaseError as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                columns_with_types = ', '.join(f"{col} {dtype}" for col, dtype in columns.items())
                cur.execute(sql.SQL(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types});"))
                conn.commit()

    def insert(self, table_name: str, data: Dict[str, Any]) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                columns = data.keys()
                values = [data[col] for col in columns]
                insert_statement = sql.SQL(
                    f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
                )
                cur.execute(insert_statement, values)
                conn.commit()

    def fetch_all(self, table_name: str, cls: Type[T]) -> List[T]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL(f"SELECT * FROM {table_name};"))
                rows = cur.fetchall()
                return [self._map_row_to_object(row, cls) for row in rows]

    def fetch_by_id(self, table_name: str, record_id: int, cls: Type[T]) -> Optional[T]:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL(f"SELECT * FROM {table_name} WHERE id = %s;"), (record_id,))
                row = cur.fetchone()
                if row:
                    return self._map_row_to_object(row, cls)
                return None

    def update(self, table_name: str, record_id: int, data: Dict[str, Any]) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                set_clause = ', '.join(f"{col} = %s" for col in data.keys())
                values = list(data.values()) + [record_id]
                update_statement = sql.SQL(
                    f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
                )
                cur.execute(update_statement, values)
                conn.commit()

    def delete(self, table_name: str, record_id: int) -> None:
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql.SQL(f"DELETE FROM {table_name} WHERE id = %s;"), (record_id,))
                conn.commit()

    def _map_row_to_object(self, row: tuple, cls: Type[T]) -> T:
        field_names = [field.name for field in fields(cls)]
        return cls(**dict(zip(field_names, row)))

"""
# Example usage:
AUSSERHALB VON PYTHON
Umgebungsvariabel setzen
Windows:
set DB_USER=your_user
set DB_PASSWORD=your_password

MacOS / Linux
export DB_USER=your_user
export DB_PASSWORD=your_password


PYTHON FILE
if __name__ == "__main__":
    repo = PostgresRepository(dbname='your_db')

    # Create a table for Person
    repo.create_table('person_table', {'id': 'SERIAL PRIMARY KEY', 'name': 'VARCHAR(100)', 'age': 'INT'})

    # Insert a record into Person table
    repo.insert('person_table', {'name': 'John Doe', 'age': 30})

    # Fetch a record by ID and return as a Person object
    person = repo.fetch_by_id('person_table', 1, Person)
    print(person)  # Output: Person(id=1, name='John Doe', age=30)

    # Create a table for Product
    repo.create_table('product_table', {'id': 'SERIAL PRIMARY KEY', 'name': 'VARCHAR(100)', 'price': 'FLOAT'})

    # Insert a record into Product table
    repo.insert('product_table', {'name': 'Laptop', 'price': 999.99})

    # Fetch a record by ID and return as a Product object
    product = repo.fetch_by_id('product_table', 1, Product)
    print(product)  # Output: Product(id=1, name='Laptop', price=999.99)
"""