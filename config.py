SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='123sql45678*',
        servidor='localhost',
        database='passaroteca'
    )