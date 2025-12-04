from database.conexao import conectar

class Horario:
 
    def __init__(self):
        pass

    def listar_por_turma(self, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    h.id,
                    h.dia_semana,
                    h.horario_inicio,
                    h.horario_fim,
                    h.id_turma,
                    h.id_professor,
                    h.id_disciplina,
                    h.id_sala,
                    t.nome as turma_nome,
                    p.nome as professor_nome,
                    d.nome as disciplina_nome,
                    s.nome as sala_nome
                FROM horarios h
                INNER JOIN turmas t ON h.id_turma = t.id
                INNER JOIN professores p ON h.id_professor = p.id
                INNER JOIN disciplinas d ON h.id_disciplina = d.id
                LEFT JOIN salas s ON h.id_sala = s.id
                WHERE h.id_turma = %s
                ORDER BY 
                    FIELD(h.dia_semana, 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'),
                    h.horario_inicio
            """
            cursor.execute(query, (id_turma,))
            horarios = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return horarios
            
        except Exception as e:
            print(f"Erro ao listar horários da turma: {e}")
            return []
    
    def listar_por_professor(self, id_professor):

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
                    d.nome as disciplina_nome,
                    s.nome as sala_nome
                FROM horarios h
                INNER JOIN turmas t ON h.id_turma = t.id
                INNER JOIN disciplinas d ON h.id_disciplina = d.id
                LEFT JOIN salas s ON h.id_sala = s.id
                WHERE h.id_professor = %s
                ORDER BY 
                    FIELD(h.dia_semana, 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'),
                    h.horario_inicio
            """
            cursor.execute(query, (id_professor,))
            horarios = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return horarios
            
        except Exception as e:
            print(f"Erro ao listar horários do professor: {e}")
            return []
    
    def buscar_por_id(self, id_horario):
  
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    h.*,
                    t.nome as turma_nome,
                    p.nome as professor_nome,
                    d.nome as disciplina_nome,
                    s.nome as sala_nome
                FROM horarios h
                INNER JOIN turmas t ON h.id_turma = t.id
                INNER JOIN professores p ON h.id_professor = p.id
                INNER JOIN disciplinas d ON h.id_disciplina = d.id
                LEFT JOIN salas s ON h.id_sala = s.id
                WHERE h.id = %s
            """
            cursor.execute(query, (id_horario,))
            horario = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return horario
            
        except Exception as e:
            print(f"Erro ao buscar horário: {e}")
            return None
 
    
    def verificar_conflito_professor(self, id_professor, dia_semana, horario_inicio, horario_fim, id_horario_excluir=None):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id FROM horarios
                WHERE id_professor = %s
                AND dia_semana = %s
                AND (
                    (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio >= %s AND horario_fim <= %s)
                )
            """
            
            params = [
                id_professor, dia_semana,
                horario_fim, horario_inicio,
                horario_fim, horario_inicio,
                horario_inicio, horario_fim
            ]
            

            if id_horario_excluir:
                query += " AND id != %s"
                params.append(id_horario_excluir)
            
            cursor.execute(query, params)
            conflito = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return conflito is not None
            
        except Exception as e:
            print(f"Erro ao verificar conflito de professor: {e}")
            return True  # Em caso de erro, considera que há conflito
    
    def verificar_conflito_sala(self, id_sala, dia_semana, horario_inicio, horario_fim, id_horario_excluir=None):
      
        if not id_sala:
            return False 
        
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id FROM horarios
                WHERE id_sala = %s
                AND dia_semana = %s
                AND (
                    (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio >= %s AND horario_fim <= %s)
                )
            """
            
            params = [
                id_sala, dia_semana,
                horario_fim, horario_inicio,
                horario_fim, horario_inicio,
                horario_inicio, horario_fim
            ]
            
            if id_horario_excluir:
                query += " AND id != %s"
                params.append(id_horario_excluir)
            
            cursor.execute(query, params)
            conflito = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return conflito is not None
            
        except Exception as e:
            print(f"Erro ao verificar conflito de sala: {e}")
            return True
    
    def verificar_conflito_turma(self, id_turma, dia_semana, horario_inicio, horario_fim, id_horario_excluir=None):
       
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id FROM horarios
                WHERE id_turma = %s
                AND dia_semana = %s
                AND (
                    (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio >= %s AND horario_fim <= %s)
                )
            """
            
            params = [
                id_turma, dia_semana,
                horario_fim, horario_inicio,
                horario_fim, horario_inicio,
                horario_inicio, horario_fim
            ]
            
            if id_horario_excluir:
                query += " AND id != %s"
                params.append(id_horario_excluir)
            
            cursor.execute(query, params)
            conflito = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return conflito is not None
            
        except Exception as e:
            print(f"Erro ao verificar conflito de turma: {e}")
            return True

    def criar(self, id_turma, dia_semana, horario_inicio, horario_fim, id_professor, id_disciplina, id_sala=None):
        
        try:
  
            if self.verificar_conflito_professor(id_professor, dia_semana, horario_inicio, horario_fim):
                return False, "Professor já tem aula nesse horário"
            
            if self.verificar_conflito_sala(id_sala, dia_semana, horario_inicio, horario_fim):
                return False, "Sala já está ocupada nesse horário"
            
            if self.verificar_conflito_turma(id_turma, dia_semana, horario_inicio, horario_fim):
                return False, "Turma já tem aula nesse horário"
            
      
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                INSERT INTO horarios 
                (id_turma, dia_semana, horario_inicio, horario_fim, id_professor, id_disciplina, id_sala)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_turma, dia_semana, horario_inicio, horario_fim, id_professor, id_disciplina, id_sala))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True, "Horário criado com sucesso"
            
        except Exception as e:
            print(f"Erro ao criar horário: {e}")
            return False, "Erro ao criar horário"
    
    def editar(self, id_horario, id_turma, dia_semana, horario_inicio, horario_fim, id_professor, id_disciplina, id_sala=None):
    
        try:
    
            if self.verificar_conflito_professor(id_professor, dia_semana, horario_inicio, horario_fim, id_horario):
                return False, "Professor já tem aula nesse horário"
            
            if self.verificar_conflito_sala(id_sala, dia_semana, horario_inicio, horario_fim, id_horario):
                return False, "Sala já está ocupada nesse horário"
            
            if self.verificar_conflito_turma(id_turma, dia_semana, horario_inicio, horario_fim, id_horario):
                return False, "Turma já tem aula nesse horário"
            
          
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                UPDATE horarios 
                SET id_turma = %s, dia_semana = %s, horario_inicio = %s, horario_fim = %s, 
                    id_professor = %s, id_disciplina = %s, id_sala = %s
                WHERE id = %s
            """
            cursor.execute(query, (id_turma, dia_semana, horario_inicio, horario_fim, id_professor, id_disciplina, id_sala, id_horario))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True, "Horário editado com sucesso"
            
        except Exception as e:
            print(f"Erro ao editar horário: {e}")
            return False, "Erro ao editar horário"

    def deletar(self, id_horario):
        
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            query = "DELETE FROM horarios WHERE id = %s"
            cursor.execute(query, (id_horario,))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao deletar horário: {e}")
            return False