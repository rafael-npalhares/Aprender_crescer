from database.conexao import conectar

class Disciplina:
    def __init__(self):
        pass
    def listar_todas(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome FROM disciplinas ORDER BY nome"   
            cursor.execute(query)
            disciplinas = cursor.fetchall()   
            cursor.close()
            conexao.close()
            
            return disciplinas
            
        except Exception as e:
            print(f"Erro ao listar disciplinas: {e}")
            return []
    
    
    def buscar_por_id(self, id_disciplina):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = "SELECT id, nome FROM disciplinas WHERE id = %s"
            
            cursor.execute(query, (id_disciplina,))
            disciplina = cursor.fetchone()
            
            cursor.close()
            conexao.close()
            
            return disciplina
            
        except Exception as e:
            print(f"Erro ao buscar disciplina: {e}")
            return None
    
    
    def buscar_por_nome(self, nome):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = "SELECT id, nome FROM disciplinas WHERE nome = %s"
            
            cursor.execute(query, (nome,))
            disciplina = cursor.fetchone()
            
            cursor.close()
            conexao.close()
            
            return disciplina
            
        except Exception as e:
            print(f"Erro ao buscar disciplina por nome: {e}")
            return None
    
    
    def contar_total(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = "SELECT COUNT(*) as total FROM disciplinas"
            
            cursor.execute(query)
            resultado = cursor.fetchone()
            
            cursor.close()
            conexao.close()
            
            return resultado['total'] if resultado else 0
            
        except Exception as e:
            print(f"Erro ao contar disciplinas: {e}")
            return 0
    
    
    def buscar_professores(self, id_disciplina):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    p.id,
                    p.nome,
                    p.email,
                    p.especialidade
                FROM professores p
                INNER JOIN professor_disciplina pd ON p.id = pd.id_professor
                WHERE pd.id_disciplina = %s
                ORDER BY p.nome
            """
            
            cursor.execute(query, (id_disciplina,))
            professores = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return professores
            
        except Exception as e:
            print(f"Erro ao buscar professores da disciplina: {e}")
            return []
    
    
    def buscar_horarios(self, id_disciplina):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    h.id,
                    h.dia_semana,
                    h.horario_inicio,
                    h.horario_fim,
                    t.nome as turma_nome,
                    p.nome as professor_nome,
                    s.nome as sala_nome
                FROM horarios h
                INNER JOIN turmas t ON h.id_turma = t.id
                INNER JOIN professores p ON h.id_professor = p.id
                LEFT JOIN salas s ON h.id_sala = s.id
                WHERE h.id_disciplina = %s
                ORDER BY 
                    FIELD(h.dia_semana, 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'),
                    h.horario_inicio
            """
            
            cursor.execute(query, (id_disciplina,))
            horarios = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return horarios
            
        except Exception as e:
            print(f"Erro ao buscar horários da disciplina: {e}")
            return []
    
    
    def contar_horarios(self, id_disciplina):
 
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT COUNT(*) as total
                FROM horarios
                WHERE id_disciplina = %s
            """
            
            cursor.execute(query, (id_disciplina,))
            resultado = cursor.fetchone()
            
            cursor.close()
            conexao.close()
            
            return resultado['total'] if resultado else 0
            
        except Exception as e:
            print(f"Erro ao contar horários: {e}")
            return 0
    
    
    def verificar_em_uso(self, id_disciplina):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
 
            cursor.execute(
                "SELECT COUNT(*) as total FROM horarios WHERE id_disciplina = %s",
                (id_disciplina,)
            )
            tem_horarios = cursor.fetchone()['total'] > 0

            cursor.execute(
                "SELECT COUNT(*) as total FROM professor_disciplina WHERE id_disciplina = %s",
                (id_disciplina,)
            )
            tem_professores = cursor.fetchone()['total'] > 0
            
            cursor.close()
            conexao.close()
            
            return tem_horarios or tem_professores
            
        except Exception as e:
            print(f"Erro ao verificar uso da disciplina: {e}")
            return True 
    

    
    def criar(self, nome):

        try:
            
            if not nome or not nome.strip():
                print("Erro: Nome da disciplina não pode estar vazio")
                return False
            
         
            nome = nome.strip()
            

            disciplina_existente = self.buscar_por_nome(nome)
            if disciplina_existente:
                print(f"Erro: Disciplina '{nome}' já existe")
                return False
    
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = "INSERT INTO disciplinas (nome) VALUES (%s)"
            
            cursor.execute(query, (nome,))
            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar disciplina: {e}")
            return False
    
    def editar(self, id_disciplina, novo_nome):

        try:

            if not novo_nome or not novo_nome.strip():
                print("Erro: Nome da disciplina não pode estar vazio")
                return False
            

            novo_nome = novo_nome.strip()

            disciplina_existente = self.buscar_por_nome(novo_nome)
            if disciplina_existente and disciplina_existente['id'] != id_disciplina:
                print(f"Erro: Já existe outra disciplina chamada '{novo_nome}'")
                return False
            

            conexao = conectar()
            cursor = conexao.cursor()
            
            query = "UPDATE disciplinas SET nome = %s WHERE id = %s"
            
            cursor.execute(query, (novo_nome, id_disciplina))
            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao editar disciplina: {e}")
            return False
    
    def deletar(self, id_disciplina):

        try:
    
            if self.verificar_em_uso(id_disciplina):
                print("Erro: Não é possível deletar disciplina que está em uso!")
                print("Remova primeiro dos horários e desvincule dos professores.")
                return False

            conexao = conectar()
            cursor = conexao.cursor()
            
            query = "DELETE FROM disciplinas WHERE id = %s"
            
            cursor.execute(query, (id_disciplina,))
            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao deletar disciplina: {e}")
            return False
    
   
    
    def buscar_com_estatisticas(self):
    
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    d.id,
                    d.nome,
                    COUNT(DISTINCT pd.id_professor) as total_professores,
                    COUNT(DISTINCT h.id) as total_horarios
                FROM disciplinas d
                LEFT JOIN professor_disciplina pd ON d.id = pd.id_disciplina
                LEFT JOIN horarios h ON d.id = h.id_disciplina
                GROUP BY d.id, d.nome
                ORDER BY d.nome
            """
            
            cursor.execute(query)
            disciplinas = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return disciplinas
            
        except Exception as e:
            print(f"Erro ao buscar disciplinas com estatísticas: {e}")
            return []