import requests
import sqlite3
import json
CEPC = input("Por favor, insira o CEP:")

print("Carregando as informações do CEP desejado.")
if len(CEPC) != 8:
    print('esse CEP não é valido')
    exit()


Requisicao = requests.get(f"https://viacep.com.br/ws/{CEPC}/json")

if Requisicao.status_code == 200:
    from datetime import datetime
    time = datetime.now().strftime("%B %d, %Y %I:%M%p")

    data = Requisicao.json()
    # Database
    con = sqlite3.connect("CEPS.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Requisicao")
    cur.execute("CREATE TABLE Requisicao (cep, logradouro, complemento, bairro, localidade, uf, ibge, gia, ddd, siafi, created´ )")
    cur.execute("insert into Requisicao values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['cep'], data['logradouro'], data['complemento'], data['bairro'], data['localidade'], data['uf'], data['ibge'], data['gia'], data['ddd'], data['siafi'], time))
    addColumn = "ALTER TABLE Requisicao ADD COLUMN Validation"
    cur.execute(addColumn)
    con.commit()
    cur.execute("SELECT * FROM Requisicao");
    rows = cur.fetchall()
    print(rows)
    con.close()
else:
    print(f"Request failed with status code {Requisicao.status_code} ")