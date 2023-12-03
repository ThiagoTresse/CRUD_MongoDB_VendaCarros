from model.veiculos import Veiculo
from conexion.mongo_queries import MongoQueries
import pandas as pd

class Controller_Veiculo:
    def __init__(self):
        self.mongo = MongoQueries()
        pass
        
    def inserir_veiculo(self) -> Veiculo:
        # Solicita ao usuario o novo id do veiculo 
        idCarro = input("idCarro (Novo): ")
        self.mongo.connect()

        if self.verifica_existencia_veiculo(idCarro):
            # Solicita ao usuario o novo modelo do veiculo
            modelo = input("modelo (Novo): ")
            # Solicita ao usuario a cor do veiculo
            cor = input("cor (Novo): ")
            # Solicita ao usuario o ano do veiculo
            anoCarro = input("ano (Novo): ")
            # Solicita ao usuario o chassi do veiculo
            chassiCarro = input("chassi (Novo): ")
            # Solicita ao usuario o tipo de cambio do veiculo
            tipoCambio = input("tipo de cambio (Novo): ")
            # Solicita ao usuario o fabricante do veiculo
            fabricante = input("fabricante do carro (Novo): ")
            # Insere e persiste o novo veiculo
            self.mongo.db["Veiculo"].insert_one({"idcarro": idCarro, "modelo": modelo, "cor": cor, "anocarro": anoCarro, 
                                                 "chassicarro": chassiCarro, "tipocambio": tipoCambio, "fabricante": fabricante})
            # Recupera os dados do novo veiculo criado transformando em um DataFrame
            df_veiculo = self.recupera_veiculo(idCarro)
            # Cria um novo objeto Veiculo
            novo_Veiculo = Veiculo(df_veiculo.idcarro.values[0], df_veiculo.modelo.values[0], df_veiculo.cor.values[0],
                            df_veiculo.anocarro.values[0], df_veiculo.chassicarro.values[0], df_veiculo.tipocambio.values[0], df_veiculo.fabricante.values[0])
            # Exibe os atributos do novo veiculo
            print(novo_Veiculo.to_string())
            self.mongo.close()
            # Retorna o objeto novo_veiculo para utilização posterior, caso necessário
            return novo_Veiculo
        else:
            self.mongo.close()
            print(f"O veiculo {idCarro} já está cadastrado.")
            return None

    def atualizar_veiculo(self) -> Veiculo:
        # Solicita ao usuário o código do veiculo a ser alterado
        idCarro = int(input("Código do Veiculo que irá alterar: "))
        self.mongo.connect()        

        # Verifica se o veiculo existe na base de dados
        if not self.verifica_existencia_veiculo(idCarro):
            # Solicita o novo modelo do veiculo
            novo_modelo = input("modelo (Novo): ")
            # Solicita ao usuario a nova cor do veiculo
            nova_cor = input("cor (Novo): ")
            # Solicita ao usuario o novo ano do veiculo
            novo_ano = input("ano (Novo): ")
            # Solicita ao usuario o novo chassi do veiculo
            novo_chassiCarro = input("chassi (Novo): ")
            # Solicita o novo cambio do veiculo
            novo_tipoCambio = input("cambio (Novo): ")
            # Solicita o novo fabricante do veiculo
            novo_fabricante = input("fabricante (Novo): ")
            # Atualiza os novos dados do veiculo existente
            self.mongo.db["Veiculo"].update_one({"idcarro":f"{idCarro}"}, {"$set": {"modelo": novo_modelo, "cor": nova_cor, "ano": novo_ano,
                                                                                    "chassicarro": novo_chassiCarro, "tipocambio": novo_tipoCambio, "fabricante": novo_fabricante}})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_veiculo = self.recupera_veiculo(idCarro)
            # Cria um novo objeto Veiculo
            veiculo_atualizado = Veiculo(df_veiculo.idcarro.values[0], df_veiculo.modelo.values[0], df_veiculo.cor.values[0], df_veiculo.anocarro.values[0], df_veiculo.chassicarro.values[0],
                                         df_veiculo.tipocambio.values[0], df_veiculo.fabricante.values[0] )
            # Exibe os atributos do novo veiculo
            print(veiculo_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto produto_atualizado para utilização posterior, caso necessário
            return veiculo_atualizado
        else:
            self.mongo.close()
            print(f"O id {idCarro} não está cadastrado.")
            return None

    def excluir_veiculo(self) -> Veiculo:
        # Solicita ao usuário o código do veiculo a ser alterado
        idCarro = int(input("id do veiculo que irá excluir: "))
        self.mongo.connect()        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_veiculo(idCarro):            
            # Recupera os dados do novo veiculo criado transformando em um DataFrame
            df_veiculo = self.recupera_veiculo(idCarro)
            # Remove o cliente da tabela
            self.mongo.db["Veiculo"].delete_one({"idcarro":f"{idCarro}"})            
            # Cria um novo objeto Veiculo para informar que foi removido
            veiculo_excluido = Veiculo(df_veiculo.idcarro.values[0], df_veiculo.modelo.values[0], df_veiculo.cor.values[0], df_veiculo.anocarro.values[0], df_veiculo.chassicarro.values[0],
                                         df_veiculo.tipocambio.values[0], df_veiculo.fabricante.values[0] )
            # Exibe os atributos do veiculo excluído
            print("Veiculo Removido com Sucesso!")
            print(veiculo_excluido.to_string())
            self.mongo.close()
        else:
            self.mongo.close()
            print(f"O id {idCarro} não existe na base de dados.")

    def verifica_existencia_veiculo(self, idCarro:int=None, external:bool=False) -> bool:
        if external:
            #cria uma conexao com o banco que permite alteração
            self.mongo.connect()

        #Recupera os dados do cliente e cria um novo DataFrame
        df_veiculo = pd.DataFrame(self.mongo.db["Veiculo"].find({"idcarro":f"{idCarro}"}, {"idCarro": 1, "modelo": 1, "cor": 1,
                       "anocarro":1, "chassicarro": 1, "tipocambio": 1 , "fabricante": 1,"_id": 0}))
        
        if external:
            #Fecha a conexão com o Mongo
            self.mongo.close()
      
        return df_veiculo.empty

    def recupera_veiculo(self, idCarro:int=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_veiculo = pd.DataFrame(list(self.mongo.db["Veiculo"].find({"idcarro":f"{idCarro}"}, {"idcarro": 1, "modelo": 1, "cor": 1,
                       "anocarro":1, "chassicarro": 1, "tipocambio": 1 , "fabricante": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_veiculo