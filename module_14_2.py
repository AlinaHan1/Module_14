import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")
for i in range(10):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (f'user{i + 1}', f'example{i + 1}@gmail.com', f'{(i + 1) * 10}', 1000))
for i in range(1, 10, 2):
    cursor.execute('UPDATE Users SET balance = ? WHERE username = ?',
                   (500, f'user{i}'))
for i in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE username = ?',
                   (f'user{i}',))
cursor.execute('SELECT username, email, age, balance FROM Users WHERE AGE != ? ',
               (60,))
users = cursor.fetchall()
for user in users:
    print(f'{user[0]}|{user[1]}|{user[2]}|{user[3]}')

cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

cursor.execute('SELECT COUNT(*) FROM Users')
all_user = cursor.fetchone()[0]
print(all_user)

cursor.execute('SELECT SUM(balance) FROM Users')
all_sum = cursor.fetchone()[0]
print(all_sum)

print(all_sum/all_user)

connection.commit()
connection.close()