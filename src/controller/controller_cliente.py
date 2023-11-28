from model.clientes import Cliente
from conexion.mongo_queries import MongoQueries
import random
import pandas as pd

class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_cliente(self) -> Cliente:
        # Solicita ao usuario o novo CPF
        cpfCliente = input("Informe o CPF do cliente: ")
        self.mongo.connect()

        if self.verifica_existencia_cliente( cpfCliente):
            # Sistema gera um numero de ID para o cliente
            idCliente = random.randint(10000, 99999)
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Solicita ao usuario o email
            email = input("email (Novo): ")
            # Solicita ao usuario o telefone
            telefone = input("telefone (Novo): ")
            # Solicita ao usuario o endereco
            endereco = input("endereco (Novo): ")            
            # Insere e persiste o novo cliente
            self.mongo.db["Cliente"].insert_one({"cpfcliente": cpfCliente, "idcliente": idCliente, "nome": nome, "email": email, "telefone": telefone, "endereco": endereco})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpfCliente)
            # Cria um novo objeto Cliente
            novo_cliente = Cliente(df_cliente.cpfcliente.values[0], df_cliente.idcliente.values[0], df_cliente.nome.values[0], df_cliente.email.values[0],
                                    df_cliente.telefone.values[0], df_cliente.endereco.values[0])
            # Exibe os atributos do novo cliente
            print(novo_cliente.to_string())
            self.mongo.close()
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            self.mongo.close()
            print(f"O CPF {cpfCliente} já está cadastrado.")
            return None

    def atualizar_cliente(self) -> Cliente:
        # Solicita ao usuário o código do cliente a ser alterado
        cpfCliente = int(input("Insira o CPF do cliente que deseja alterar o nome: "))
        self.mongo.connect()
        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(cpfCliente):
            # Solicita a nova descrição do cliente
            novo_nome = input("Nome (Novo): ")
            # Solicita ao usuario o novo email do cliente
            novo_email = input("email (Novo): ")
            # Solicita ao usuario o novo telefone do cliente
            novo_telefone = input("telefone (Novo): ")
            # Solicita ao usuario o novo endereco do cliente
            novo_endereco = input("endereco (Novo): ")
            # Atualiza as informações do cliente no banco de dados
            self.mongo.db["Cliente"].update_one({"cpfcliente":f"{cpfCliente}"}, {"$set": {"nome": novo_nome, "email": novo_email,
                                                                                          "telefone": novo_telefone, "endereco": novo_endereco}})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpfCliente)
            # Cria um novo objeto cliente
            cliente_atualizado = Cliente(df_cliente.cpfcliente.values[0], df_cliente.idcliente.values[0], df_cliente.nome.values[0],
                            df_cliente.email.values[0], df_cliente.telefone.values[0], df_cliente.endereco.values[0])
            # Exibe os atributos do novo cliente
            print(cliente_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return cliente_atualizado
        else:
            print(f"O CPF {cpfCliente} não existe.")
            return None

    def excluir_cliente(self):
        # Solicita ao usuário o CPF do Cliente a ser excluido
        cpfCliente = int(input("Informe o CPF do Cliente que irá excluir: "))        
        self.mongo.connect()
        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(cpfCliente):            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpfCliente)
            # Remove o cliente da tabela
            self.mongo.db["Cliente"].delete_one({"cpfcliente":f"{cpfCliente}"})            
            # Cria um novo objeto Cliente para informar que foi removido
            cliente_excluido = Cliente(df_cliente.cpfcliente.values[0], df_cliente.idcliente.values[0], df_cliente.nome.values[0],
                            df_cliente.email.values[0], df_cliente.telefone.values[0], df_cliente.endereco.values[0])
            # Exibe os atributos do cliente excluído
            print("Cliente Removido com Sucesso!")
            print(cliente_excluido.to_string())
            self.mongo.close()
        else:
            print(f"O CPF {cpfCliente} não existe.")

    def verifica_existencia_cliente(self, cpfCliente:str=None, external:bool=False) -> bool:
        if external:
            #cria uma conexao com o banco que permite alteração
            self.mongo.connect()

        #Recupera os dados do cliente e cria um novo DataFrame
        df_cliente = pd.DataFrame(self.mongo.db["Cliente"].find({"cpfcliente":f"{cpfCliente}"}, {"cpfcliente": 1, "idcliente": 1, "nome": 1,
                       "email":1, "telefone": 1, "endereco": 1 ,"_id": 0}))
        
        if external:
            #Fecha a conexão com o Mongo
            self.mongo.close()
      
        return df_cliente.empty
           
    def recupera_cliente(self, cpfCliente:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(list(self.mongo.db["Cliente"].find({"cpfcliente":f"{cpfCliente}"}, {"cpfcliente": 1, "idcliente": 1, "nome": 1,
                       "email":1, "telefone": 1, "endereco": 1 ,"_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente