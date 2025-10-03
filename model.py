# from sqlite3 import Error
# import conexao

# class Model:
#     def __init__(self):
#         self.con = conexao.Conexao()

#     # def create_db(self):
#     #     sql =  """CREATE TABLE IF NOT EXISTS "cliente" (
# 	#            "id"	INTEGER,
# 	#            "nome"	VARCHAR NOT NULL,
# 	#            "cpf"	VARCHAR NOT NULL,
# 	#            "email"	VARCHAR,
# 	#            PRIMARY KEY("id" AUTOINCREMENT)
#     #            );"""
#     #     try:
#     #         con = self.con.get_conexao()
#     #         cursor = con.cursor()
#     #         cursor.execute(sql)
#     #         con.commit()
#     #         con.close()
#     #     except Error as er:
#     #         print(er)

#     # def get(self, sql):
#     #     try:
#     #         con = self.con.get_conexao()
#     #         cursor = con.cursor()
#     #         result = cursor.execute(sql).fetchall()
#     #         con.close()
#     #         return result
#     #     except Error as er:
#     #         print(er)

#     # def insert(self, sql):
#     #     try:
#     #         con = self.con.get_conexao()
#     #         cursor = con.cursor()
#     #         cursor.execute(sql)
#     #         if cursor.rowcount == 1: #Quantidade de linhas afetadas
#     #             con.commit()
#     #         con.close()
#     #         return cursor.rowcount
#     #     except Error as er:
#     #         print(er)

#     # def delete(self, sql):
#     #     try:
#     #         con = self.con.get_conexao()
#     #         cursor = con.cursor()
#     #         cursor.execute(sql)
#     #         if cursor.rowcount == 1:
#     #             con.commit()
#     #         con.close()
#     #         return cursor.rowcount
#     #     except Error as er:
#     #         print(er)

#     # def update(self, sql):
#     #     try:
#     #         con = self.con.get_conexao()
#     #         cursor = con.cursor()
#     #         cursor.execute(sql)
#     #         if cursor.rowcount == 1:
#     #             con.commit()
#     #         con.close()
#     #         return cursor.rowcount
#     #     except Error as er:
#     #         print(er)

#     def 