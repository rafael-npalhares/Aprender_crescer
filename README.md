 Sistema Escolar 

Sistema de gestão escolar desenvolvido como parte da SA (Situação de Aprendizagem) do SENAI, utilizando arquitetura MVC com Python Flask.

---

 Equipe

- **Rafael Palhares** - Administrador
- **Natan Henrique** - Professor
- **Tiago Marghotti** - Professor  
- **Murilo Camargo** - Aluno



 Sobre o Projeto

A Escola "Aprender & Crescer" atende aproximadamente **850 alunos** do Ensino Fundamental ao Médio, funcionando de segunda a sexta, das 7h às 18h, com aulas em três turnos.

Este sistema foi desenvolvido para resolver problemas operacionais causados por processos manuais e planilhas desorganizadas, integrando:

 **Reservas** de salas, laboratórios, auditórios e equipamentos
-**Horários** personalizados por turma e professor
-**Mural de Avisos** centralizado



 Funcionalidades

 Módulo de Reservas
- Reserva de salas, laboratórios e auditórios por data/horário
- Reserva de equipamentos (projetores, notebooks, caixas de som)
- Aprovação/reprovação pelo administrador
- Cancelamento controlado
- Verificação automática de conflitos de horário

 Módulo de Horários
- Consulta de grade por turma (alunos)
- Visualização personalizada para professores
- Edição e atualização de horários (administradores)
- Validação automática de conflitos

 Módulo de Mural de Avisos
- Publicação de eventos, comunicados e informes
- Controle de versões e edição
- Avisos fixados no topo por 48h
- Gerenciamento completo pelo administrador

---

 Tecnologias Utilizadas

- **Backend:** Python 3.x + Flask
- **Banco de Dados:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript
- **Arquitetura:** MVC (Model-View-Controller)
- **Controle de Versão:** Git/GitHub



 Estrutura do Projeto

sistema_escola/
│
├── app.py                          # Aplicação principal Flask
│
├── database/
│   ├── CONEXAO.py                  # Gerenciador de conexões
│   └── script.sql                  # Script de criação do banco
│
├── models/                         # Lógica de negócio
│   ├── reserva_model.py
│   ├── horario_model.py
│   ├── aviso_model.py
│   └── usuario_model.py
│
├── controllers/                    # Coordenação entre Model e View
│   ├── reserva_controller.py
│   ├── horario_controller.py
│   └── aviso_controller.py
│
├── views/                          # Templates HTML
│   ├── base.html
│   ├── login.html
│   ├── reservas/
│   ├── horarios/
│   └── avisos/
│
├── static/                         # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
│
├── test_database.py                # Testes de leitura do banco
└── README.md                       # Este arquivo

3. **Instalar dependências**
```bash
pip install flask mysql-connector-python
```
4. **Configurar o banco de dados**

Edite o arquivo `database/CONEXAO.py` com suas credenciais:
```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'sua_senha'  
DB_NAME = 'escola_db'      
```

5. **Criar o banco de dados**
```bash
mysql -u root -p < database/script.sql
```

6. **Testar a conexão**
```bash
python database/CONEXAO.py
```

Se aparecer "Conexão OK!", está tudo certo!

 7. **Executar a aplicação**
```bash
python app.py
```

Acesse: ``



 Testar o Sistema

Para verificar se o banco está funcionando:

```bash
python test_database.py




 Níveis de Acesso

 Aluno
- Consultar grade de horários da própria turma
- Visualizar avisos do mural

 Professor
- Todas as permissões de aluno
- Solicitar reservas de salas e equipamentos
- Visualizar própria grade de horários
- Cancelar próprias reservas

 Administrador

- Todas as permissões anteriores
- Aprovar/reprovar reservas
- Criar e editar horários
- Publicar, editar e excluir avisos
- Gerenciar salas e equipamentos



 Requisitos Não Funcionais

-  Interface responsiva e intuitiva
-  Autenticação por níveis (aluno, professor, administrador)
-  Logs completos de todas as operações
-  Criptografia para dados sensíveis
-  Backup automático em nuvem
-  Normalização do banco até 3FN


 Fluxo de Operações

 Exemplo: Professor faz uma reserva

1. Professor acessa o módulo de Reservas
2. Seleciona equipamento (ex: Projetor), data e horário
3. Sistema verifica disponibilidade automaticamente
4. Se disponível, cria reserva com status "pendente"
5. Administrador recebe notificação
6. Administrador aprova ou reprova
7. Professor recebe confirmação



 Segurança

- Senhas criptografadas no banco de dados
- Sessões com timeout automático
- Validação de entrada em todos os formulários
- Proteção contra SQL Injection
- Logs auditáveis de todas as ações


 Backlog / Melhorias Futuras

- [ ] Sistema de notificações por email
- [ ] Aplicativo mobile
- [ ] Relatórios em PDF
- [ ] Dashboard com gráficos
- [ ] Integração com Google Calendar
- [ ] Sistema de frequência





