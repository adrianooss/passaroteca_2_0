import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='123sql45678*'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `passaroteca`;")

cursor.execute("CREATE DATABASE `passaroteca`;")

cursor.execute("USE `passaroteca`;")

# criando tabelas
TABLES = {}
TABLES['Aves'] = ('''
      CREATE TABLE `aves` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome_popular` varchar(30) NOT NULL,
      `especie` varchar(30) NOT NULL,
      `familia` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `apelido` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`apelido`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, apelido, senha) VALUES (%s, %s, %s)'
usuarios = [
    ("Adriano Santos", "driko", "driko"),
    ("Cinara Cesário", "ci", "ci"),
    ("Christian Santos", "ze ruela", "zeruela")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from passaroteca.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo aves
aves_sql = 'INSERT INTO aves (nome_popular, especie, familia) VALUES (%s, %s, %s)'
aves = [
    ('Bem-te-Vi', 'Pitangus Sulphuratus', 'Atari'),
    ('Anu Branco', 'Guira guira', 'Cuculidae'),
    ('Tucano', 'Ramphastos toco', 'Ramphastidae')
]
cursor.executemany(aves_sql, aves)

cursor.execute('select * from passaroteca.aves')
print(' -------------  Aves:  -------------')
for ave in cursor.fetchall():
    print(ave[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
