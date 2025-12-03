from database.conexao import conectar

class Turma:
    def __init__(self):
        pass

    def listar_todas(self):
  
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, ativa FROM turmas ORDER BY nome"
            cursor.execute(query)
            turmas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return turmas
            
        except Exception as e:
            print(f"Erro ao listar turmas: {e}")
            return []
    
    def listar_ativas(self):
    
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome FROM turmas WHERE ativa = TRUE ORDER BY nome"
            cursor.execute(query)
            turmas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return turmas
            
        except Exception as e:
            print(f"Erro ao listar turmas ativas: {e}")
            return []
    
    def buscar_por_id(self, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, ativa FROM turmas WHERE id = %s"
            cursor.execute(query, (id_turma,))
            turma = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return turma
            
        except Exception as e:
            print(f"Erro ao buscar turma: {e}")
            return None
    
    def buscar_por_nome(self, nome):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, ativa FROM turmas WHERE nome = %s"
            cursor.execute(query, (nome,))
            turma = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return turma
            
        except Exception as e:
            print(f"Erro ao buscar turma por nome: {e}")
            return None
    
    def contar_total(self, apenas_ativas=False):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            if apenas_ativas:
                query = "SELECT COUNT(*) as total FROM turmas WHERE ativa = TRUE"
            else:
                query = "SELECT COUNT(*) as total FROM turmas"
            
            cursor.execute(query)
            resultado = cursor.fetchone() 
            cursor.close()
            conexao.close()
            
            return resultado['total'] if resultado else 0
            
        except Exception as e:
            print(f"Erro ao contar turmas: {e}")
            return 0
    
    def contar_alunos(self, id_turma):

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
    
    def listar_alunos(self, id_turma):

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
    
    def buscar_horarios(self, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    h.id,
                    h.dia_semana,
                    h.horario_inicio,
                    h.horario_fim,
                    d.nome as disciplina_nome,
                    p.nome as professor_nome,
                    s.nome as sala_nome
                FROM horarios h
                INNER JOIN disciplinas d ON h.id_disciplina = d.id
                INNER JOIN professores p ON h.id_professor = p.id
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
            print(f"Erro ao buscar horários da turma: {e}")
            return []
    
    def contar_horarios(self, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT COUNT(*) as total
                FROM horarios
                WHERE id_turma = %s
            """ 
            cursor.execute(query, (id_turma,))
            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return resultado['total'] if resultado else 0
            
        except Exception as e:
            print(f"Erro ao contar horários: {e}")
            return 0
    
    def buscar_com_estatisticas(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    t.id,
                    t.nome,
                    t.ativa,
                    COUNT(DISTINCT at.id_aluno) as total_alunos,
                    COUNT(DISTINCT h.id) as total_horarios
                FROM turmas t
                LEFT JOIN aluno_turma at ON t.id = at.id_turma
                LEFT JOIN horarios h ON t.id = h.id_turma
                GROUP BY t.id, t.nome, t.ativa
                ORDER BY t.nome
            """

            cursor.execute(query)
            turmas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return turmas
            
        except Exception as e:
            print(f"Erro ao buscar turmas com estatísticas: {e}")
            return []
    
    
    def verificar_em_uso(self, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT COUNT(*) as total FROM aluno_turma WHERE id_turma = %s",
                (id_turma,)
            )
            tem_alunos = cursor.fetchone()['total'] > 0
        
            cursor.execute(
                "SELECT COUNT(*) as total FROM horarios WHERE id_turma = %s",
                (id_turma,)
            )
            tem_horarios = cursor.fetchone()['total'] > 0
            
            cursor.close()
            conexao.close()
            
            return tem_alunos or tem_horarios
            
        except Exception as e:
            print(f"Erro ao verificar uso da turma: {e}")
            return True  

    def criar(self, nome):

        try:

            if not nome or not nome.strip():
                print("Erro: Nome da turma não pode estar vazio")
                return False
            
            nome = nome.strip()

            turma_existente = self.buscar_por_nome(nome)
            if turma_existente:
                print(f"Erro: Turma '{nome}' já existe")
                return False
            
            conexao = conectar()
            cursor = conexao.cursor()
            query = "INSERT INTO turmas (nome) VALUES (%s)"
            cursor.execute(query, (nome,))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar turma: {e}")
            return False
    
    
    def editar(self, id_turma, novo_nome):

        try:

            if not novo_nome or not novo_nome.strip():
                print("Erro: Nome da turma não pode estar vazio")
                return False
            
            novo_nome = novo_nome.strip()

            turma_existente = self.buscar_por_nome(novo_nome)
            if turma_existente and turma_existente['id'] != id_turma:
                print(f"Erro: Já existe outra turma chamada '{novo_nome}'")
                return False
            
            conexao = conectar()
            cursor = conexao.cursor()
            query = "UPDATE turmas SET nome = %s WHERE id = %s"
            cursor.execute(query, (novo_nome, id_turma))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao editar turma: {e}")
            return False
    
    
    def ativar(self, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor()
            query = "UPDATE turmas SET ativa = TRUE WHERE id = %s"
            cursor.execute(query, (id_turma,))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao ativar turma: {e}")
            return False
    
    
    def desativar(self, id_turma):

        try:
            conexao = conectar()
            cursor = conexao.cursor()
            query = "UPDATE turmas SET ativa = FALSE WHERE id = %s"
            cursor.execute(query, (id_turma,))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao desativar turma: {e}")
            return False

    def deletar(self, id_turma):

        try:

            if self.verificar_em_uso(id_turma):
                print("Erro: Não é possível deletar turma que está em uso!")
                print("Remova primeiro os alunos e horários.")
                return False

            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM aluno_turma WHERE id_turma = %s", (id_turma,))
            cursor.execute("DELETE FROM horarios WHERE id_turma = %s", (id_turma,))    
            cursor.execute("DELETE FROM turmas WHERE id = %s", (id_turma,))
            conexao.commit()
            cursor.close()
            conexao.close()

            return True
            
        except Exception as e:
            print(f"Erro ao deletar turma: {e}")
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
    
    def buscar_detalhes_completos(self, id_turma):
  
        try:
            turma = self.buscar_por_id(id_turma)
            
            if not turma:
                return None
            
            turma['alunos'] = self.listar_alunos(id_turma)
            turma['total_alunos'] = len(turma['alunos'])
            
            turma['horarios'] = self.buscar_horarios(id_turma)
            turma['total_horarios'] = len(turma['horarios'])
            
            turma['horarios_organizados'] = self.organizar_horarios_por_dia(turma['horarios'])
            
            return turma
            
        except Exception as e:
            print(f"Erro ao buscar detalhes completos da turma: {e}")
            return None