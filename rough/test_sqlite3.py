import sqlite3

conn = sqlite3.connect('../FinSolve.db')
cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM roles"
)
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()