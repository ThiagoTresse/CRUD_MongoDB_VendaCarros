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
            mongo.db["Cliente"]
            .find({}, {"cpfcliente": 1, "idcliente": 1, "nome": 1,
                       "email":1, "telefone": 1, "endereco": 1 ,"_id": 0})
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
            mongo.db["Veiculo"]
            .find({}, {"idcarro": 1, "modelo": 1, "cor": 1, "anocarro":1 ,
                       "chassicarro": 1, "tipocambio": 1, "fabricante":1 ,
                       "_id": 0})
            .sort("idcarro", ASCENDING)
        )
        df_veiculo = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_veiculo)
        input("Pressione Enter para Sair do Relatório de Veiculos")

    def get_relatorio_vendas(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = (
            mongo.db["VendaVeiculo"]
            .find({}, {"idvenda": 1, "valorvenda": 1, "datavenda": 1, "idvendedor":1 ,
                       "cpfcliente": 1, "idcarro": 1 ,"_id": 0})
            .sort("idvenda", ASCENDING)
        )
        df_venda = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_venda)
        input("Pressione Enter para Sair do Relatório de Vendas")
