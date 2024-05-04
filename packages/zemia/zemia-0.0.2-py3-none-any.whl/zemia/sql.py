'''
Used to access .db files via SQLite3.
Taken from my ChessMate code.
'''
from sqlite3 import Connection
from sqlite3 import connect as conn
from sqlite3 import OperationalError, IntegrityError
from file_edit import delete

class TableClass:
    '''
    Initialises a table, which is an object that is used to interface with a specific table within the sql database.
    '''
    def __init__(self, connection: Connection, table_name: str, columns: list[str]) -> None:
        self._connection = connection
        self._cursor = self._connection.cursor()
        self._table_name = table_name

        create_string = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        create_string += ", ".join(columns)
        create_string += ")"
        self._connection.cursor().execute(create_string)
        self._connection.commit()

    def list_record(self, conditions: str = "", columns: str = "*") -> list[list]:
        '''
        Lists all recs where the condition is true.
        '''
        rec_bank = []
        for row in self._cursor.execute(f"""SELECT {columns} FROM {self._table_name} {conditions}"""):
            rec_bank.append(row)
        return rec_bank

    def update_record(self, key: str, value, conditions: str = "") -> bool:
        '''
        Attempts to update a record. Returns True if an error occurred, and False otherwise.
        '''
        try:
            self._cursor.execute(f"""UPDATE {self._table_name} SET {key} = {value} {conditions}""")
            self._connection.commit()
        except OperationalError:
            return True
        return False

    def add_record(self, data: str) -> None:
        '''
        Adds a new row to the table.
        '''
        # Create the execute string
        execute_string = f"INSERT INTO {self._table_name} VALUES("
        for _ in range(len(data[0])):
            execute_string += "?, "
        execute_string = execute_string[:-2] + ")"
        # Add the record
        try:
            self._cursor.executemany(execute_string, data)
            self._connection.commit()  # Remember to commit the transaction after executing INSERT.
        except IntegrityError as e:
            print("add_record error:", e)

def connect(database_name: str) -> Connection:
    '''
    Returns the database connection, which needs to be passed into most other functions from this file.
    '''
    connection = ""
    while connection == "":
        try:
            connection = conn(database_name)
        except OperationalError:
            pass
    return connection

def close(connection: Connection) -> None:
    '''
    Commits any unsaved changes and closes the connection to the database.
    '''
    connection.commit()
    connection.close()

if __name__ == "__main__":
    TEST_FILE = "test.db"

    test_connection = connect(TEST_FILE)
    test_table = TableClass(test_connection, "test_table", ["title TEXT NOT NULL", "year INTEGER NOT NULL", "score REAL NOT NULL", "PRIMARY KEY (title, year)"])
    test_table.add_record([("test1", "test2", "test3"), ("test4", "test5", "test6")])
    print(test_table.list_record())
    close(test_connection)
    input() # Allow user to view file before deleting it
    delete(TEST_FILE)
