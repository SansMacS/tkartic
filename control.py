
import variaveis_globais
from requesicao import requestBD

class ControllerUsuario:


    def inserir_usuario(self, nome, senha):
        sql = (f"INSERT INTO Usuario (nome, senha) VALUES('{nome}', '{senha}');")
        return requestBD(sql)

    def listar_usuario(self, nome='', senha = ''):
        sql = f"SELECT * FROM Usuario WHERE nome LIKE '{nome}' AND senha LIKE '{senha}';"
        return requestBD(sql)

    def excluir_usuario(self, id):
        sql = f"DELETE FROM Usuario WHERE id={id};"
        return requestBD(sql)

    def editar_usuario(self, id, nome, senha):
        sql = f"UPDATE cliente SET nome='{nome}', senha='{senha}' WHERE id={id};"
        return requestBD(sql)

    def editar_sala(self):
        id = variaveis_globais.lista_global[0][0]
        sql = f"UPDATE Usuario SET sala_id = (SELECT MAX(id) FROM Sala) WHERE id = {id};"
        return requestBD(sql)
    
class ControllerSala:

    def inserir_sala(self):
        sql = (f"INSERT INTO Sala DEFAULT VALUES;")
        return requestBD(sql)

    def listar_sala(self, id=''):
        sql = f"SELECT * FROM Sala WHERE id LIKE '{id}';"
        return requestBD(sql)

    def excluir_sala(self, id):
        sql = f"DELETE FROM Sala WHERE id={id};"
        return requestBD(sql)


