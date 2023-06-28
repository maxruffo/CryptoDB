import sqlite3
import os
database_name='database.db'
database_path='resources/database'

connection = sqlite3.connect(os.path.join(database_path, database_name))

print(type(connection))