from database.conexao import conectar

class Aviso:
    def __init__(self):
        pass
    def listar_ativos(self):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        query = """
            SELECT * FROM avisos 
            WHERE ativo = TRUE 
            ORDER BY fixado DESC, data_postagem DESC
            """
        cursor.execute(query)
        avisos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return avisos
    
    def criar(self, titulo, descricao, tipo, id_autor, data_expiracao=None):
        try:
            conexao = conectar()
            cursor = conexao.cursor()
        
            query = """
                INSERT INTO avisos (titulo, descricao, tipo, id_autor, data_expiracao) 
                VALUES (%s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (titulo, descricao, tipo, id_autor, data_expiracao))
        
            conexao.commit()  
            cursor.close()
            conexao.close()
        
            return True
        except Exception as e:
            print(f"Erro ao criar aviso: {e}")
            return False
        
    def buscar_por_id(self, id_aviso):
    
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
    
        query = "SELECT * FROM avisos WHERE id = %s"
        cursor.execute(query, (id_aviso,))
        aviso = cursor.fetchone() 
    
        cursor.close()
        conexao.close()
    
        return aviso
    
    def editar(self, id_aviso, titulo, descricao, tipo, data_expiracao):
        try:
            conexao = conectar()
            cursor = conexao.cursor()
        
            query = """
                UPDATE avisos 
                SET titulo = %s, descricao = %s, tipo = %s, data_expiracao = %s 
                WHERE id = %s
                """ 
            cursor.execute(query, (titulo, descricao, tipo, data_expiracao, id_aviso))
        
            conexao.commit()
            cursor.close()
            conexao.close()
        
            return True
        except Exception as e:
            print(f"Erro ao editar aviso: {e}")
            return False
    def deletar(self, id_aviso):
    
        try:
            conexao = conectar()
            cursor = conexao.cursor()
        
            query = "UPDATE avisos SET ativo = FALSE WHERE id = %s"
            cursor.execute(query, (id_aviso,))
        
            conexao.commit()
            cursor.close()
            conexao.close()
        
            return True
        except Exception as e:
            print(f"Erro ao deletar aviso: {e}")
            return False
        
    def fixar(self, id_aviso):
    
        try:
            conexao = conectar()
            cursor = conexao.cursor()
        
            query = "UPDATE avisos SET fixado = TRUE WHERE id = %s"
            cursor.execute(query, (id_aviso,))
        
            conexao.commit()
            cursor.close()
            conexao.close()
        
            return True
        except Exception as e:
            print(f"Erro ao fixar aviso: {e}")
            return False

    def desfixar(self, id_aviso):
   
        try:
            conexao = conectar()
            cursor = conexao.cursor()
        
            query = "UPDATE avisos SET fixado = FALSE WHERE id = %s"
            cursor.execute(query, (id_aviso,))
        
            conexao.commit()
            cursor.close()
            conexao.close()
        
            return True
        except Exception as e:
            print(f"Erro ao desfixar aviso: {e}")
            return False
        
    def listar_todos(self):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        query = """
            SELECT * FROM avisos 
            ORDER BY fixado DESC, data_postagem DESC
            """
        cursor.execute(query)
        avisos = cursor.fetchall()
        cursor.close()
        conexao.close()
        return avisos