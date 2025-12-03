from database.conexao import conectar

class Sala:

    def __init__(self):
        pass
    
    def listar_todas(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo, capacidade, ativo 
                FROM salas 
                ORDER BY tipo, nome
            """
            
            cursor.execute(query)
            salas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return salas
            
        except Exception as e:
            print(f"Erro ao listar salas: {e}")
            return []
    
    def listar_ativas(self):
 
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo, capacidade 
                FROM salas 
                WHERE ativo = TRUE 
                ORDER BY tipo, nome
            """
            
            cursor.execute(query)
            salas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return salas
            
        except Exception as e:
            print(f"Erro ao listar salas ativas: {e}")
            return []
    
    def listar_por_tipo(self, tipo):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo, capacidade 
                FROM salas 
                WHERE tipo = %s AND ativo = TRUE 
                ORDER BY nome
            """
            
            cursor.execute(query, (tipo,))
            salas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return salas
            
        except Exception as e:
            print(f"Erro ao listar salas por tipo: {e}")
            return []
    
    def buscar_por_id(self, id_sala):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo, capacidade, ativo 
                FROM salas 
                WHERE id = %s
            """
            
            cursor.execute(query, (id_sala,))
            sala = cursor.fetchone()  
            cursor.close()
            conexao.close()
            
            return sala
            
        except Exception as e:
            print(f"Erro ao buscar sala: {e}")
            return None
     
    def buscar_por_nome(self, nome):
 
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo, capacidade, ativo 
                FROM salas 
                WHERE nome = %s
            """

            cursor.execute(query, (nome,))
            sala = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return sala
            
        except Exception as e:
            print(f"Erro ao buscar sala por nome: {e}")
            return None
    
    def contar_total(self, apenas_ativas=False):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            if apenas_ativas:
                query = "SELECT COUNT(*) as total FROM salas WHERE ativo = TRUE"
            else:
                query = "SELECT COUNT(*) as total FROM salas"
            
            cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return resultado['total'] if resultado else 0
            
        except Exception as e:
            print(f"Erro ao contar salas: {e}")
            return 0
    
    def contar_por_tipo(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT tipo, COUNT(*) as total 
                FROM salas 
                WHERE ativo = TRUE 
                GROUP BY tipo
            """

            cursor.execute(query)
            resultados = cursor.fetchall() 
            cursor.close()
            conexao.close()

            contagem = {
                'sala': 0,
                'laboratorio': 0,
                'auditorio': 0
            }
            
            for resultado in resultados:
                contagem[resultado['tipo']] = resultado['total']
            
            return contagem
            
        except Exception as e:
            print(f"Erro ao contar por tipo: {e}")
            return {'sala': 0, 'laboratorio': 0, 'auditorio': 0}
    
    def verificar_disponibilidade(self, id_sala, data, horario_inicio, horario_fim, id_reserva_atual=None):
   
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query_reservas = """
                SELECT id 
                FROM reservas 
                WHERE id_sala = %s 
                AND data = %s
                AND status IN ('pendente', 'aprovada')
                AND (
                    (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio >= %s AND horario_fim <= %s)
                )
            """
            
            parametros_reservas = [
                id_sala, data,
                horario_fim, horario_inicio,
                horario_fim, horario_inicio,
                horario_inicio, horario_fim
            ]

            if id_reserva_atual:
                query_reservas += " AND id != %s"
                parametros_reservas.append(id_reserva_atual)
            
            cursor.execute(query_reservas, tuple(parametros_reservas))
            conflitos_reservas = cursor.fetchall()
            cursor.execute("SELECT DAYNAME(%s) as dia_semana_en", (data,))
            dia_semana_resultado = cursor.fetchone()
            
            if dia_semana_resultado:
                dia_semana_en = dia_semana_resultado['dia_semana_en']
                
                mapa_dias = {
                    'Monday': 'segunda',
                    'Tuesday': 'terca',
                    'Wednesday': 'quarta',
                    'Thursday': 'quinta',
                    'Friday': 'sexta',
                    'Saturday': 'sabado',
                    'Sunday': 'domingo'
                }
                
                dia_semana_pt = mapa_dias.get(dia_semana_en)
                
                if dia_semana_pt:
                    query_horarios = """
                        SELECT id 
                        FROM horarios 
                        WHERE id_sala = %s 
                        AND dia_semana = %s
                        AND (
                            (horario_inicio < %s AND horario_fim > %s)
                            OR (horario_inicio < %s AND horario_fim > %s)
                            OR (horario_inicio >= %s AND horario_fim <= %s)
                        )
                    """
                    
                    cursor.execute(query_horarios, (
                        id_sala, dia_semana_pt,
                        horario_fim, horario_inicio,
                        horario_fim, horario_inicio,
                        horario_inicio, horario_fim
                    ))
                    conflitos_horarios = cursor.fetchall()
                else:
                    conflitos_horarios = []
            else:
                conflitos_horarios = []
            
            cursor.close()
            conexao.close()
            
            
            return len(conflitos_reservas) == 0 and len(conflitos_horarios) == 0
            
        except Exception as e:
            print(f"Erro ao verificar disponibilidade: {e}")
            return False
    
    def buscar_reservas(self, id_sala, limite=10):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    r.id,
                    r.data,
                    r.horario_inicio,
                    r.horario_fim,
                    r.finalidade,
                    r.status,
                    p.nome as professor_nome
                FROM reservas r
                INNER JOIN professores p ON r.id_professor = p.id
                WHERE r.id_sala = %s
                ORDER BY r.data DESC, r.horario_inicio DESC
                LIMIT %s
            """
            
            cursor.execute(query, (id_sala, limite))
            reservas = cursor.fetchall()       
            cursor.close()
            conexao.close()
            
            return reservas
            
        except Exception as e:
            print(f"Erro ao buscar reservas da sala: {e}")
            return []
      
    def buscar_horarios(self, id_sala):

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
                    p.nome as professor_nome
                FROM horarios h
                INNER JOIN turmas t ON h.id_turma = t.id
                INNER JOIN disciplinas d ON h.id_disciplina = d.id
                INNER JOIN professores p ON h.id_professor = p.id
                WHERE h.id_sala = %s
                ORDER BY 
                    FIELD(h.dia_semana, 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'),
                    h.horario_inicio
            """

            cursor.execute(query, (id_sala,))
            horarios = cursor.fetchall()           
            cursor.close()
            conexao.close()
            
            return horarios
            
        except Exception as e:
            print(f"Erro ao buscar horários da sala: {e}")
            return []
    
    def verificar_em_uso(self, id_sala):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT COUNT(*) as total FROM reservas WHERE id_sala = %s AND status IN ('pendente', 'aprovada')",
                (id_sala,)
            )
            tem_reservas = cursor.fetchone()['total'] > 0
            
            cursor.execute(
                "SELECT COUNT(*) as total FROM horarios WHERE id_sala = %s",
                (id_sala,)
            )
            tem_horarios = cursor.fetchone()['total'] > 0
            
            cursor.close()
            conexao.close()
            
            return tem_reservas or tem_horarios
            
        except Exception as e:
            print(f"Erro ao verificar uso da sala: {e}")
            return True 
    
    def criar(self, nome, tipo, capacidade):

        try:
          
            if not nome or not nome.strip():
                print("Erro: Nome da sala não pode estar vazio")
                return False
            
            if tipo not in ['sala', 'laboratorio', 'auditorio']:
                print("Erro: Tipo inválido! Use: sala, laboratorio ou auditorio")
                return False
            
            if not capacidade or capacidade <= 0:
                print("Erro: Capacidade deve ser maior que zero")
                return False
            
            nome = nome.strip()

            sala_existente = self.buscar_por_nome(nome)
            if sala_existente:
                print(f"Erro: Sala '{nome}' já existe")
                return False
    
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                INSERT INTO salas (nome, tipo, capacidade) 
                VALUES (%s, %s, %s)
            """

            cursor.execute(query, (nome, tipo, capacidade))         
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar sala: {e}")
            return False
 
    def editar(self, id_sala, nome, tipo, capacidade):

        try:

            if not nome or not nome.strip():
                print("Erro: Nome da sala não pode estar vazio")
                return False
            
            if tipo not in ['sala', 'laboratorio', 'auditorio']:
                print("Erro: Tipo inválido! Use: sala, laboratorio ou auditorio")
                return False
            
            if not capacidade or capacidade <= 0:
                print("Erro: Capacidade deve ser maior que zero")
                return False

            nome = nome.strip()
            sala_existente = self.buscar_por_nome(nome)
            if sala_existente and sala_existente['id'] != id_sala:
                print(f"Erro: Já existe outra sala chamada '{nome}'")
                return False

            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                UPDATE salas 
                SET nome = %s, tipo = %s, capacidade = %s 
                WHERE id = %s
            """

            cursor.execute(query, (nome, tipo, capacidade, id_sala))       
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao editar sala: {e}")
            return False
      
    def ativar(self, id_sala):

        try:
            conexao = conectar()
            cursor = conexao.cursor()          
            query = "UPDATE salas SET ativo = TRUE WHERE id = %s"          
            cursor.execute(query, (id_sala,))           
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao ativar sala: {e}")
            return False
    
    def desativar(self, id_sala):

        try:
            conexao = conectar()
            cursor = conexao.cursor()          
            query = "UPDATE salas SET ativo = FALSE WHERE id = %s"          
            cursor.execute(query, (id_sala,))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao desativar sala: {e}")
            return False

    def deletar(self, id_sala):

        try:

            if self.verificar_em_uso(id_sala):
                print("Erro: Não é possível deletar sala que está em uso!")
                print("Cancele as reservas e remova dos horários primeiro.")
                return False
            
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM reservas WHERE id_sala = %s AND status = 'cancelada'", (id_sala,))
            cursor.execute("UPDATE horarios SET id_sala = NULL WHERE id_sala = %s", (id_sala,))
            cursor.execute("DELETE FROM salas WHERE id = %s", (id_sala,))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao deletar sala: {e}")
            return False
   
    def buscar_com_estatisticas(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    s.id,
                    s.nome,
                    s.tipo,
                    s.capacidade,
                    s.ativo,
                    COUNT(DISTINCT r.id) as total_reservas,
                    COUNT(DISTINCT h.id) as total_horarios
                FROM salas s
                LEFT JOIN reservas r ON s.id = r.id_sala AND r.status IN ('pendente', 'aprovada')
                LEFT JOIN horarios h ON s.id = h.id_sala
                GROUP BY s.id, s.nome, s.tipo, s.capacidade, s.ativo
                ORDER BY s.tipo, s.nome
            """
            
            cursor.execute(query)
            salas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return salas
            
        except Exception as e:
            print(f"Erro ao buscar salas com estatísticas: {e}")
            return []