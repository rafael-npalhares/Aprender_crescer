from database.conexao import conectar

class professor:
    def __init__(self):
       pass
    def listar_todos(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM professores ORDER BY nome"
            cursor.execute(query)
            professor = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return professor
            
        except Exception as e:
            print(f"Erro ao listar os professores: {e}")
            return []

        
    def buscar_por_id(self, id_aluno):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM professores WHERE id = %s"
            cursor.execute(query, (id_aluno,))
            professor = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return professor
        
        except Exception as e:
            print(f"Erro ao buscar professor: {e}")
            return None

    def buscar_por_email(self, email):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM professores WHERE email = %s"          
            cursor.execute(query, (email,))
            professor = cursor.fetchone()           
            cursor.close()
            conexao.close()            
            
            return professor
            
        except Exception as e:
            print(f"Erro ao buscar professor por email: {e}")
            return None       
            

    