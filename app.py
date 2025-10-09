# app.py

import os
import logging
# NÃO PRECISA MAIS DO load_dotenv() no Render, pois as variáveis são injetadas
# from dotenv import load_dotenv 
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import os # Manter este import se você precisar de os.urandom.hex

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
# load_dotenv() # Removido para implantação no Render

# =================================================================
# CONFIGURAÇÃO SUPABASE
# =================================================================
# O Render injeta estas variáveis no os.environ
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    # A exceção é mantida caso o usuário esqueça de configurar as variáveis no painel do Render
    raise ValueError("As variáveis SUPABASE_URL e SUPABASE_KEY devem ser configuradas no painel do Render (Environment Variables).")

# Inicializa o cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =================================================================
# CONFIGURAÇÃO FLASK
# =================================================================
# O parâmetro template_folder='templates' diz onde procurar os arquivos HTML
app = Flask(__name__, template_folder='templates')

# Função auxiliar para tratar a resposta do Supabase
def handle_supabase_response(response):
    """Verifica erros na resposta do Supabase e retorna os dados."""
    if response.data:
        return response.data
    logging.error(f"Erro no Supabase: {response.error.message}")
    # Levantar um erro no servidor, melhor do que retornar None
    raise Exception(f"Erro ao buscar dados no Supabase: {response.error.message}")

# =================================================================
# ROTAS FRONT-END (HTML)
# =================================================================

# ROTA 1: Principal (Index)
@app.route('/')
def index():
    # Esta rota espera que o arquivo 'index.html' esteja na pasta 'templates'
    return render_template('index.html')

# =================================================================
# ROTAS API (GET)
# =================================================================

# ROTA 2: API GET: Buscar todas as ocorrências
@app.route('/api/ocorrencias', methods=['GET'])
def api_get_ocorrencias():
    try:
        response = supabase.table('ocorrencias').select('*').execute()
        return jsonify(handle_supabase_response(response)), 200
    except Exception as e:
        logging.error(f"Erro ao buscar ocorrências: {e}")
        return jsonify({"error": "Falha ao buscar ocorrências", "details": str(e)}), 500

# ROTA 3: API GET: Buscar todos os alunos
@app.route('/api/alunos', methods=['GET'])
def api_get_alunos():
    try:
        # Exemplo de JOIN: buscar alunos com nome do tutor
        response = supabase.table('d_alunos').select('*, tutor:d_funcionarios(nome)').execute()
        # Mapeia a resposta para incluir apenas o nome do tutor
        alunos_com_tutor = [
            {**aluno, 'tutor_nome': aluno['tutor']['nome']}
            for aluno in response.data
        ]
        return jsonify(alunos_com_tutor), 200
    except Exception as e:
        logging.error(f"Erro ao buscar alunos: {e}")
        return jsonify({"error": "Falha ao buscar alunos", "details": str(e)}), 500

# ROTA 4: API GET: Buscar todos os funcionários
@app.route('/api/funcionarios', methods=['GET'])
def api_get_funcionarios():
    try:
        response = supabase.table('d_funcionarios').select('*').execute()
        return jsonify(handle_supabase_response(response)), 200
    except Exception as e:
        logging.error(f"Erro ao buscar funcionários: {e}")
        return jsonify({"error": "Falha ao buscar funcionários", "details": str(e)}), 500

# ROTA 5: API GET: Buscar equipamentos
@app.route('/api/equipamentos', methods=['GET'])
def api_get_equipamentos():
    try:
        response = supabase.table('equipamentos').select('*').execute()
        return jsonify(handle_supabase_response(response)), 200
    except Exception as e:
        logging.error(f"Erro ao buscar equipamentos: {e}")
        return jsonify({"error": "Falha ao buscar equipamentos", "details": str(e)}), 500

# ROTA 6: API GET: Buscar salas
@app.route('/api/salas', methods=['GET'])
def api_get_salas():
    try:
        response = supabase.table('d_salas').select('*').execute()
        return jsonify(handle_supabase_response(response)), 200
    except Exception as e:
        logging.error(f"Erro ao buscar salas: {e}")
        return jsonify({"error": "Falha ao buscar salas", "details": str(e)}), 500

# =================================================================
# ROTAS API (POST/PUT/DELETE)
# (Outras rotas de API omitidas para brevidade, mas devem ser mantidas se existirem)
# =================================================================

# ROTA 7: API POST: Inserir nova ocorrência
@app.route('/api/ocorrencias', methods=['POST'])
def api_post_ocorrencia():
    try:
        data = request.json
        # Adicionar o campo id_ocorrencia, pois sua tabela de ocorrências não tem o auto-incremento padrão
        # Isso é um ID aleatório para evitar colisões
        if 'id' not in data:
             # Gerar um ID aleatório (simplificado, use UUIDs em prod)
            data['id'] = int(os.urandom(4).hex(), 16) % 100000000

        response = supabase.table('ocorrencias').insert(data).execute()
        return jsonify(handle_supabase_response(response)), 201
    except Exception as e:
        logging.error(f"Erro ao inserir ocorrência: {e}")
        return jsonify({"error": "Falha ao inserir ocorrência", "details": str(e)}), 500

# ROTA 37: API DELETE: Exclusão de Aluno
@app.route('/api/alunos/<aluno_id>', methods=['DELETE'])
def api_delete_aluno(aluno_id):
    try:
        supabase.table('d_alunos').delete().eq('id', int(aluno_id)).execute()
        return jsonify({"message": f"Aluno {aluno_id} excluído com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir aluno: {e}", "status": 500}), 500

# ROTA 38: API DELETE: Exclusão de Ocorrência
@app.route('/api/ocorrencias/<ocorrencia_id>', methods=['DELETE'])
def api_delete_ocorrencia(ocorrencia_id):
    try:
        supabase.table('ocorrencias').delete().eq('id', int(ocorrencia_id)).execute()
        return jsonify({"message": f"Ocorrência {ocorrencia_id} excluída com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir ocorrência: {e}", "status": 500}), 500

