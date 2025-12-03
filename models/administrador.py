from database.conexao import conectar
class Administrador:
    
    def __init__(self):
        pass
    def listar_todos(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM administradores ORDER BY nome"
            cursor.execute(query)
            administradores = cursor.fetchall()
            cursor.close()
            conexao.close()
            return administradores
        except Exception as e:
            print(f"Erro ao listar administradores: {e}")
            return []
    
    def buscar_por_id(self, id_admin):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM administradores WHERE id = %s"
            cursor.execute(query, (id_admin,))
            admin = cursor.fetchone()
            cursor.close()
            conexao.close()
            return admin
        
        except Exception as e:
            print(f"Erro ao buscar administrador: {e}")
            return None
        
    def buscar_por_email(self, email):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT id, nome, email FROM administradores WHERE email = %s"
            cursor.execute(query, (email,))
            admin = cursor.fetchone()  
            cursor.close()
            conexao.close()
            return admin
            
        except Exception as e:
            print(f"Erro ao buscar administrador por email: {e}")
            return None
    def contar_total(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = "SELECT COUNT(*) as total FROM administradores"
            cursor.execute(query)
            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()
            return resultado['total'] if resultado else 0
    
        except Exception as e:
            print(f"Erro ao contar administradores: {e}")
            return 0
    
    def buscar_avisos_criados(self, id_admin):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            query = """
                SELECT 
                    id,
                    titulo,
                    tipo,
                    data_postagem,
                    fixado,
                    ativo
                FROM avisos
                WHERE id_autor = %s
                ORDER BY data_postagem DESC
                LIMIT 50
            """
            cursor.execute(query, (id_admin,))
            avisos = cursor.fetchall()
            cursor.close()
            conexao.close()
            return avisos
            
        except Exception as e:
            print(f"Erro ao buscar avisos do administrador: {e}")
            return []
       
    def buscar_estatisticas_sistema(self):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            estatisticas = {}
            cursor.execute("SELECT COUNT(*) as total FROM alunos")
            resultado = cursor.fetchone()
            estatisticas['total_alunos'] = resultado['total'] if resultado else 0
            
            
            cursor.execute("SELECT COUNT(*) as total FROM professores")
            resultado = cursor.fetchone()
            estatisticas['total_professores'] = resultado['total'] if resultado else 0
            


            cursor.execute("SELECT COUNT(*) as total FROM administradores")
            resultado = cursor.fetchone()
            estatisticas['total_administradores'] = resultado['total'] if resultado else 0
            


            cursor.execute("SELECT COUNT(*) as total FROM turmas WHERE ativa = TRUE")
            resultado = cursor.fetchone()
            estatisticas['total_turmas'] = resultado['total'] if resultado else 0
            


            cursor.execute("SELECT COUNT(*) as total FROM salas WHERE ativo = TRUE")
            resultado = cursor.fetchone()
            estatisticas['total_salas'] = resultado['total'] if resultado else 0
            


            cursor.execute("SELECT COUNT(*) as total FROM equipamentos WHERE ativo = TRUE")
            resultado = cursor.fetchone()
            estatisticas['total_equipamentos'] = resultado['total'] if resultado else 0
            


            cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE status = 'pendente'")
            resultado = cursor.fetchone()
            estatisticas['reservas_pendentes'] = resultado['total'] if resultado else 0
            

            cursor.execute("SELECT COUNT(*) as total FROM avisos WHERE ativo = TRUE")
            resultado = cursor.fetchone()
            estatisticas['total_avisos'] = resultado['total'] if resultado else 0
            cursor.close()
            conexao.close()
            return estatisticas
            
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {}
    
    
    def buscar_atividades_recentes(self, limite=10):
        try:
            conexao = conectar()
            cursor = conexao.cursor(dictionary=True)
            atividades = []
            query_reservas = """
                SELECT 
                    r.id,
                    r.tipo,
                    r.data_criacao,
                    r.status,
                    p.nome as professor_nome,
                    'reserva' as tipo_atividade
                FROM reservas r
                INNER JOIN professores p ON r.id_professor = p.id
                ORDER BY r.data_criacao DESC
                LIMIT %s
            """
            cursor.execute(query_reservas, (limite,))
            reservas = cursor.fetchall()
            atividades.extend(reservas)
            

            query_avisos = """
                SELECT 
                    a.id,
                    a.titulo,
                    a.data_postagem as data_criacao,
                    a.tipo,
                    ad.nome as admin_nome,
                    'aviso' as tipo_atividade
                FROM avisos a
                INNER JOIN administradores ad ON a.id_autor = ad.id
                ORDER BY a.data_postagem DESC
                LIMIT %s
            """
            
            cursor.execute(query_avisos, (limite,))
            avisos = cursor.fetchall()
            atividades.extend(avisos)
            atividades.sort(key=lambda x: x['data_criacao'], reverse=True)
            cursor.close()
            conexao.close()
            return atividades[:limite]
            
        except Exception as e:
            print(f"Erro ao buscar atividades recentes: {e}")
            return []
    
    def atualizar_perfil(self, id_admin, nome, email):
        try:
            if not nome or not nome.strip():
                print("Erro: Nome não pode estar vazio")
                return False
            
            if not email or not email.strip():
                print("Erro: Email não pode estar vazio")
                return False
            
            admin_existente = self.buscar_por_email(email)
            if admin_existente and admin_existente['id'] != id_admin:
                print(f"Erro: Email '{email}' já está em uso")
                return False
            conexao = conectar()
            cursor = conexao.cursor()
            query = """
                UPDATE administradores 
                SET nome = %s, email = %s 
                WHERE id = %s
            """
            cursor.execute(query, (nome.strip(), email.strip(), id_admin))
            conexao.commit()
            cursor.close()
            conexao.close()
            return True
            
        except Exception as e:
            print(f"Erro ao atualizar perfil do administrador: {e}")
            return False
    
    
    def atualizar_senha(self, id_admin, nova_senha_hash):
        try:
            if not nova_senha_hash:
                print("Erro: Senha não pode estar vazia")
                return False
            conexao = conectar()
            cursor = conexao.cursor()
            query = "UPDATE administradores SET senha = %s WHERE id = %s"
            cursor.execute(query, (nova_senha_hash, id_admin))
            conexao.commit()
            cursor.close()
            conexao.close()
            return True
        
        except Exception as e:
            print(f"Erro ao atualizar senha do administrador: {e}")
            return False
    
    def deletar(self, id_admin):
        try:
            total_admins = self.contar_total()
            if total_admins <= 1:
                print("Erro: Não é possível deletar o último administrador!")
                return False
            
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT COUNT(*) as total FROM avisos WHERE id_autor = %s",
                (id_admin,)
            )
            total_avisos = cursor.fetchone()['total']

            if total_avisos > 0:
                print(f"Aviso: Este admin tem {total_avisos} avisos criados")
            
            query = "DELETE FROM administradores WHERE id = %s"
            cursor.execute(query, (id_admin,))
            conexao.commit()
            cursor.close()
            conexao.close()
            return True
            
        except Exception as e:
            print(f"Erro ao deletar administrador: {e}")
            return False
    