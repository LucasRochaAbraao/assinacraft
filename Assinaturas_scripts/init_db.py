import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO assinaturas (nome, setor, telefone, email) VALUES (?, ?, ?, ?)",
            ('Lucas Rocha Abraão', 'CGR', '24 99301-2301', 'lucas.abraao@gmail.com')
            )

cur.execute("INSERT INTO assinaturas (nome, setor, telefone, email) VALUES (?, ?, ?, ?)",
            ('Pietra Cursino', 'MARKETING', '24 99301-2301', 'pietra.cursino@gmail.com')
            )

connection.commit()
connection.close()

# initial login
connection_login = sqlite3.connect('database_login.db')

with open('login_schema.sql') as f:
    connection_login.executescript(f.read())

cur_login = connection_login.cursor()

cur_login.execute("INSERT INTO login (email, password) VALUES (?, ?)",
            ('lucas.abraao@gmail.com', '123mudar')
            )

connection_login.commit()
connection_login.close()