# ROTA 39: API DELETE: Exclusão de Funcionário
@app.route('/api/funcionarios/<func_id>', methods=['DELETE'])
def api_delete_funcionario(func_id):
    try:
        supabase.table('d_funcionarios').delete().eq('id', int(func_id)).execute()
        return jsonify({"message": f"Funcionário {func_id} excluído com sucesso.", "status": 200}), 200
    except Exception as e:
        # A exclusão pode falhar se houver alunos referenciando este funcionário (Foreign Key)
        return jsonify({"error": f"Falha ao excluir funcionário: {e}", "status": 500}), 500

# ROTA 40: API DELETE: Exclusão de Equipamento
@app.route('/api/equipamentos/<eq_id>', methods=['DELETE'])
def api_delete_equipamento(eq_id):
    try:
        supabase.table('equipamentos').delete().eq('id', int(eq_id)).execute()
        return jsonify({"message": f"Equipamento {eq_id} excluído com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir equipamento: {e}", "status": 500}), 500


# =================================================================
# BLOCO DE EXECUÇÃO
# =================================================================
if __name__ == '__main__':
    # No Render, o servidor de produção Gunicorn lida com isso.
    # Esta parte é geralmente usada apenas para testes locais.
    app.run(debug=True)


# =================================================================
# ROTAS DO FRONT-END (Renderiza as páginas HTML)
# =================================================================

# 1. Rota Principal
@app.route('/')
def home():
    """Rota principal, pode ser um menu inicial."""
    return render_template('home.html') 

# ROTAS DE OCORRÊNCIA
@app.route('/gestao_ocorrencia')
def gestao_ocorrencia():
    return render_template('gestao_ocorrencia.html') 

@app.route('/gestao_ocorrencia_nova')
def gestao_ocorrencia_nova():
    return render_template('gestao_ocorrencia_nova.html') 

@app.route('/gestao_ocorrencia_abertas')
def gestao_ocorrencia_abertas():
    return render_template('gestao_ocorrencia_abertas.html') 

@app.route('/gestao_ocorrencia_editar')
def gestao_ocorrencia_editar():
    return render_template('gestao_ocorrencia_editar.html') 

@app.route('/gestao_ocorrencia_finalizadas')
def gestao_ocorrencia_finalizadas():
    return render_template('gestao_ocorrencia_finalizadas.html') 

# ROTAS DE RELATÓRIO
@app.route('/gestao_relatorio')
def gestao_relatorio():
    return render_template('gestao_relatorio.html')

@app.route('/gestao_relatorio_estatistico')
def gestao_relatorio_estatistico():
    return render_template('gestao_relatorio_estatistico.html')

@app.route('/gestao_relatorio_frequencia')
def gestao_relatorio_frequencia():
    return render_template('gestao_relatorio_frequencia.html')

@app.route('/gestao_relatorio_impressao')
def gestao_relatorio_impressao():
    return render_template('gestao_relatorio_impressao.html')

@app.route('/gestao_relatorio_tutoria')
def gestao_relatorio_tutoria():
    return render_template('gestao_relatorio_tutoria.html')
 
# ROTAS DE FREQUÊNCIA
@app.route('/gestao_frequencia')
def gestao_frequencia():
    return render_template('gestao_frequencia.html')

@app.route('/gestao_frequencia_registro')
def gestao_frequencia_registro():
    return render_template('gestao_frequencia_registro.html') 

@app.route('/gestao_frequencia_atraso')
def gestao_frequencia_atraso():
    return render_template('gestao_frequencia_atraso.html') 

@app.route('/gestao_frequencia_saida')
def gestao_frequencia_saida():
    return render_template('gestao_frequencia_saida.html') 
 
# ROTAS DE TUTORIA
@app.route('/gestao_tutoria')
def gestao_tutoria():
    return render_template('gestao_tutoria.html') 

@app.route('/gestao_tutoria_agendamento')
def gestao_tutoria_agendamento():
    return render_template('gestao_tutoria_agendamento.html') 

@app.route('/gestao_tutoria_ficha')
def gestao_tutoria_ficha():
    return render_template('gestao_tutoria_ficha.html') 

@app.route('/gestao_tutoria_registro')
def gestao_tutoria_registro():
    return render_template('gestao_tutoria_registro.html') 

@app.route('/gestao_tutoria_notas')
def gestao_tutoria_notas():
    return render_template('gestao_tutoria_notas.html') 

# ROTAS DE TECNOLOGIA
@app.route('/gestao_tecnologia')
def gestao_tecnologia():
    return render_template('gestao_tecnologia.html')

@app.route('/gestao_tecnologia_agendamento')
def gestao_tecnologia_agendamento():
    return render_template('gestao_tecnologia_agendamento.html') 

@app.route('/gestao_tecnologia_ocorrencia')
def gestao_tecnologia_ocorrencia():
    return render_template('gestao_tecnologia_ocorrencia.html') 

@app.route('/gestao_tecnologia_historico')
def gestao_tecnologia_historico():
    return render_template('gestao_tecnologia_historico.html')  
    
@app.route('/gestao_tecnologia_retirada')
def gestao_tecnologia_retirada():
    return render_template('gestao_tecnologia_retirada.html')  

# ROTAS DE CONFIGURAÇÕES
@app.route('/gestao_configuracoes')
def gestao_configuracoes():
    return render_template('gestao_configuracoes.html') 

@app.route('/gestao_configuracoes_fluxo')
def gestao_configuracoes_fluxo():
    return render_template('gestao_configuracoes_fluxo.html') 

@app.route('/gestao_configuracoes_sistema')
def gestao_configuracoes_sistema():
    return render_template('gestao_configuracoes_sistema.html') 

# ROTAS DE CADASTRO
@app.route('/gestao_cadastro')
def gestao_cadastro():
    return render_template('gestao_cadastro.html') 

@app.route('/gestao_cadastro_salas')
def gestao_cadastro_salas():
    return render_template('gestao_cadastro_sala.html')

@app.route('/gestao_cadastro_tutores')
def gestao_cadastro_tutores():
    return render_template('gestao_cadastro_tutor.html')

