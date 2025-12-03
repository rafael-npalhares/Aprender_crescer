from database.conexao import conectar

class Aluno: 
    def __init__(self):
        pass
    def listar_todos(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM alunos ORDER BY nome"
            cursor.execute(query)
            alunos = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return alunos
            
        except Exception as e:
            print(f"Erro ao listar alunos: {e}")
            return []
    
    def buscar_por_id(self, id_aluno):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM alunos WHERE id = %s"
            cursor.execute(query, (id_aluno,))
            aluno = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return aluno
        
        except Exception as e:
            print(f"Erro ao buscar aluno: {e}")
            return None
    
    def buscar_por_email(self, email):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM alunos WHERE email = %s"          
            cursor.execute(query, (email,))
            aluno = cursor.fetchone()           
            cursor.close()
            conexao.close()            
            
            return aluno
            
        except Exception as e:
            print(f"Erro ao buscar aluno por email: {e}")
            return None
    
    def buscar_turma(self, id_aluno):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)  
            
            query = """
                SELECT 
                    t.id,
                    t.nome,
                    t.ativa
                FROM turmas t
                INNER JOIN aluno_turma at ON t.id = at.id_turma
                WHERE at.id_aluno = %s AND t.ativa = TRUE
            """
            cursor.execute(query, (id_aluno,))
            turma = cursor.fetchone()
            cursor.close()
            conexao.close() 
            
            return turma
            
        except Exception as e:
            print(f"Erro ao buscar turma do aluno: {e}")
            return None
    
    def buscar_horarios(self, id_aluno):

        try:
 
            turma = self.buscar_turma(id_aluno)
            
            if not turma:
                return []
            
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    h.id,
                    h.dia_semana,
                    h.horario_inicio,
                    h.horario_fim,
                    p.nome as professor_nome,
                    d.nome as disciplina_nome,
                    s.nome as sala_nome
                FROM horarios h
                INNER JOIN professores p ON h.id_professor = p.id
                INNER JOIN disciplinas d ON h.id_disciplina = d.id
                LEFT JOIN salas s ON h.id_sala = s.id
                WHERE h.id_turma = %s
                ORDER BY 
                    FIELD(h.dia_semana, 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'),
                    h.horario_inicio
            """
            
            cursor.execute(query, (turma['id'],))
            horarios = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return horarios
            
        except Exception as e:
            print(f"Erro ao buscar horários do aluno: {e}")
            return []
    
    def listar_por_turma(self, id_turma):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    a.id,
                    a.nome,
                    a.email
                FROM alunos a
                INNER JOIN aluno_turma at ON a.id = at.id_aluno
                WHERE at.id_turma = %s
                ORDER BY a.nome
            """
            cursor.execute(query, (id_turma,))
            alunos = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return alunos
            
        except Exception as e:
            print(f"Erro ao listar alunos da turma: {e}")
            return []
    
    def contar_alunos_turma(self, id_turma):
    
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT COUNT(*) as total
                FROM aluno_turma
                WHERE id_turma = %s
            """
            cursor.execute(query, (id_turma,))
            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return resultado['total'] if resultado else 0
        
        except Exception as e:
            print(f"Erro ao contar alunos da turma: {e}")
            return 0

    def criar(self, nome, email, senha):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query_verifica = "SELECT id FROM alunos WHERE email = %s"
            cursor.execute(query_verifica, (email,))
            
            if cursor.fetchone():
                cursor.close()
                conexao.close()
                return False 

            query = """
                INSERT INTO alunos (nome, email, senha) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nome, email, senha))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar aluno: {e}")
            return False
    
    def atualizar_perfil(self, id_aluno, nome, email):
    
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                UPDATE alunos 
                SET nome = %s, email = %s 
                WHERE id = %s
            """
            cursor.execute(query, (nome, email, id_aluno))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True 
            
        except Exception as e:
            print(f"Erro ao atualizar perfil do aluno: {e}")
            return False
    
    def atualizar_senha(self, id_aluno, senha_atual, nova_senha):
     
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query_verifica = "SELECT senha FROM alunos WHERE id = %s"
            cursor.execute(query_verifica, (id_aluno,))
            aluno = cursor.fetchone()
            
            if not aluno or aluno['senha'] != senha_atual:
                cursor.close()
                conexao.close()
                return False  
            
            query_update = "UPDATE alunos SET senha = %s WHERE id = %s"
            cursor.execute(query_update, (nova_senha, id_aluno))
            conexao.commit()
            
            cursor.close()
            conexao.close()
            
            return True
        
        except Exception as e:
            print(f"Erro ao atualizar senha do aluno: {e}")
            return False
    
    def vincular_turma(self, id_aluno, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            

            query_verifica = """
                SELECT id FROM aluno_turma 
                WHERE id_aluno = %s AND id_turma = %s
            """
            cursor.execute(query_verifica, (id_aluno, id_turma))
            
            if cursor.fetchone():
                cursor.close()
                conexao.close()
                return True 
            

            query_insert = """
                INSERT INTO aluno_turma (id_aluno, id_turma)
                VALUES (%s, %s)
            """
            cursor.execute(query_insert, (id_aluno, id_turma))
            conexao.commit()
            
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao vincular aluno à turma: {e}")
            return False 
    
    def desvincular_turma(self, id_aluno, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                DELETE FROM aluno_turma 
                WHERE id_aluno = %s AND id_turma = %s
            """
            cursor.execute(query, (id_aluno, id_turma))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao desvincular aluno da turma: {e}")
            return False
    
    def deletar(self, id_aluno):

        try:
            conexao = conectar()
            cursor = conexao.cursor()
            
            query_turmas = "DELETE FROM aluno_turma WHERE id_aluno = %s"
            cursor.execute(query_turmas, (id_aluno,))
            
            query_aluno = "DELETE FROM alunos WHERE id = %s"
            cursor.execute(query_aluno, (id_aluno,))
            
            conexao.commit()
            
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao deletar aluno: {e}")
            return False