import model

class ControllerUsuario:
    def __init__(self):
        self.model = model.Model()

    def criar_tabelas(self):
        self.model.create_db()

    def inserir_usuario(self, nome, senha):
        sql = (f"INSERT INTO Usuario (nome, senha) VALUES('{nome}', '{senha}');")
        return self.model.insert(sql)

    def listar_usuario(self, nome='', senha = ''):
        sql = f"SELECT * FROM Usuario WHERE nome LIKE '{nome}' AND senha LIKE '{senha}';"
        return self.model.get(sql)

    def excluir_usuario(self, id):
        sql = f"DELETE FROM Usuario WHERE id={id};"
        return self.model.delete(sql)

    def editar_usuario(self, id, nome, senha):
        sql = f"UPDATE cliente SET nome='{nome}', senha='{senha}' WHERE id={id};"
        return self.model.update(sql)
    
class ControllerSala:
    def __init__(self):
        self.model = model.Model()

    def inserir_sala(self):
        sql = (f"INSERT INTO Sala DEFAULT VALUES;")
        return self.model.insert(sql)
    
    def listar_sala(self, id=''):
        sql = f"SELECT * FROM Sala WHERE id LIKE '{id}';"
        return self.model.get(sql)
    
    def excluir_sala(self, id):
        sql = f"DELETE FROM Sala WHERE id={id};"
        return self.model.delete(sql)
    

