from pydoc import cli
from reports.relatorios import Relatorio
from model.clientes import Cliente
from controller.controller_cliente import Controller_Cliente
from model.veiculos import Veiculo
from controller.controller_veiculo import Controller_Veiculo
from model.Venda import VendaVeiculo
from conexion.mongo_queries import MongoQueries
from datetime import date
import pandas as pd
import random

class Controller_Venda:
    def __init__(self):
        self.ctrl_cliente = Controller_Cliente()
        self.ctrl_veiculo = Controller_Veiculo()
        self.relatorio = Relatorio()
        self.mongo = MongoQueries()

    def inserir_venda(self) -> VendaVeiculo:
        # Lista os clientes existentes para inserir no pedido
        self.mongo.connect()
        self.relatorio.get_relatorio_clientes()
        cpfCliente = str(input("Digite o número do CPF do Cliente para adicionar a Venda: "))
        Cliente = self.valida_cliente(cpfCliente)
        if Cliente == None:
            return None

        # Lista os Veiculos existentes para inserir no pedido
        self.relatorio.get_relatorio_veiculos()
        idCarro = int(input("Digite o número do id do Veiculo para adicionar a Venda: "))
        Veiculo = self.valida_veiculo(idCarro)
        if Veiculo == None:
            return None

        data_hoje = date.today()
        print("A data de hoje é: ", data_hoje)

        if self.verifica_prevenda(cpfCliente, idCarro):  # VERIFICAR PRÉ VENDA
            #Sistema gera a data da venda com a data de hoje
            dataVenda = input("Informe a data da venda: ")
            #Solicita ao usuario o valor da venda
            valorVenda = input("Informe o valor da venda: ")
            #Solicita ao usuario o id do vendedor
            idVendedor = input("Informe o id do vendedor: ")
            #Sistema gera um id de venda aleatorio
            idVenda = random.randint(1000,9999)
            print(f"O numero do ID da Venda é {idVenda}")
            # Grava os dados da nova Venda
            self.mongo.db["VendaVeiculo"].insert_one({"cpfcliente": cpfCliente, "idcarro": idCarro, "datavenda": dataVenda,
                                                      "valorvenda": valorVenda, "idvendedor": idVendedor, "idvenda": idVenda})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_venda = self.recupera_venda(idVenda)
            # Cria um novo objeto venda
            nova_venda = VendaVeiculo(df_venda.cpfcliente.values[0], df_venda.idcarro.values[0], df_venda.datavenda.values[0],
                                    df_venda.valorvenda.values[0], df_venda.idvendedor[0], df_venda.idvenda[0])
            # Exibe os atributos da nova venda
            print(nova_venda.to_string())
            self.mongo.close()
            # Retorna o objeto novo_pedido para utilização posterior, caso necessário
        return nova_venda

    def atualizar_venda(self) -> VendaVeiculo:
        #Lista as vendas para serem alteradas
        self.relatorio.get_relatorio_vendas
        # Solicita ao usuário o código da venda a ser alterado
        idVenda = int(input("Insira o código da Venda que irá alterar: "))        
        self.mongo.connect

        # Verifica se a venda existe na base de dados
        if not self.verifica_existencia_venda(idVenda):

            # Lista os clientes existentes para inserir na venda
            self.relatorio.get_relatorio_clientes
            novo_cpfCliente = str(input("Digite o novo número do CPF do Cliente: "))

            Cliente = self.valida_cliente(novo_cpfCliente)
            if Cliente == None:
                return None
          
            # Lista os veiculos existentes para inserir na venda
            self.relatorio.get_relatorio_veiculos
            novo_idCarro = str(input("Digite o novo codigo do Veiculo: "))
            Veiculo = self.valida_veiculo(novo_idCarro)
            if Veiculo == None:
                return None
            else:
                oracle.write(f"update VendaVeiculo set idCarro = {novo_idCarro} where cpfCliente = {idVenda}")

            #Solicita ao usuario o novo valor da venda
            novo_valorVenda = input("Informe o valor da venda: ")
            #Solicita ao usuario o novo id do vendedor
            novo_idVendedor = input("Informe o id do vendedor: ")
            # Atualiza a data da venda
            nova_dataVenda = input("informe a nova data da venda: ")
            data_hoje = date.today()
            print("Data de hoje: ", data_hoje)
            self.mongo.db["VendaVeiculo"].update_one({"idvenda":f"{idVenda}"}, {"$set": {"valorvenda": novo_valorVenda, "idvendedor": novo_idVendedor,
                                                                                          "datavenda": nova_dataVenda , "cpfcliente": novo_cpfCliente, "idcarro": novo_idCarro}})
            # Recupera os dados da nova venda criada transformando em um DataFrame
            df_venda = self.recupera_venda(idVenda)
            # Cria um novo objeto venda
            venda_atualizada = VendaVeiculo(df_venda.idVenda.values[0], df_venda.valorVenda.values[0], df_venda.dataVenda.values[0], df_venda.idVendedor.values[0],
                                             df_venda.cpfCliente[0], df_venda.idCarro[0])
            # Exibe os atributos da nova venda
            print(venda_atualizada.to_string())
            # Retorna o objeto venda_atualizado para utilização posterior, caso necessário
            return venda_atualizada
            self.mongo.close
        else:
            print(f"O id {idVenda} não existe.")
            return None
            self.mongo.close

    def excluir_venda(self):
        # Solicita ao usuário o código do produto a ser alterado
        idVenda = int(input("ID da venda que deseja excluir: "))        
        self.mongo.connect
        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_venda(idVenda):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_venda = self.recupera_venda(idVenda)
            opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {idVenda} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso a venda possua itens, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {idVenda} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o produto da tabela
                    self.mongo.db["VendaVeiculo"].delete_one({"idvenda":f"{idVenda}"})
                    print("Venda removida com sucesso!")
                    # Cria um novo objeto Venda para informar que foi removido
                    venda_excluida = VendaVeiculo(df_venda.idvenda.values[0], df_venda.valorvenda.values[0], df_venda.datavenda.values[0], 
                                                  df_venda.idvendedor.values[0], df_venda.cpfcliente[0], df_venda.idcarro[0])
                    # Exibe os atributos do produto excluído
                    print("Venda Removida com Sucesso!")
                    print(venda_excluida.to_string())
        else:
            print(f"O id {idVenda} não existe.")

    def verifica_prevenda(self, cpfCliente:str=None, idCarro:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_veiculo = (self.mongo.db["VendaVeiculo"].find({"$and":[
                                                                        {"cpfcliente":f"{cpfCliente}"},
                                                                        {"idcarro":f"{idCarro}"}
                                                                        ]
                                                                            }, {"idvenda": 1, "_id": 0}))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_veiculo
    
    def verifica_existencia_venda(self, cpfCliente:str=None, external:bool=False) -> bool:
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
        
    def valida_cliente(self, cpfCliente:str=None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(cpfCliente=cpfCliente, external=True):
            print(f"O CPF {cpfCliente} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.ctrl_cliente.recupera_cliente(cpfCliente=cpfCliente, external=True)
            # Cria um novo objeto cliente
            cliente = Cliente(df_cliente.cpfcliente.values[0], df_cliente.idcliente.values[0], df_cliente.nome.values[0],
                            df_cliente.email.values[0], df_cliente.telefone.values[0], df_cliente.endereco.values[0])
            return cliente

    def valida_veiculo(self, idCarro:str=None) -> Veiculo:
        if self.ctrl_veiculo.verifica_existencia_veiculo(idCarro=idCarro, external=True):
            print(f"O idCarro {idCarro} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_veiculo = self.ctrl_veiculo.recupera_veiculo(idCarro=idCarro, external=True)
            # Cria um novo objeto cliente
            veiculo = Veiculo(df_veiculo.idcarro.values[0], df_veiculo.modelo.values[0], df_veiculo.cor.values[0],
                            df_veiculo.anocarro.values[0], df_veiculo.chassicarro.values[0], df_veiculo.tipocambio.values[0], df_veiculo.fabricante.values[0])
            return veiculo
        
    def recupera_venda(self, idVenda:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_venda = pd.DataFrame(list(self.mongo.db["VendaVeiculo"].find({"idvenda":f"{idVenda}"}, {"cpfcliente": 1, "idvenda": 1,"idcarro": 1, "datavenda": 1,
                       "valorvenda":1, "idvendedor": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_venda