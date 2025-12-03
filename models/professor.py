from database.conexao import conectar
class Professor:
    
    def __init__(self):
        pass
    
    def buscar_por_id(self, id_professor):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, email, especialidade 
                FROM professores 
                WHERE id = %s
            """
            
            cursor.execute(query, (id_professor,))
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
            
            query = """
                SELECT id, nome, email, especialidade 
                FROM professores 
                WHERE email = %s
            """
            
            cursor.execute(query, (email,))
            professor = cursor.fetchone()
            
            cursor.close()
            conexao.close()
            
            return professor
            
        except Exception as e:
            print(f"Erro ao buscar professor por email: {e}")
            return None
    
    
    def buscar_minhas_disciplinas(self, id_professor):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    d.id,
                    d.nome
                FROM disciplinas d
                INNER JOIN professor_disciplina pd ON d.id = pd.id_disciplina
                WHERE pd.id_professor = %s
                ORDER BY d.nome
            """
            
            cursor.execute(query, (id_professor,))
            disciplinas = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return disciplinas
            
        except Exception as e:
            print(f"Erro ao buscar disciplinas do professor: {e}")
            return []
    
    
    def buscar_meus_horarios(self, id_professor):
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
            print(f"Erro ao buscar horários do professor: {e}")
            return []
    
    
    def buscar_minhas_turmas(self, id_professor):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT DISTINCT
                    t.id,
                    t.nome
                FROM turmas t
                INNER JOIN horarios h ON t.id = h.id_turma
                WHERE h.id_professor = %s AND t.ativa = TRUE
                ORDER BY t.nome
            """
            
            cursor.execute(query, (id_professor,))
            turmas = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return turmas
            
        except Exception as e:
            print(f"Erro ao buscar turmas do professor: {e}")
            return []
    
    
    def buscar_minhas_reservas(self, id_professor):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    r.id,
                    r.tipo,
                    r.data,
                    r.horario_inicio,
                    r.horario_fim,
                    r.finalidade,
                    r.status,
                    s.nome as sala_nome,
                    e.nome as equipamento_nome
                FROM reservas r
                LEFT JOIN salas s ON r.id_sala = s.id
                LEFT JOIN equipamentos e ON r.id_equipamento = e.id
                WHERE r.id_professor = %s
                ORDER BY r.data DESC, r.horario_inicio DESC
            """
            
            cursor.execute(query, (id_professor,))
            reservas = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return reservas
            
        except Exception as e:
            print(f"Erro ao buscar reservas do professor: {e}")
            return []
    
    
    def atualizar_meu_perfil(self, id_professor, nome, email, especialidade):
        try:
            if not nome or not nome.strip():
                print("Erro: Nome não pode estar vazio")
                return False
            
            if not email or not email.strip():
                print("Erro: Email não pode estar vazio")
                return False
            
            if '@' not in email or '.' not in email:
                print("Erro: Email inválido")
                return False
            
            if not especialidade or not especialidade.strip():
                print("Erro: Especialidade não pode estar vazia")
                return False
            
            nome = nome.strip()
            email = email.strip()
            especialidade = especialidade.strip()
            
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                UPDATE professores 
                SET nome = %s, email = %s, especialidade = %s 
                WHERE id = %s
            """
            
            cursor.execute(query, (nome, email, especialidade, id_professor))
            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao atualizar perfil do professor: {e}")
            return False
    
    
    def atualizar_minha_senha(self, id_professor, nova_senha_hash):
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = "UPDATE professores SET senha = %s WHERE id = %s"
            
            cursor.execute(query, (nova_senha_hash, id_professor))
            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao atualizar senha do professor: {e}")
            return False
    
    
    def organizar_horarios_por_dia(self, horarios):
        horarios_organizados = {
            'segunda': [],
            'terca': [],
            'quarta': [],
            'quinta': [],
            'sexta': [],
            'sabado': []
        }
        
        for horario in horarios:
            dia = horario['dia_semana']
            if dia in horarios_organizados:
                horarios_organizados[dia].append(horario)
        
        return horarios_organizados
    
    
    def buscar_meus_detalhes_completos(self, id_professor):
        try:
            professor = self.buscar_por_id(id_professor)
            
            if not professor:
                return None
            
            professor['disciplinas'] = self.buscar_minhas_disciplinas(id_professor)
            professor['total_disciplinas'] = len(professor['disciplinas'])
            
            professor['horarios'] = self.buscar_meus_horarios(id_professor)
            professor['total_horarios'] = len(professor['horarios'])
            professor['horarios_organizados'] = self.organizar_horarios_por_dia(professor['horarios'])
            
            professor['turmas'] = self.buscar_minhas_turmas(id_professor)
            professor['total_turmas'] = len(professor['turmas'])
            
            professor['reservas'] = self.buscar_minhas_reservas(id_professor)
            professor['total_reservas'] = len(professor['reservas'])
            
            return professor
            
        except Exception as e:
            print(f"Erro ao buscar detalhes completos do professor: {e}")
            return None
    