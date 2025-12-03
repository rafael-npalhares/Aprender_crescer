from database.conexao import conectar

class Reserva:
    
    def __init__(self):
        pass
    
    def listar_todas(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    r.*,
                    p.nome as professor_nome,
                    s.nome as sala_nome,
                    e.nome as equipamento_nome
                FROM reservas r
                INNER JOIN professores p ON r.id_professor = p.id
                LEFT JOIN salas s ON r.id_sala = s.id
                LEFT JOIN equipamentos e ON r.id_equipamento = e.id
                ORDER BY r.data DESC, r.horario_inicio DESC
            """
            
            cursor.execute(query)
            reservas = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return reservas
            
        except Exception as e:
            print(f"Erro ao listar reservas: {e}")
            return []
    
    
    def listar_por_professor(self, id_professor):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    r.*,
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
            print(f"Erro ao listar reservas do professor: {e}")
            return []
    
    
    def listar_pendentes(self):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    r.*,
                    p.nome as professor_nome,
                    s.nome as sala_nome,
                    e.nome as equipamento_nome
                FROM reservas r
                INNER JOIN professores p ON r.id_professor = p.id
                LEFT JOIN salas s ON r.id_sala = s.id
                LEFT JOIN equipamentos e ON r.id_equipamento = e.id
                WHERE r.status = 'pendente'
                ORDER BY r.data_criacao DESC
            """
            
            cursor.execute(query)
            reservas = cursor.fetchall()
            
            cursor.close()
            conexao.close()
            
            return reservas
            
        except Exception as e:
            print(f"Erro ao listar reservas pendentes: {e}")
            return []
    
    
    def buscar_por_id(self, id_reserva):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    r.*,
                    p.nome as professor_nome,
                    p.email as professor_email,
                    s.nome as sala_nome,
                    s.tipo as sala_tipo,
                    e.nome as equipamento_nome,
                    e.tipo as equipamento_tipo
                FROM reservas r
                INNER JOIN professores p ON r.id_professor = p.id
                LEFT JOIN salas s ON r.id_sala = s.id
                LEFT JOIN equipamentos e ON r.id_equipamento = e.id
                WHERE r.id = %s
            """
            
            cursor.execute(query, (id_reserva,))
            reserva = cursor.fetchone()
            
            cursor.close()
            conexao.close()
            
            return reserva
            
        except Exception as e:
            print(f"Erro ao buscar reserva: {e}")
            return None
    
    
    def verificar_disponibilidade(self, tipo, data, horario_inicio, horario_fim, 
                                   id_sala=None, id_equipamento=None, id_reserva_atual=None):

        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id 
                FROM reservas 
                WHERE tipo = %s 
                AND data = %s
                AND status IN ('pendente', 'aprovada')
            """
            
            parametros = [tipo, data]
            

            if tipo == 'sala':
                query += " AND id_sala = %s"
                parametros.append(id_sala)
            else:
                query += " AND id_equipamento = %s"
                parametros.append(id_equipamento)
            
 
            if id_reserva_atual:
                query += " AND id != %s"
                parametros.append(id_reserva_atual)

            query += """
                AND (
                    (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio >= %s AND horario_fim <= %s)
                )
            """
            
            parametros.extend([
                horario_fim, horario_inicio,
                horario_fim, horario_inicio,
                horario_inicio, horario_fim
            ])

            cursor.execute(query, tuple(parametros))
            conflitos = cursor.fetchall()
            cursor.close()
            conexao.close()
      
            return len(conflitos) == 0
            
        except Exception as e:
            print(f"Erro ao verificar disponibilidade: {e}")
            return False
    
    
    def criar(self, tipo, id_professor, data, horario_inicio, horario_fim, 
              finalidade, id_sala=None, id_equipamento=None):
        try:
            if not all([tipo, id_professor, data, horario_inicio, horario_fim]):
                print("Erro: Dados obrigatórios faltando")
                return False
            
            if tipo == 'sala' and not id_sala:
                print("Erro: Reserva de sala precisa de id_sala")
                return False
            
            if tipo == 'equipamento' and not id_equipamento:
                print("Erro: Reserva de equipamento precisa de id_equipamento")
                return False
     
            if not self.verificar_disponibilidade(tipo, data, horario_inicio, horario_fim, 
                                                   id_sala, id_equipamento):
                print("Erro: Já existe reserva neste horário")
                return False

            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                INSERT INTO reservas 
                (tipo, id_professor, id_sala, id_equipamento, data, 
                 horario_inicio, horario_fim, finalidade, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pendente')
            """
            
            cursor.execute(query, (
                tipo, id_professor, id_sala, id_equipamento,
                data, horario_inicio, horario_fim, finalidade
            ))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar reserva: {e}")
            return False
    
    
    def aprovar(self, id_reserva):

        try:
            conexao = conectar()
            cursor = conexao.cursor()  
            query = "UPDATE reservas SET status = 'aprovada' WHERE id = %s"
            cursor.execute(query, (id_reserva,))
            conexao.commit()
            cursor.close()
            conexao.close()
         
            return True
            
        except Exception as e:
            print(f"Erro ao aprovar reserva: {e}")
            return False
    
    
    def reprovar(self, id_reserva):
     
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            query = "UPDATE reservas SET status = 'reprovada' WHERE id = %s"
            cursor.execute(query, (id_reserva,))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao reprovar reserva: {e}")
            return False
    
    
    def cancelar(self, id_reserva):
       
        try:
            conexao = conectar()
            cursor = conexao.cursor()
            query = "UPDATE reservas SET status = 'cancelada' WHERE id = %s"
            cursor.execute(query, (id_reserva,))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao cancelar reserva: {e}")
            return False
    
    def listar_salas_disponiveis(self):
  
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM salas WHERE ativo = TRUE ORDER BY nome"
            cursor.execute(query)
            salas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return salas
            
        except Exception as e:
            print(f"Erro ao listar salas: {e}")
            return []
    
    
    def listar_equipamentos_disponiveis(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT * FROM equipamentos WHERE ativo = TRUE ORDER BY nome"
            cursor.execute(query)
            equipamentos = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return equipamentos
            
        except Exception as e:
            print(f"Erro ao listar equipamentos: {e}")
            return []