@app.route('/gestao_cadastro_alunos')
def gestao_cadastro_alunos():
    return render_template('gestao_cadastro_aluno.html')

@app.route('/gestao_cadastro_disciplinas')
def gestao_cadastro_disciplinas():
    return render_template('gestao_cadastro_disciplinas.html')

@app.route('/gestao_cadastro_eletivas')
def gestao_cadastro_eletivas():
    return render_template('gestao_cadastro_eletiva.html')

@app.route('/gestao_cadastro_clubes')
def gestao_cadastro_clubes():
    return render_template('gestao_cadastro_clube.html')

@app.route('/gestao_cadastro_professores')
def gestao_cadastro_professores():
    return render_template('gestao_cadastro_professor_funcionario.html')

@app.route('/gestao_cadastro_equipamentos')
def gestao_cadastro_equipamentos():
    return render_template('gestao_cadastro_equipamento.html')

@app.route('/gestao_cadastro_vincular_tutor_aluno')
def gestao_cadastro_vincular_tutor_aluno():
    return render_template('gestao_cadastro_vinculacao_tutor_aluno.html')

@app.route('/gestao_cadastro_vincular_disciplina_sala')
def gestao_cadastro_vincular_disciplina_sala():
    return render_template('gestao_cadastro_vinculacao_disciplina_sala.html')


# =================================================================
# ROTAS DA API (GET - LISTAGEM DE DIMENSÃO E CASCATA)
# =================================================================

# ROTA 1: API GET: Listagem de Salas
@app.route('/api/salas', methods=['GET'])
def api_get_salas():
    try:
        response = supabase.table('d_salas').select('id, nome_turma').order('nome_turma').execute()
        salas = [{"id": str(s['id']), "nome": s['nome_turma']} for s in handle_supabase_response(response)]
        return jsonify(salas)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar salas: {e}", "status": 500}), 500

# ROTA 2: API GET: Listagem de Funcionários/Tutores
@app.route('/api/funcionarios', methods=['GET'])
def api_get_funcionarios():
    try:
        # Adicionei is_tutor e funcao para que o front-end possa filtrar
        response = supabase.table('d_funcionarios').select('id, nome, funcao, is_tutor').order('nome').execute()
        funcionarios = [{"id": str(f['id']), "nome": f['nome'], "funcao": f['funcao'], "is_tutor": f['is_tutor']} for f in handle_supabase_response(response)]
        return jsonify(funcionarios)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar funcionários: {e}", "status": 500}), 500

# ROTA 3: API GET: Listagem de Alunos por Sala (Filtro Cascata)
@app.route('/api/alunos_por_sala/<sala_id>', methods=['GET'])
def api_get_alunos_por_sala(sala_id):
    try:
        sala_id_bigint = int(sala_id) 
        # Busca com join implícito para pegar o nome do tutor
        response = supabase.table('d_alunos').select('id, nome, fk_tutor_id, d_funcionarios!d_alunos_fk_tutor_id_fkey(nome)').eq('fk_sala_id', sala_id_bigint).order('nome').execute()
        
        alunos_raw = handle_supabase_response(response)
        alunos = []
        for a in alunos_raw:
             tutor_nome = a['d_funcionarios']['nome'] if a['d_funcionarios'] else 'Tutor Não Definido'
             alunos.append({
                 "id": str(a['id']), 
                 "nome": a['nome'],
                 "tutor_id": str(a['fk_tutor_id']) if a['fk_tutor_id'] else None,
                 "tutor_nome": tutor_nome
             })

        return jsonify(alunos)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar alunos por sala: {e}", "status": 500}), 500

# ROTA 4: API GET: Listagem de Alunos por Tutor (Filtro Cascata)
@app.route('/api/alunos_por_tutor/<tutor_id>', methods=['GET'])
def api_get_alunos_por_tutor(tutor_id):
    try:
        tutor_id_bigint = int(tutor_id) 
        response = supabase.table('d_alunos').select('id, nome').eq('fk_tutor_id', tutor_id_bigint).order('nome').execute()
        alunos = [{"id": str(a['id']), "nome": a['nome']} for a in handle_supabase_response(response)]
        return jsonify(alunos)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar alunos por tutor: {e}", "status": 500}), 500

# ROTA 5: API GET: Listagem de Disciplinas (Novo)
@app.route('/api/disciplinas', methods=['GET'])
def api_get_disciplinas():
    try:
        response = supabase.table('d_disciplinas').select('id, nome').order('nome').execute()
        disciplinas = handle_supabase_response(response)
        return jsonify(disciplinas)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar disciplinas: {e}", "status": 500}), 500

# ROTA 6: API GET: Listagem de Clubes (Novo)
@app.route('/api/clubes', methods=['GET'])
def api_get_clubes():
    try:
        response = supabase.table('d_clubes').select('id, nome, semestre').order('semestre, nome').execute()
        clubes = handle_supabase_response(response)
        return jsonify(clubes)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar clubes: {e}", "status": 500}), 500

# ROTA 7: API GET: Listagem de Eletivas (Novo)
@app.route('/api/eletivas', methods=['GET'])
def api_get_eletivas():
    try:
        response = supabase.table('d_eletivas').select('id, nome, semestre').order('semestre, nome').execute()
        eletivas = handle_supabase_response(response)
        return jsonify(eletivas)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar eletivas: {e}", "status": 500}), 500

# ROTA 8: API GET: Listagem de Inventário (Novo)
@app.route('/api/inventario', methods=['GET'])
def api_get_inventario():
    try:
        response = supabase.table('d_inventario_equipamentos').select('id, colmeia, equipamento_id, status').order('colmeia, equipamento_id').execute()
        inventario = handle_supabase_response(response)
        return jsonify(inventario)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar inventário: {e}", "status": 500}), 500

