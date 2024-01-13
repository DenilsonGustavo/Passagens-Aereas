import requests
import pandas as pd
from pandas import json_normalize
from sqlalchemy import create_engine

url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/getPriceCalendar"

today = pd.to_datetime('today')
fromDate = today.strftime('%Y-%m-%d')
toDate = (today + pd.Timedelta(days=30 * 1)).strftime('%Y-%m-%d')

querystring = {"originSkyId": "GRU", "destinationSkyId": "NAT", "fromDate": fromDate, "toDate": toDate}

headers = {
    "X-RapidAPI-Key": "6b10ff12d6msha07329de0a6cabdp105ad5jsn3b24493987f7",
    "X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

if data['status']:
    # Normalizar a lista antes de criar o DataFrame
    flights_data = json_normalize(data['data']['flights']['days'])

    # Renomear as colunas do DataFrame
    flights_data.columns = ['Day', 'Group', 'Price']

    # Ajustar a forma como os dados são exibidos
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.precision', 2)

    # Mostrar os dados do DataFrame
    print(flights_data)

    # Create a connection to the MySQL database using SQLAlchemy
    engine = create_engine('mysql+pymysql://root:$12345678$@localhost/passagens_aereas')

    # Inserir os dados do DataFrame na tabela prices
    flights_data.to_sql('prices', con=engine, if_exists='append', index=False)

    # Ler os dados do MySQL e salvar em um arquivo Excel
    #query = "SELECT * FROM prices;"
    #df_from_mysql = pd.read_sql_query(query, con=engine)
    #df_from_mysql.to_excel('flights_data.xlsx', index=False)

    # Fechar a conexão
    engine.dispose()
else:
    print("No price information available.")
