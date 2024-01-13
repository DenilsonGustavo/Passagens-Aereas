from sqlalchemy import create_engine, text

# Crie uma conexão com o banco de dados MySQL usando SQLAlchemy
engine = create_engine('mysql+pymysql://root:$12345678$@localhost/passagens_aereas')

# Criar um objeto de conexão
connection = engine.connect()

# Comando SQL para apagar todos os dados da tabela 'prices'
delete_query = "TRUNCATE TABLE prices;"

# Executar o comando SQL
connection.execute(text(delete_query))

# Fechar a conexão
connection.close()

print("Todos os dados foram removidos da tabela 'prices'.")