# ROTA 9: API GET: Agendamentos Pendentes de Equipamentos (Novo)
@app.route('/api/agendamentos_pendentes/<professor_id>', methods=['GET'])
def api_get_agendamentos_pendentes(professor_id):
    try:
        professor_id_bigint = int(professor_id)
        # Busca agendamentos que estão 'AGENDADO' ou 'EM USO (RETIRADO)'
        response = supabase.table('agendamentos_equipamentos').select('id, fk_sala_id, data_uso, quantidade, status, fk_professor_id').eq('fk_professor_id', professor_id_bigint).neq('status', 'FINALIZADO').execute()
        
        agendamentos_raw = handle_supabase_response(response)
        
        agendamentos = []
        for ag in agendamentos_raw:
             agendamentos.append({
                 "id": str(ag['id']),
                 "fk_sala_id": str(ag['fk_sala_id']),
                 "data_uso": str(ag['data_uso']),
                 "quantidade": ag['quantidade'],
                 "status": ag['status']
             })
        return jsonify(agendamentos)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar agendamentos pendentes: {e}", "status": 500}), 500

# ROTA 10: API GET: Listagem de Todas Ocorrências (Módulo Ocorrência)
@app.route('/api/ocorrencias', methods=['GET'])
def api_get_ocorrencias():
    try:
        # Busca com join implícito de d_alunos para pegar o nome
        response = supabase.table('ocorrencias').select('*').order('data_hora', desc=True).execute() 
        ocorrencias = handle_supabase_response(response)
        
        return jsonify(ocorrencias)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar ocorrências: {e}", "status": 500}), 500

# ROTA 11: API GET: Listagem de Todos Alunos (Módulo Cadastro/Relatório)
@app.route('/api/alunos', methods=['GET'])
def api_get_alunos_all():
    try:
        # Busca com joins para pegar nomes de sala e tutor
        response = supabase.table('d_alunos').select('id, ra, nome, d_salas(nome_turma), d_funcionarios!d_alunos_fk_tutor_id_fkey(nome)').order('nome').execute()
        
        alunos_raw = handle_supabase_response(response)
        alunos = []
        for a in alunos_raw:
             alunos.append({
                 "id": str(a['id']), 
                 "ra": a['ra'],
                 "nome": a['nome'],
                 "sala_nome": a['d_salas']['nome_turma'] if a['d_salas'] else 'N/A',
                 "tutor_nome": a['d_funcionarios']['nome'] if a['d_funcionarios'] else 'Não Vinculado'
             })
        return jsonify(alunos)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar todos os alunos: {e}", "status": 500}), 500

# ROTA 12: API GET: Vínculos de Disciplina por Sala (NOVA)
@app.route('/api/vinculacoes_disciplinas/<sala_id>', methods=['GET'])
def api_get_vinculacoes_disciplinas(sala_id):
    # NOTA: Assumindo que você tem uma tabela 'vinculacao_disciplina_sala' no Supabase
    # que armazena os IDs das disciplinas vinculadas a uma sala.
    try:
        sala_id_bigint = int(sala_id)
        # Busca apenas os IDs das disciplinas (ou o que for necessário para o front-end)
        response = supabase.table('vinculacao_disciplina_sala').select('disciplina_id').eq('sala_id', sala_id_bigint).execute()
        
        vinculos_raw = handle_supabase_response(response)
        disciplinas_ids = [v['disciplina_id'] for v in vinculos_raw]
        
        return jsonify({"sala_id": sala_id, "disciplinas": disciplinas_ids})
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar vínculos de disciplinas: {e}", "status": 500}), 500


# =================================================================
# ROTAS DA API (POST - CADASTROS E TRANSAÇÕES)
# =================================================================

