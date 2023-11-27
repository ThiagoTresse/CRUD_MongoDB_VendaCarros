from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING


class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_clientes(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = (
            mongo.db["LABDATABASE.Cliente"]
            .find({}, {"cpfCliente": 1, "nome": 1, "_id": 0})
            .sort("nome", ASCENDING)
        )
        df_cliente = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_cliente)
        input("Pressione Enter para Sair do Relatório de Clientes")

    def get_relatorio_veiculos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = (
            mongo.db["LABDATABASE.Veiculo"]
            .find({}, {"codigo_produto": 1, "descricao_produto": 1, "_id": 0})
            .sort("descricao_produto", ASCENDING)
        )
        df_produto = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_produto)
        input("Pressione Enter para Sair do Relatório de Veiculos")

    def get_relatorio_vendas(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = (
            mongo.db["LABDATABASE.VendaVeiculo"]
            .find({}, {"cnpj": 1, "razao_social": 1, "nome_fantasia": 1, "_id": 0})
            .sort("nome_fantasia", ASCENDING)
        )
        df_fornecedor = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_fornecedor)
        input("Pressione Enter para Sair do Relatório de Fornecedores")
