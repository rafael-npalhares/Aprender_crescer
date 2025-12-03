from database.conexao import conectar

class Usuario:
    def __init__(self):
        pass
    
    def login_aluno(self, email, senha):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        query = "SELECT * FROM alunos WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        aluno = cursor.fetchone()
        cursor.close()
        conexao.close()
        return aluno  

    def login_professor(self, email, senha):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        query = "SELECT * FROM professores WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        professor = cursor.fetchone()
        cursor.close()
        conexao.close()
        
        return professor

    def login_admin(self, email, senha):
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        query = "SELECT * FROM administradores WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        admin = cursor.fetchone()
        cursor.close()
        conexao.close()
        return admin
    
    def registrar_aluno(self, nome, email, senha):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            verificacao = "SELECT * FROM alunos WHERE email = %s"
            cursor.execute(verificacao, (email,))
            resultado = cursor.fetchone()
            if resultado:
                cursor.close()
                conexao.close()
                return False 
            
            query = "INSERT INTO alunos (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(query, (nome, email, senha))
            conexao.commit()
            
            cursor.close()
            conexao.close()
            return True
        
        except Exception as e:
            print(f"Erro ao registrar aluno: {e}")
            return False

    def registrar_professor(self, nome, email, especialidade, senha):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            verificacao = "SELECT * FROM professores WHERE email = %s"
            cursor.execute(verificacao, (email,))
            resultado = cursor.fetchone()
            
            if resultado:
                cursor.close()
                conexao.close()
                return False
            
            query = "INSERT INTO professores (nome, email, especialidade, senha) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nome, email, especialidade, senha))
            conexao.commit()
            
            cursor.close()
            conexao.close()
            return True
        
        except Exception as e:
            print(f"Erro ao registrar professor: {e}")
            return False
        
    def registrar_admin(self, nome, email, senha, senha_mestra):
        if senha_mestra != 'Admin_AP2008':
            return False 
        
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            verificacao = "SELECT * FROM administradores WHERE email = %s"
            cursor.execute(verificacao, (email,))
            resultado = cursor.fetchone()
            
            if resultado:
                cursor.close()
                conexao.close()
                return False
            
            query = "INSERT INTO administradores (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(query, (nome, email, senha))
            conexao.commit()
            
            cursor.close()
            conexao.close()
            return True
        
        except Exception as e:
            print(f"Erro ao registrar admin: {e}")
            return False