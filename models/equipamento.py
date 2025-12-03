from database.conexao import conectar

class Equipamento:
    
    def __init__(self):
        pass
    
    def listar_todos(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo, ativo 
                FROM equipamentos 
                ORDER BY tipo, nome
            """
            
            cursor.execute(query)
            equipamentos = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return equipamentos
            
        except Exception as e:
            print(f"Erro ao listar equipamentos: {e}")
            return []
    
    def listar_ativos(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo 
                FROM equipamentos 
                WHERE ativo = TRUE 
                ORDER BY tipo, nome
            """
            
            cursor.execute(query)
            equipamentos = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return equipamentos
            
        except Exception as e:
            print(f"Erro ao listar equipamentos ativos: {e}")
            return []
    
    def listar_por_tipo(self, tipo):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo 
                FROM equipamentos 
                WHERE tipo = %s AND ativo = TRUE 
                ORDER BY nome
            """
            
            cursor.execute(query, (tipo,))
            equipamentos = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return equipamentos
            
        except Exception as e:
            print(f"Erro ao listar equipamentos por tipo: {e}")
            return []
    
    def buscar_por_id(self, id_equipamento):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo, ativo 
                FROM equipamentos 
                WHERE id = %s
            """
            
            cursor.execute(query, (id_equipamento,))
            equipamento = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return equipamento
            
        except Exception as e:
            print(f"Erro ao buscar equipamento: {e}")
            return None
    
    def buscar_por_nome(self, nome):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id, nome, tipo, ativo 
                FROM equipamentos 
                WHERE nome = %s
            """
        
            cursor.execute(query, (nome,))
            equipamento = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            return equipamento
            
        except Exception as e:
            print(f"Erro ao buscar equipamento por nome: {e}")
            return None
    
    def contar_total(self, apenas_ativos=False):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            if apenas_ativos:
                query = "SELECT COUNT(*) as total FROM equipamentos WHERE ativo = TRUE"
            else:
                query = "SELECT COUNT(*) as total FROM equipamentos"
            
            cursor.execute(query)
            resultado = cursor.fetchone()  
            cursor.close()
            conexao.close()
            
            return resultado['total'] if resultado else 0
            
        except Exception as e:
            print(f"Erro ao contar equipamentos: {e}")
            return 0
    
    def contar_por_tipo(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT tipo, COUNT(*) as total 
                FROM equipamentos 
                WHERE ativo = TRUE 
                GROUP BY tipo
            """
            
            cursor.execute(query)
            resultados = cursor.fetchall() 
            cursor.close()
            conexao.close()   
            contagem = {}
            
            for resultado in resultados:
                contagem[resultado['tipo']] = resultado['total']
            
            return contagem
            
        except Exception as e:
            print(f"Erro ao contar por tipo: {e}")
            return {}
    
    def verificar_disponibilidade(self, id_equipamento, data, horario_inicio, horario_fim, id_reserva_atual=None):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT id 
                FROM reservas 
                WHERE id_equipamento = %s 
                AND data = %s
                AND status IN ('pendente', 'aprovada')
                AND (
                    (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio < %s AND horario_fim > %s)
                    OR (horario_inicio >= %s AND horario_fim <= %s)
                )
            """

            parametros = [
                id_equipamento, data,
                horario_fim, horario_inicio,
                horario_fim, horario_inicio,
                horario_inicio, horario_fim
            ]
            
            if id_reserva_atual:
                query += " AND id != %s"
                parametros.append(id_reserva_atual)
            
            cursor.execute(query, tuple(parametros))
            conflitos = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return len(conflitos) == 0
            
        except Exception as e:
            print(f"Erro ao verificar disponibilidade: {e}")
            return False
    
    def buscar_reservas(self, id_equipamento, limite=10):
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
                WHERE r.id_equipamento = %s
                ORDER BY r.data DESC, r.horario_inicio DESC
                LIMIT %s
            """
            
            cursor.execute(query, (id_equipamento, limite))
            reservas = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return reservas
            
        except Exception as e:
            print(f"Erro ao buscar reservas do equipamento: {e}")
            return []
    
    def verificar_em_uso(self, id_equipamento):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT COUNT(*) as total FROM reservas WHERE id_equipamento = %s AND status IN ('pendente', 'aprovada')",
                (id_equipamento,)
            )
            tem_reservas = cursor.fetchone()['total'] > 0
            cursor.close()
            conexao.close()
            
            return tem_reservas
            
        except Exception as e:
            print(f"Erro ao verificar uso do equipamento: {e}")
            return True
    
    def criar(self, nome, tipo):
        try:
            if not nome or not nome.strip():
                print("Erro: Nome do equipamento não pode estar vazio")
                return False
            
            if not tipo or not tipo.strip():
                print("Erro: Tipo do equipamento não pode estar vazio")
                return False
            
            nome = nome.strip()
            tipo = tipo.strip()
            
            equipamento_existente = self.buscar_por_nome(nome)
            if equipamento_existente:
                print(f"Erro: Equipamento '{nome}' já existe")
                return False
            
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                INSERT INTO equipamentos (nome, tipo) 
                VALUES (%s, %s)
            """
            
            cursor.execute(query, (nome, tipo))
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar equipamento: {e}")
            return False
    
    def editar(self, id_equipamento, nome, tipo):
        try:
            if not nome or not nome.strip():
                print("Erro: Nome do equipamento não pode estar vazio")
                return False
            
            if not tipo or not tipo.strip():
                print("Erro: Tipo do equipamento não pode estar vazio")
                return False
            
            nome = nome.strip()
            tipo = tipo.strip()
            
            equipamento_existente = self.buscar_por_nome(nome)
            if equipamento_existente and equipamento_existente['id'] != id_equipamento:
                print(f"Erro: Já existe outro equipamento chamado '{nome}'")
                return False
            
            conexao = conectar()
            cursor = conexao.cursor()
            
            query = """
                UPDATE equipamentos 
                SET nome = %s, tipo = %s 
                WHERE id = %s
            """
            
            cursor.execute(query, (nome, tipo, id_equipamento))  
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao editar equipamento: {e}")
            return False
    
    def ativar(self, id_equipamento):
        try:
            conexao = conectar()
            cursor = conexao.cursor()      
            query = "UPDATE equipamentos SET ativo = TRUE WHERE id = %s"      
            cursor.execute(query, (id_equipamento,))       
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao ativar equipamento: {e}")
            return False
    
    def desativar(self, id_equipamento):
        try:
            conexao = conectar()
            cursor = conexao.cursor() 
            query = "UPDATE equipamentos SET ativo = FALSE WHERE id = %s"  
            cursor.execute(query, (id_equipamento,))   
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao desativar equipamento: {e}")
            return False
    
    def deletar(self, id_equipamento):
        try:
            if self.verificar_em_uso(id_equipamento):
                print("Erro: Não é possível deletar equipamento que está em uso!")
                print("Cancele as reservas primeiro.")
                return False
            
            conexao = conectar()
            cursor = conexao.cursor()        
            cursor.execute("DELETE FROM reservas WHERE id_equipamento = %s AND status = 'cancelada'", (id_equipamento,))
            cursor.execute("DELETE FROM equipamentos WHERE id = %s", (id_equipamento,))            
            conexao.commit()
            cursor.close()
            conexao.close()
            
            return True
            
        except Exception as e:
            print(f"Erro ao deletar equipamento: {e}")
            return False
    
    def buscar_com_estatisticas(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            
            query = """
                SELECT 
                    e.id,
                    e.nome,
                    e.tipo,
                    e.ativo,
                    COUNT(DISTINCT r.id) as total_reservas
                FROM equipamentos e
                LEFT JOIN reservas r ON e.id = r.id_equipamento AND r.status IN ('pendente', 'aprovada')
                GROUP BY e.id, e.nome, e.tipo, e.ativo
                ORDER BY e.tipo, e.nome
            """
            
            cursor.execute(query)
            equipamentos = cursor.fetchall()
            cursor.close()
            conexao.close()
            
            return equipamentos
            
        except Exception as e:
            print(f"Erro ao buscar equipamentos com estatísticas: {e}")
            return []
    
    def buscar_detalhes_completos(self, id_equipamento):
        try:
            equipamento = self.buscar_por_id(id_equipamento)
            
            if not equipamento:
                return None
            
            equipamento['reservas'] = self.buscar_reservas(id_equipamento, limite=20)
            equipamento['total_reservas'] = len(equipamento['reservas'])
            
            return equipamento
            
        except Exception as e:
            print(f"Erro ao buscar detalhes completos do equipamento: {e}")
            return None