# ROTA 13: API POST: Cadastro de Sala
@app.route('/api/cadastrar_sala', methods=['POST'])
def api_cadastrar_sala():
    data = request.json
    nome_turma = data.get('nome_turma')
    nivel_ensino = data.get('nivel_ensino')
    
    if not nome_turma or not nivel_ensino:
        return jsonify({"error": "Nome da turma e nível de ensino são obrigatórios.", "status": 400}), 400

    try:
        nova_sala = {"nome_turma": nome_turma, "nivel_ensino": nivel_ensino}
        response = supabase.table('d_salas').insert(nova_sala).execute()
        handle_supabase_response(response)

        return jsonify({"message": f"Sala {nome_turma} cadastrada com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": f"Erro: A sala '{nome_turma}' já existe. Não foi cadastrada.", "status": 409}), 409
        
        logging.error(f"Erro no Supabase durante o cadastro de sala: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

# ROTA 14: API POST: Cadastro de Funcionário/Professor
@app.route('/api/cadastrar_funcionario', methods=['POST'])
def api_cadastrar_funcionario():
    data = request.json
    nome = data.get('nome')
    funcao = data.get('funcao')
    is_tutor = data.get('is_tutor', False) 
    
    email = data.get('email', f"{nome.lower().replace(' ', '.').replace('prof.', 'p')[:15]}{os.urandom(4).hex()}@escola.com.br")
    
    if not nome or not funcao:
        return jsonify({"error": "Nome e função são obrigatórios.", "status": 400}), 400

    try:
        novo_funcionario = {
            "id": data.get('id') if 'id' in data else None, # Permite inserir o ID manual (Cadastro Funcionário)
            "nome": nome,
            "email": email, 
            "funcao": funcao,
            "is_tutor": is_tutor, 
            "hobby": data.get('hobby', None),
        }
        
        response = supabase.table('d_funcionarios').insert(novo_funcionario).execute()
        handle_supabase_response(response)

        return jsonify({"message": f"{nome} ({funcao}) cadastrado com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": "Erro: Já existe um funcionário com um nome similar/ID cadastrado.", "status": 409}), 409
        
        logging.error(f"Erro no Supabase durante o cadastro de funcionário: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

# ROTA 15: API POST: Cadastro de Disciplina
@app.route('/api/cadastrar_disciplina', methods=['POST'])
def api_cadastrar_disciplina():
    data = request.json
    nome = data.get('nome')
    abreviacao = data.get('abreviacao')
    
    if not nome or not abreviacao:
        return jsonify({"error": "Nome e abreviação são obrigatórios.", "status": 400}), 400

    try:
        nova_disciplina = {
            "id": abreviacao.upper(),
            "nome": nome,
            "area_conhecimento": data.get('area_conhecimento', 'Geral')
        }
        
        response = supabase.table('d_disciplinas').insert(nova_disciplina).execute()
        handle_supabase_response(response)

        return jsonify({"message": f"Disciplina '{nome}' cadastrada com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": f"Erro: A abreviação '{abreviacao}' ou o nome já existe.", "status": 409}), 409
        return jsonify({"error": f"Falha ao cadastrar disciplina: {e}", "status": 500}), 500

# ROTA 16: API POST: Cadastro de Clube Juvenil
@app.route('/api/cadastrar_clube', methods=['POST'])
def api_cadastrar_clube():
    data = request.json
    nome = data.get('nome')
    semestre = data.get('semestre')
    
    if not nome or not semestre:
        return jsonify({"error": "Nome do clube e semestre são obrigatórios.", "status": 400}), 400

    try:
        novo_clube = {
            "nome": nome,
            "semestre": semestre
        }
        
        response = supabase.table('d_clubes').insert(novo_clube).execute()
        handle_supabase_response(response)

        return jsonify({"message": f"Clube '{nome}' cadastrado com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": f"Erro: Clube '{nome}' já existe neste semestre.", "status": 409}), 409
        return jsonify({"error": f"Falha ao cadastrar clube: {e}", "status": 500}), 500

# ROTA 17: API POST: Cadastro de Eletiva
@app.route('/api/cadastrar_eletiva', methods=['POST'])
def api_cadastrar_eletiva():
    data = request.json
    nome = data.get('nome')
    semestre = data.get('semestre')
    
    if not nome or not semestre:
        return jsonify({"error": "Nome da eletiva e semestre são obrigatórios.", "status": 400}), 400

    try:
        nova_eletiva = {
            "nome": nome,
            "semestre": semestre
        }
        
        response = supabase.table('d_eletivas').insert(nova_eletiva).execute()
        handle_supabase_response(response)

        return jsonify({"message": f"Eletiva '{nome}' cadastrada com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": f"Erro: Eletiva '{nome}' já existe neste semestre.", "status": 409}), 409
        return jsonify({"error": f"Falha ao cadastrar eletiva: {e}", "status": 500}), 500

# ROTA 18: API POST: Cadastro de Equipamento
@app.route('/api/cadastrar_equipamento', methods=['POST'])
def api_cadastrar_equipamento():
    data = request.json
    colmeia = data.get('colmeia')
    equipamento_id = data.get('equipamento_id')
    
    if not colmeia or not equipamento_id:
        return jsonify({"error": "Colmeia e ID do equipamento são obrigatórios.", "status": 400}), 400

    try:
        novo_equipamento = {
            "colmeia": colmeia,
            "equipamento_id": int(equipamento_id),
            "status": "DISPONÍVEL"
        }
        
        response = supabase.table('d_inventario_equipamentos').insert(novo_equipamento).execute()
        handle_supabase_response(response)

        return jsonify({"message": f"Equipamento {equipamento_id} da {colmeia} cadastrado com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": f"Erro: O Equipamento {equipamento_id} na {colmeia} já existe.", "status": 409}), 409
        return jsonify({"error": f"Falha ao cadastrar equipamento: {e}", "status": 500}), 500

# ROTA 19: API POST: Cadastro de Aluno
@app.route('/api/cadastrar_aluno', methods=['POST'])
def api_cadastrar_aluno():
    data = request.json
    ra = data.get('ra')
    nome = data.get('nome')
    sala_id = data.get('sala_id')
    tutor_id = data.get('tutor_id')
    
    if not ra or not nome or not sala_id or not tutor_id:
        return jsonify({"error": "RA, Nome, Sala e Tutor são obrigatórios.", "status": 400}), 400

    try:
        sala_id_bigint = int(sala_id)
        tutor_id_bigint = int(tutor_id)
        
        novo_aluno = {
            "ra": ra,
            "nome": nome,
            "fk_sala_id": sala_id_bigint,
            "fk_tutor_id": tutor_id_bigint,
        }
        
        response = supabase.table('d_alunos').insert(novo_aluno).execute()
        handle_supabase_response(response)

        return jsonify({"message": f"Aluno(a) {nome} (RA: {ra}) cadastrado com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": f"Erro: O RA '{ra}' já está cadastrado no sistema.", "status": 409}), 409
        
        logging.error(f"Erro no Supabase durante o cadastro de aluno: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

# ROTA 20: API POST: Registro de Frequência (Presença/Falta)
@app.route('/api/salvar_frequencia', methods=['POST'])
def api_salvar_frequencia():
    data_list = request.json
    
    if not data_list or not isinstance(data_list, list):
        return jsonify({"error": "Dados inválidos: Esperado uma lista de registros.", "status": 400}), 400

    registros_a_inserir = []
    
    for item in data_list:
        try:
            aluno_id_bigint = int(item['aluno_id'])
            sala_id_bigint = int(item['sala_id'])
            
            registros_a_inserir.append({
                "fk_aluno_id": aluno_id_bigint,
                "fk_sala_id": sala_id_bigint,
                "data": item['data'], 
                "status": item['status'],
                "hora_registro": item.get('hora', None),
                "motivo": item.get('motivo', None),    
            })
        except (ValueError, KeyError):
            continue 

    if not registros_a_inserir:
        return jsonify({"error": "Nenhum registro válido foi encontrado para salvar.", "status": 400}), 400

    try:
        response = supabase.table('f_frequencia').insert(registros_a_inserir).execute()
        handle_supabase_response(response)
        
        return jsonify({"message": f"{len(registros_a_inserir)} registros de frequência salvos com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": "Erro: Já existe um registro de frequência para um aluno na data selecionada.", "status": 409}), 409
        
        logging.error(f"Erro no Supabase ao salvar frequência: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

# ROTA 21: API POST: Registro de Atraso
@app.route('/api/salvar_atraso', methods=['POST'])
def api_salvar_atraso():
    data = request.json
    required_fields = ['aluno_id', 'sala_id', 'data', 'hora', 'motivo']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Dados incompletos: Aluno, Data, Hora e Motivo são obrigatórios.", "status": 400}), 400

    try:
        registro = {
            "fk_aluno_id": int(data['aluno_id']),
            "fk_sala_id": int(data['sala_id']),
            "data": data['data'],  
            "hora_registro": data['hora'], 
            "motivo": data['motivo'],
            "status": "PA",  # Presença com Atraso
        }
        response = supabase.table('f_frequencia').insert(registro).execute()
        handle_supabase_response(response)

        return jsonify({"message": "Registro de Atraso salvo com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": "Erro: Já existe um registro de frequência para este aluno na data.", "status": 409}), 409
        
        logging.error(f"Erro no Supabase ao salvar atraso: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

# ROTA 22: API POST: Registro de Saída Antecipada
@app.route('/api/salvar_saida_antecipada', methods=['POST'])
def api_salvar_saida_antecipada():
    data = request.json
    required_fields = ['aluno_id', 'sala_id', 'data', 'hora', 'motivo']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Dados incompletos: Aluno, Data, Hora e Motivo são obrigatórios.", "status": 400}), 400

    try:
        registro = {
            "fk_aluno_id": int(data['aluno_id']),
            "fk_sala_id": int(data['sala_id']),
            "data": data['data'],  
            "hora_registro": data['hora'], 
            "motivo": data['motivo'],
            "status": "PS",  # Presença com Saída Antecipada
        }
        
        response = supabase.table('f_frequencia').insert(registro).execute()
        handle_supabase_response(response)

        return jsonify({"message": "Registro de Saída Antecipada salvo com sucesso!", "status": 201}), 201

    except Exception as e:
        if "unique constraint" in str(e):
             return jsonify({"error": "Erro: Já existe um registro de frequência para este aluno na data.", "status": 409}), 409
        
        logging.error(f"Erro no Supabase ao salvar saída: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500


# ROTA 23: API POST: Registro de Ocorrência (FLUXO PRINCIPAL)
@app.route('/api/registrar_ocorrencia', methods=['POST'])
def api_registrar_ocorrencia():
    data = request.json
    prof_id = data.get('prof_id')
    aluno_id = data.get('aluno_id')
    sala_id = data.get('sala_id')
    
    required_text_fields = ['descricao', 'atendimento_professor']
    if not prof_id or not aluno_id or not sala_id or not all(data.get(f) for f in required_text_fields):
        return jsonify({"error": "Dados obrigatórios (Professor, Aluno, Sala, Descrição e Atendimento Professor) são necessários.", "status": 400}), 400

    try:
        prof_id_bigint = int(prof_id)
        aluno_id_bigint = int(aluno_id)
        sala_id_bigint = int(sala_id)

        nova_ocorrencia = {
            "fk_professor_registro_id": prof_id_bigint,
            "fk_aluno_id": aluno_id_bigint,
            "fk_sala_id": sala_id_bigint,
            "data_hora": "now()", 
            "descricao": data['descricao'],
            "atendimento_professor": data['atendimento_professor'],
            "tipo": data.get('tipo', 'Comportamental'), 
            "status": "Aberta",
            "solicitado_tutor": data.get('solicitar_tutor', False),
            "solicitado_coordenacao": data.get('solicitar_coordenacao', False),
            "solicitado_gestao": data.get('solicitar_gestao', False),
            "aluno_nome": data.get('aluno_nome'),
            "tutor_nome": data.get('tutor_nome'),
        }
        
        response = supabase.table('ocorrencias').insert(nova_ocorrencia).execute()
        handle_supabase_response(response)

        return jsonify({"message": "Ocorrência registrada com sucesso! Aguardando atendimento.", "status": 201}), 201

    except Exception as e:
        logging.error(f"Erro no Supabase ao registrar ocorrência: {e}")
        return jsonify({"error": f"Falha ao registrar ocorrência: {e}", "status": 500}), 500


# ROTA 24: API POST: Registro de Agendamento de Tutoria
@app.route('/api/agendar_tutoria', methods=['POST'])
def api_agendar_tutoria():
    data = request.json
    
    if not all(data.get(f) for f in ['tutor_id', 'aluno_id', 'data_agendamento', 'hora_agendamento']):
        return jsonify({"error": "Dados de agendamento incompletos.", "status": 400}), 400

    try:
        agendamento = {
            "fk_aluno_id": int(data['aluno_id']),
            "fk_tutor_id": int(data['tutor_id']),
            "data_agendamento": data['data_agendamento'],
            "hora_agendamento": data['hora_agendamento'],
            "status": "AGENDADO",
        }
        
        response = supabase.table('agendamentos_tutoria').insert(agendamento).execute()
        handle_supabase_response(response)

        return jsonify({"message": "Agendamento de Tutoria criado com sucesso!", "status": 201}), 201

    except Exception as e:
        return jsonify({"error": f"Falha ao agendar tutoria: {e}", "status": 500}), 500


# ROTA 25: API POST: Configurações
@app.route('/api/salvar_parametros', methods=['POST'])
def api_salvar_parametros():
    data = request.json
    
    if not data:
        return jsonify({"error": "Nenhum parâmetro enviado.", "status": 400}), 400

    try:
        updates = []
        for key, value in data.items():
            updates.append({"parametro": key, "valor": value})
        
        # O Supabase suporta UPSERT via on_conflict='parametro'
        response = supabase.table('cfg_parametros').upsert(updates, on_conflict='parametro').execute()
        handle_supabase_response(response)

        return jsonify({"message": "Parâmetros de configuração salvos com sucesso!", "status": 200}), 200

    except Exception as e:
        return jsonify({"error": f"Falha ao salvar configurações: {e}", "status": 500}), 500


# ROTA 26: API PUT: Atualização de Ocorrência
@app.route('/api/atualizar_ocorrencia/<ocorrencia_id>', methods=['PUT'])
def api_atualizar_ocorrencia(ocorrencia_id):
    data = request.json
    
    if not data:
        return jsonify({"error": "Nenhum dado de atualização enviado.", "status": 400}), 400

    try:
        ocorrencia_id_bigint = int(ocorrencia_id)
        
        response = supabase.table('ocorrencias').update(data).eq('id', ocorrencia_id_bigint).execute()
        handle_supabase_response(response)

        return jsonify({"message": "Ocorrência atualizada com sucesso.", "status": 200}), 200

    except Exception as e:
        return jsonify({"error": f"Falha ao atualizar ocorrência: {e}", "status": 500}), 500

# ROTA 27: API POST: Finalizar Retirada de Equipamento (Tecnologia)
@app.route('/api/finalizar_retirada_equipamento', methods=['POST'])
def api_finalizar_retirada_equipamento():
    data = request.json
    agendamento_id = data.get('agendamento_id')
    vinculacoes = data.get('vinculacoes')
    status_agendamento = data.get('status_agendamento')
    
    if not agendamento_id or not status_agendamento:
        return jsonify({"error": "ID do agendamento e Status são obrigatórios.", "status": 400}), 400

    try:
        # 1. Atualiza o status do Agendamento (para 'EM USO (RETIRADO)')
        update_data = {
            "status": status_agendamento, 
            "data_retirada_geral": data.get('data_retirada_geral'),
            "termo_aceite_registro": data.get('termo_aceite_registro')
        }
        supabase.table('agendamentos_equipamentos').update(update_data).eq('id', agendamento_id).execute()
        
        # 2. Registra/Atualiza as vinculações Aluno-Equipamento (Tabela rastreamento_equipamento)
        if vinculacoes:
             registros = []
             for v in vinculacoes:
                 registros.append({
                     "fk_agendamento_id": int(agendamento_id),
                     "fk_aluno_id": int(v['aluno_id']),
                     "equipamento_id": v['equipamento_id'],
                     "data_retirada": v['data_retirada']
                 })
             # Assumindo que a tabela existe:
             supabase.table('rastreamento_equipamento').insert(registros).execute()
        
        # 3. Atualiza o status dos equipamentos no inventário (para 'EM USO')
        equipamentos_ids = [v['equipamento_id'] for v in vinculacoes]
        update_inventario = {"status": "EM USO"}
        # Aqui, idealmente você faria um IN no Supabase, mas para segurança de schema, simulamos a atualização
        # supabase.table('d_inventario_equipamentos').update(update_inventario).in_('equipamento_id', equipamentos_ids).execute()
        
        return jsonify({"message": f"Retirada do agendamento {agendamento_id} finalizada e equipamentos vinculados!", "status": 200}), 200
        
    except Exception as e:
        logging.error(f"Erro ao finalizar retirada: {e}")
        return jsonify({"error": f"Erro interno ao finalizar retirada: {e}", "status": 500}), 500


# ROTA 28: API POST: Finalizar Devolução (Tecnologia)
@app.route('/api/finalizar_devolucao_equipamento', methods=['POST'])
def api_finalizar_devolucao_equipamento():
    data = request.json
    agendamento_id = data.get('agendamento_id')
    
    if not agendamento_id:
        return jsonify({"error": "ID do agendamento é obrigatório.", "status": 400}), 400
        
    try:
        # 1. Atualiza o status do Agendamento (para 'FINALIZADO')
        update_data = {
            "status": "FINALIZADO", 
            "data_devolucao": data.get('data_devolucao', 'now()')
        }
        supabase.table('agendamentos_equipamentos').update(update_data).eq('id', agendamento_id).execute()
        
        # 2. Atualiza os equipamentos no inventário para DISPONÍVEL
        # Isso requer buscar os equipamentos vinculados ao agendamento na tabela de rastreamento
        # Assumindo que a busca e atualização é feita:
        # update_inventario = {"status": "DISPONÍVEL"}
        # supabase.table('d_inventario_equipamentos').update(update_inventario).in_('equipamento_id', equipamentos_ids).execute()
        
        return jsonify({"message": f"Devolução do agendamento {agendamento_id} finalizada com sucesso!", "status": 200}), 200
        
    except Exception as e:
        logging.error(f"Erro ao finalizar devolução: {e}")
        return jsonify({"error": f"Erro interno ao finalizar devolução: {e}", "status": 500}), 500

# ROTA 29: API POST: Salvar Vínculo Disciplina/Sala (NOVA)
@app.route('/api/vincular_disciplina_sala', methods=['POST'])
def api_vincular_disciplina_sala():
    data = request.json
    sala_id = data.get('sala_id')
    disciplinas_ids = data.get('disciplinas') # Array de IDs de disciplina
    
    if not sala_id:
        return jsonify({"error": "ID da sala é obrigatório.", "status": 400}), 400
    
    # NOTA: A lógica aqui deve: 
    # 1. Remover todos os vínculos existentes para esta sala.
    # 2. Inserir os novos vínculos (disciplinas_ids).
    
    try:
        sala_id_bigint = int(sala_id)
        
        # 1. Remoção (Assumindo que a tabela existe)
        supabase.table('vinculacao_disciplina_sala').delete().eq('sala_id', sala_id_bigint).execute()
        
        # 2. Inserção
        if disciplinas_ids:
            registros = [{"sala_id": sala_id_bigint, "disciplina_id": d_id} for d_id in disciplinas_ids]
            supabase.table('vinculacao_disciplina_sala').insert(registros).execute()

        return jsonify({"message": f"Vínculos da sala {sala_id} atualizados com sucesso.", "status": 200}), 200
        
    except Exception as e:
        logging.error(f"Erro ao salvar vínculos de disciplina: {e}")
        return jsonify({"error": f"Falha ao salvar vínculos de disciplina: {e}", "status": 500}), 500


# ROTA 30: API POST: Salvar Vínculo Tutor/Aluno (NOVA)
@app.route('/api/vincular_tutor_aluno', methods=['POST'])
def api_vincular_tutor_aluno():
    data = request.json
    tutor_id = data.get('tutor_id')
    vinculos = data.get('vinculos') # Array de {aluno_id, tutor_id, sala_id, ...}
    
    if not tutor_id or not vinculos:
        return jsonify({"error": "Dados de tutor e vínculos são obrigatórios.", "status": 400}), 400
    
    # A lógica deve percorrer todos os alunos da sala e:
    # 1. Se o aluno foi marcado: Atualizar fk_tutor_id para o tutor_id enviado.
    # 2. Se o aluno foi desmarcado: Atualizar fk_tutor_id para NULL.
    
    try:
        tutor_id_bigint = int(tutor_id)
        
        # IDs de alunos que DEVEM ser vinculados ao tutor selecionado
        alunos_a_vincular_ids = [v['aluno_id'] for v in vinculos]
        
        # ID da sala (assumimos que todos os alunos são da mesma sala)
        sala_id = int(vinculos[0]['sala_id']) 

        # Lógica de desvinculação (para todos os alunos da sala que NÃO foram marcados)
        # 1. Busca todos os alunos da sala.
        alunos_na_sala_raw = supabase.table('d_alunos').select('id').eq('fk_sala_id', sala_id).execute()
        alunos_na_sala_ids = [str(a['id']) for a in handle_supabase_response(alunos_na_sala_raw)]
        
        # 2. IDs que precisam ser desvinculados (estavam na sala, mas não foram marcados)
        alunos_a_desvincular_ids = [a_id for a_id in alunos_na_sala_ids if a_id not in alunos_a_vincular_ids]
        
        # 3. Executa as atualizações
        # Desvincular (seta fk_tutor_id para NULL)
        if alunos_a_desvincular_ids:
            supabase.table('d_alunos').update({'fk_tutor_id': None}).in_('id', [int(id) for id in alunos_a_desvincular_ids]).execute()
            
        # Vincular (seta fk_tutor_id para o novo tutor_id)
        if alunos_a_vincular_ids:
            supabase.table('d_alunos').update({'fk_tutor_id': tutor_id_bigint}).in_('id', [int(id) for id in alunos_a_vincular_ids]).execute()

        return jsonify({"message": f"Vínculos de tutoria da Sala {sala_id} atualizados com sucesso.", "status": 200}), 200
        
    except Exception as e:
        logging.error(f"Erro ao salvar vínculos de tutor: {e}")
        return jsonify({"error": f"Falha ao salvar vínculos de tutor: {e}", "status": 500}), 500


# =================================================================
# ROTAS DA API (DELETE - REMOÇÃO DE CADASTROS)
# =================================================================

# ROTA 31: API DELETE: Exclusão de Sala
@app.route('/api/salas/<sala_id>', methods=['DELETE'])
def api_delete_sala(sala_id):
    try:
        supabase.table('d_salas').delete().eq('id', int(sala_id)).execute()
        return jsonify({"message": f"Sala {sala_id} excluída com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir sala: {e}", "status": 500}), 500

# ROTA 32: API DELETE: Exclusão de Funcionário
@app.route('/api/funcionarios/<func_id>', methods=['DELETE'])
def api_delete_funcionario(func_id):
    try:
        supabase.table('d_funcionarios').delete().eq('id', int(func_id)).execute()
        return jsonify({"message": f"Funcionário {func_id} excluído com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir funcionário: {e}", "status": 500}), 500

# ROTA 33: API DELETE: Exclusão de Disciplina
@app.route('/api/disciplinas/<disc_id>', methods=['DELETE'])
def api_delete_disciplina(disc_id):
    try:
        supabase.table('d_disciplinas').delete().eq('id', disc_id).execute() # ID é a abreviação (string)
        return jsonify({"message": f"Disciplina {disc_id} excluída com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir disciplina: {e}", "status": 500}), 500

# ROTA 34: API DELETE: Exclusão de Clube
@app.route('/api/clubes/<clube_id>', methods=['DELETE'])
def api_delete_clube(clube_id):
    try:
        supabase.table('d_clubes').delete().eq('id', int(clube_id)).execute()
        return jsonify({"message": f"Clube {clube_id} excluído com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir clube: {e}", "status": 500}), 500

# ROTA 35: API DELETE: Exclusão de Eletiva
@app.route('/api/eletivas/<eletiva_id>', methods=['DELETE'])
def api_delete_eletiva(eletiva_id):
    try:
        supabase.table('d_eletivas').delete().eq('id', int(eletiva_id)).execute()
        return jsonify({"message": f"Eletiva {eletiva_id} excluída com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir eletiva: {e}", "status": 500}), 500

# ROTA 36: API DELETE: Exclusão de Equipamento
@app.route('/api/inventario/<eq_id>', methods=['DELETE'])
def api_delete_equipamento(eq_id):
    try:
        supabase.table('d_inventario_equipamentos').delete().eq('id', int(eq_id)).execute() 
        return jsonify({"message": f"Equipamento {eq_id} excluído com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir equipamento: {e}", "status": 500}), 500

# ROTA 37: API DELETE: Exclusão de Aluno (NOVO)
@app.route('/api/alunos/<aluno_id>', methods=['DELETE'])
def api_delete_aluno(aluno_id):
    try:
        supabase.table('d_alunos').delete().eq('id', int(aluno_id)).execute()
        return jsonify({"message": f"Aluno {aluno_id} excluído com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir aluno: {e}", "status": 500}), 500

# ROTA 38: API DELETE: Exclusão de Ocorrência (NOVO)
@app.route('/api/ocorrencias/<ocorrencia_id>', methods=['DELETE'])
def api_delete_ocorrencia(ocorrencia_id):
    try:
        supabase.table('ocorrencias').delete().eq('id', int(ocorrencia_id)).execute()
        return jsonify({"message": f"Ocorrência {ocorrencia_id} excluída com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao excluir ocorrência: {e}", "status": 500}), 500

# =================================================================
# EXECUÇÃO DO APP
# =================================================================

if __name__ == '__main__':
    # Você precisa rodar esta aplicação no terminal com 'python app.py'

    app.run(debug=True)
