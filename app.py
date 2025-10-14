import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("As variáveis SUPABASE_URL e SUPABASE_KEY devem ser configuradas no arquivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__, template_folder='templates')

def handle_supabase_response(response):
    if not response:
        return []
    if hasattr(response, "data"):
        return response.data or []
    if isinstance(response, dict) and "data" in response:
        return response.get("data") or []
    return []

def formatar_data_hora(data_str):
    if not data_str:
        return 'N/A'
    try:
        dt_obj = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
        return dt_obj.strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return data_str

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gestao_aulas')
def gestao_aulas():
    return render_template('gestao_aulas.html')

@app.route('/gestao_agenda')
def gestao_agenda():
    return render_template('gestao_agenda.html')

@app.route('/gestao_plano_aula')
def gestao_plano_aula():
    return render_template('gestao_plano_aula.html')

@app.route('/gestao_guia_aprendizagem')
def gestao_guia_aprendizagem():
    return render_template('gestao_guia_aprendizagem.html')

@app.route('/gestao_ocorrencia')
def gestao_ocorrencia():
    return render_template('gestao_ocorrencia.html')

@app.route('/gestao_ocorrencia_nova')
def gestao_ocorrencia_nova():
    return render_template('gestao_ocorrencia_nova.html')

@app.route("/gestao_ocorrencia_abertas")
def gestao_ocorrencia_abertas():
    return render_template("gestao_ocorrencia_abertas.html")

@app.route("/gestao_ocorrencia_editar")
def gestao_ocorrencia_editar():
    return render_template("gestao_ocorrencia_editar.html")

@app.route('/gestao_ocorrencia_finalizadas')
def gestao_ocorrencia_finalizadas():
    return render_template('gestao_ocorrencia_finalizadas.html')

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

@app.route('/gestao_configuracoes')
def gestao_configuracoes():
    return render_template('gestao_configuracoes.html')

@app.route('/gestao_configuracoes_fluxo')
def gestao_configuracoes_fluxo():
    return render_template('gestao_configuracoes_fluxo.html')

@app.route('/gestao_configuracoes_sistema')
def gestao_configuracoes_sistema():
    return render_template('gestao_configuracoes_sistema.html')

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

@app.route('/api/salas', methods=['GET'])
def api_get_salas():
    try:
        response = supabase.table('d_salas').select('id, sala, nivel_ensino').order('sala').execute()
        salas = [{"id": str(s['id']), "nome": f"{s['sala']} ({s['nivel_ensino']})", "nivel_ensino": s['nivel_ensino']} for s in handle_supabase_response(response)]
        return jsonify(salas)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar salas: {e}", "status": 500}), 500

@app.route('/api/funcionarios', methods=['GET'])
def api_get_funcionarios():
    try:
        response = supabase.table('d_funcionarios').select('id, nome, funcao, is_tutor, email').order('nome').execute()
        funcionarios = [{"id": str(f['id']), "nome": f['nome'], "funcao": f.get('funcao', ''), "is_tutor": f.get('is_tutor', False), "email": f.get('email', '')} for f in handle_supabase_response(response)]
        return jsonify(funcionarios)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar funcionários: {e}", "status": 500}), 500

@app.route('/api/alunos_por_sala/<sala_id>', methods=['GET'])
def api_get_alunos_por_sala(sala_id):
    try:
        sala_id_bigint = int(sala_id)
        response_alunos = supabase.table('d_alunos').select('id, nome, tutor_id').eq('sala_id', sala_id_bigint).order('nome').execute()
        alunos_raw = handle_supabase_response(response_alunos)
        response_tutores = supabase.table('d_funcionarios').select('id, nome').eq('is_tutor', True).execute()
        tutores_raw = handle_supabase_response(response_tutores)
        tutores_dict = {str(t['id']): t['nome'] for t in tutores_raw}
        alunos = []
        for a in alunos_raw:
            tutor_id_str = str(a['tutor_id']) if a.get('tutor_id') else None
            tutor_nome = tutores_dict.get(tutor_id_str, 'Tutor Não Definido')
            alunos.append({
                "id": str(a['id']),
                "nome": a['nome'],
                "tutor_id": tutor_id_str,
                "tutor_nome": tutor_nome
            })
        return jsonify(alunos)
    except Exception as e:
        logging.error(f"Erro ao buscar alunos por sala: {e}")
        return jsonify({"error": f"Erro ao buscar alunos por sala: {e}", "status": 500}), 500

@app.route('/api/tutores', methods=['GET'])
def api_get_tutores():
    try:
        response = supabase.table('d_funcionarios').select('id, nome, email, funcao').eq('is_tutor', True).order('nome').execute()
        tutores_raw = handle_supabase_response(response)
        tutores = [{"id": str(t["id"]), "nome": t["nome"], "email": t.get("email", ""), "funcao": t.get("funcao", "")} for t in tutores_raw]
        return jsonify(tutores)
    except Exception as e:
        logging.error(f"Erro ao buscar tutores: {e}")
        return jsonify({"error": f"Erro ao buscar tutores: {e}", "status": 500}), 500

@app.route('/api/relatorio_frequencia')
def api_relatorio_frequencia():
    sala_id = request.args.get('salaId')
    aluno_id = request.args.get('alunoId')
    data_inicial = request.args.get('dataInicial')
    data_final = request.args.get('dataFinal')
    return jsonify({
        'presencas_percentual': 92,
        'faltas_totais': 5,
        'atrasos_totais': 2,
        'saidas_antecipadas_totais': 1
    })

@app.route('/api/frequencia/datas_registradas_por_sala/<int:sala_id>')
def api_datas_registradas(sala_id):
    try:
        resp = supabase.table('f_frequencia').select('data').eq('fk_sala_id', sala_id).order('data').execute()
        datas = sorted(list({r['data'] for r in handle_supabase_response(resp)}))
        return jsonify(datas)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar datas: {e}", "status": 500}), 500

@app.route('/api/alunos_por_tutor/<tutor_id>', methods=['GET'])
def api_get_alunos_por_tutor(tutor_id):
    try:
        tutor_id_bigint = int(tutor_id)
        response = supabase.table('d_alunos').select('id, nome').eq('tutor_id', tutor_id_bigint).order('nome').execute()
        alunos = [{"id": str(a['id']), "nome": a['nome']} for a in handle_supabase_response(response)]
        return jsonify(alunos)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar alunos por tutor: {e}", "status": 500}), 500

@app.route('/api/disciplinas', methods=['GET'])
def api_get_disciplinas():
    try:
        response = supabase.table('d_disciplinas').select('id, nome').order('nome').execute()
        disciplinas = handle_supabase_response(response)
        return jsonify(disciplinas)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar disciplinas: {e}", "status": 500}), 500

@app.route('/api/clubes', methods=['GET'])
def api_get_clubes():
    try:
        response = supabase.table('d_clubes').select('id, nome, semestre').order('semestre, nome').execute()
        clubes = handle_supabase_response(response)
        return jsonify(clubes)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar clubes: {e}", "status": 500}), 500

@app.route('/api/eletivas', methods=['GET'])
def api_get_eletivas():
    try:
        response = supabase.table('d_eletivas').select('id, nome, semestre').order('semestre, nome').execute()
        eletivas = handle_supabase_response(response)
        return jsonify(eletivas)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar eletivas: {e}", "status": 500}), 500

@app.route('/api/inventario', methods=['GET'])
def api_get_inventario():
    try:
        response = supabase.table('d_inventario_equipamentos').select('id, colmeia, equipamento_id, status').order('colmeia, equipamento_id').execute()
        inventario = handle_supabase_response(response)
        return jsonify(inventario)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar inventário: {e}", "status": 500}), 500

@app.route('/api/agendamentos_pendentes/<professor_id>', methods=['GET'])
def api_get_agendamentos_pendentes(professor_id):
    try:
        professor_id_bigint = int(professor_id)
        response = supabase.table('reservas_equipamentos').select('id, fk_sala_id, data_uso, periodo_uso, status, fk_professor_id').eq('fk_professor_id', professor_id_bigint).neq('status', 'FINALIZADO').execute()
        agendamentos_raw = handle_supabase_response(response)
        agendamentos = []
        for ag in agendamentos_raw:
            agendamentos.append({
                "id": str(ag['id']),
                "fk_sala_id": str(ag.get('fk_sala_id')),
                "data_uso": str(ag.get('data_uso')),
                "periodo_uso": ag.get('periodo_uso'),
                "status": ag.get('status')
            })
        return jsonify(agendamentos)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar agendamentos pendentes: {e}", "status": 500}), 500

def _to_bool(value):
    if value is True or value == 1:
        return True
    if value is False or value == 0 or value is None:
        return False
    s = str(value).strip().lower()
    if s in ('true', '1', 't', 'y', 'yes', 'sim'):
        return True
    if s in ('false', '0', 'f', 'n', 'no', 'nao', 'não', 'nao'):
        return False
    return False

DEFAULT_AUTOTEXT = "ATENDIMENTO NÃO SOLICITADO PELO RESPONSÁVEL DA OCORRÊNCIA"

@app.route('/api/ocorrencias_abertas', methods=['GET'])
def api_ocorrencias_abertas():
    try:
        resp = supabase.table('ocorrencias').select(
            "numero, data_hora, status, aluno_nome, tutor_nome, solicitado_tutor, solicitado_coordenacao, solicitado_gestao, atendimento_tutor, atendimento_coordenacao, atendimento_gestao, professor_id(nome), sala_id(sala)"
        ).order('data_hora', desc=True).execute()
        items = resp.data or []
        abertas = []
        for item in items:
            numero = item.get('numero')
            update_fields = {}
            st = _to_bool(item.get('solicitado_tutor'))
            sc = _to_bool(item.get('solicitado_coordenacao'))
            sg = _to_bool(item.get('solicitado_gestao'))
            at_tutor = (item.get('atendimento_tutor') or "").strip()
            at_coord = (item.get('atendimento_coordenacao') or "").strip()
            at_gest = (item.get('atendimento_gestao') or "").strip()
            if not st and at_tutor == "":
                at_tutor = DEFAULT_AUTOTEXT
                update_fields['atendimento_tutor'] = at_tutor
            if not sc and at_coord == "":
                at_coord = DEFAULT_AUTOTEXT
                update_fields['atendimento_coordenacao'] = at_coord
            if not sg and at_gest == "":
                at_gest = DEFAULT_AUTOTEXT
                update_fields['atendimento_gestao'] = at_gest
            pendente_tutor = st and (at_tutor == "")
            pendente_coord = sc and (at_coord == "")
            pendente_gestao = sg and (at_gest == "")
            # Linha corrigida (antes era a linha 460 que estava com o walrus operator no seu deploy)
            novo_status = "Aberta" if (pendente_tutor or pendente_coord or pendente_gestao) else "Finalizada"
            if item.get('status') != novo_status:
                update_fields['status'] = novo_status
            if update_fields:
                try:
                    supabase.table('ocorrencias').update(update_fields).eq('numero', numero).execute()
                except Exception:
                    pass
            if novo_status == "Aberta":
                abertas.append({
                    "numero": numero,
                    "data_hora": formatar_data_hora(item.get('data_hora')),
                    "aluno_nome": item.get('aluno_nome', 'N/A'),
                    "tutor_nome": item.get('tutor_nome', 'N/A'),
                    "professor_nome": (item.get('professor_id') or {}).get('nome', 'N/A'),
                    "sala_nome": (item.get('sala_id') or {}).get('sala', 'N/A'),
                    "status": novo_status,
                    "solicitado_tutor": st,
                    "solicitado_coordenacao": sc,
                    "solicitado_gestao": sg,
                    "atendimento_tutor": at_tutor,
                    "atendimento_coordenacao": at_coord,
                    "atendimento_gestao": at_gest
                })
        return jsonify(abertas), 200
    except Exception as e:
        logging.exception("Erro /api/ocorrencias_abertas")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ocorrencias_finalizadas', methods=['GET'])
def api_ocorrencias_finalizadas():
    try:
        sala = request.args.get('sala')
        aluno = request.args.get('aluno')
        q = supabase.table('ocorrencias').select(
            "numero, data_hora, status, aluno_nome, tutor_nome, solicitado_tutor, solicitado_coordenacao, solicitado_gestao, atendimento_tutor, atendimento_coordenacao, atendimento_gestao, professor_id(nome), sala_id(sala)"
        ).order('data_hora', desc=True)
        if sala:
            q = q.eq('sala_id', sala)
        if aluno:
            q = q.eq('aluno_id', aluno)
        resp = q.execute()
        items = resp.data or []
        finalizadas = []
        for item in items:
            numero = item.get('numero')
            update_fields = {}
            st = _to_bool(item.get('solicitado_tutor'))
            sc = _to_bool(item.get('solicitado_coordenacao'))
            sg = _to_bool(item.get('solicitado_gestao'))
            at_tutor = (item.get('atendimento_tutor') or "").strip()
            at_coord = (item.get('atendimento_coordenacao') or "").strip()
            at_gest = (item.get('atendimento_gestao') or "").strip()
            if not st and at_tutor == "":
                at_tutor = DEFAULT_AUTOTEXT
                update_fields['atendimento_tutor'] = at_tutor
            if not sc and at_coord == "":
                at_coord = DEFAULT_AUTOTEXT
                update_fields['atendimento_coordenacao'] = at_coord
            if not sg and at_gest == "":
                at_gest = DEFAULT_AUTOTEXT
                update_fields['atendimento_gestao'] = at_gest
            pendente_tutor = st and (at_tutor == "")
            pendente_coord = sc and (at_coord == "")
            pendente_gestao = sg and (at_gest == "")
            novo_status = "Aberta" if (pendente_tutor or pendente_coord or pendente_gestao) else "Finalizada"
            if item.get('status') != novo_status:
                update_fields['status'] = novo_status
            if update_fields:
                try:
                    supabase.table('ocorrencias').update(update_fields).eq('numero', numero).execute()
                except Exception:
                    pass
            if novo_status == "Finalizada":
                finalizadas.append({
                    "numero": numero,
                    "data_hora": formatar_data_hora(item.get('data_hora')),
                    "aluno_nome": item.get('aluno_nome', 'N/A'),
                    "tutor_nome": item.get('tutor_nome', 'N/A'),
                    "professor_nome": (item.get('professor_id') or {}).get('nome', 'N/A'),
                    "sala_nome": (item.get('sala_id') or {}).get('sala', 'N/A'),
                    "status": novo_status,
                    "solicitado_tutor": st,
                    "solicitado_coordenacao": sc,
                    "solicitado_gestao": sg,
                    "atendimento_tutor": at_tutor,
                    "atendimento_coordenacao": at_coord,
                    "atendimento_gestao": at_gest
                })
        return jsonify(finalizadas), 200
    except Exception as e:
        logging.exception("Erro /api/ocorrencias_finalizadas")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ocorrencias_todas')
def api_ocorrencias_todas():
    try:
        response = supabase.table('ocorrencias').select('*').order('data_hora', desc=True).execute()
        return jsonify(handle_supabase_response(response))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/salas_com_ocorrencias')
def get_salas_com_ocorrencias():
    try:
        ocorrencias = supabase.table('ocorrencias').select('sala_id').execute()
        sala_ids = list({o['sala_id'] for o in ocorrencias.data if o.get('sala_id')})
        salas = supabase.table('d_salas').select('id, sala').in_('id', sala_ids).execute()
        return jsonify(handle_supabase_response(salas))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/alunos_com_ocorrencias_por_sala/<int:sala_id>')
def get_alunos_com_ocorrencias_por_sala(sala_id):
    try:
        ocorrencias = supabase.table('ocorrencias').select('aluno_id').eq('sala_id', sala_id).execute()
        aluno_ids = list({o['aluno_id'] for o in ocorrencias.data if o.get('aluno_id')})
        alunos = supabase.table('d_alunos').select('id, nome').in_('id', aluno_ids).execute()
        return jsonify(handle_supabase_response(alunos))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/relatorio_ocorrencias')
def get_relatorio_ocorrencias():
    try:
        sala_id = request.args.get('salaId')
        aluno_id = request.args.get('alunoId')
        data_inicial = request.args.get('dataInicial')
        data_final = request.args.get('dataFinal')
        query = supabase.table('ocorrencias').select('*, aluno_id(nome)').order('data_hora')
        if sala_id:
            query = query.eq('sala_id', int(sala_id))
        if aluno_id:
            query = query.eq('aluno_id', int(aluno_id))
        if data_inicial:
            query = query.gte('data_hora', data_inicial)
        if data_final:
            query = query.lte('data_hora', data_final)
        resp = query.execute()
        return jsonify(handle_supabase_response(resp))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ocorrencias', methods=['GET'])
@app.route('/api/ocorrencias/<ocorrencia_id>', methods=['GET'])
def api_get_ocorrencias(ocorrencia_id=None):
    try:
        select_query_detail = "numero, data_hora, descricao, atendimento_professor, atendimento_tutor, atendimento_coordenacao, atendimento_gestao, dt_atendimento_tutor, dt_atendimento_coordenacao, dt_atendimento_gestao, aluno_nome, tutor_nome, professor_id(nome), sala_id(sala)"
        if ocorrencia_id:
            response = supabase.table('ocorrencias').select(select_query_detail).eq('numero', int(ocorrencia_id)).single().execute()
            data = handle_supabase_response(response)
            if data and isinstance(data, dict):
                data['id'] = data.get('numero')
                data['professor_nome'] = data.get('professor_id', {}).get('nome', 'N/A')
                data['sala_nome'] = data.get('sala_id', {}).get('sala', 'N/A')
                if 'professor_id' in data:
                    del data['professor_id']
                if 'sala_id' in data:
                    del data['sala_id']
            return jsonify(data), 200
        else:
            response = supabase.table('ocorrencias').select('*').order('data_hora', desc=True).execute()
            return jsonify(handle_supabase_response(response)), 200
    except Exception as e:
        logging.error(f"Erro ao buscar ocorrência de detalhe: {e}")
        return jsonify({"error": f"Falha ao buscar detalhes: {e}", "status": 500}), 500

@app.route('/api/alunos', methods=['GET'])
def api_get_alunos_all():
    try:
        response = supabase.table('d_alunos').select('id, ra, nome, sala_id, tutor_id').order('nome').execute()
        alunos_raw = handle_supabase_response(response)
        alunos = []
        for a in alunos_raw:
            sala_nome = None
            tutor_nome = None
            if a.get('sala_id'):
                sala_resp = supabase.table('d_salas').select('sala').eq('id', a['sala_id']).single().execute()
                sala_data = handle_supabase_response(sala_resp)
                sala_nome = sala_data.get('sala') if isinstance(sala_data, dict) else None
            if a.get('tutor_id'):
                tut_resp = supabase.table('d_funcionarios').select('nome').eq('id', a['tutor_id']).single().execute()
                tut_data = handle_supabase_response(tut_resp)
                tutor_nome = tut_data.get('nome') if isinstance(tut_data, dict) else None
            alunos.append({
                "id": str(a.get('id')),
                "ra": a.get('ra'),
                "nome": a.get('nome'),
                "sala_nome": sala_nome or 'N/A',
                "tutor_nome": tutor_nome or 'Não Vinculado'
            })
        return jsonify(alunos)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar todos os alunos: {e}", "status": 500}), 500

@app.route('/api/vinculacoes_disciplinas/<sala_id>', methods=['GET'])
def api_get_vinculacoes_disciplinas(sala_id):
    try:
        sala_id_bigint = int(sala_id)
        response = supabase.table('vinculos_disciplina_sala').select('fk_disciplina_id').eq('fk_sala_id', sala_id_bigint).execute()
        vinculos_raw = handle_supabase_response(response)
        disciplinas_ids = [v['fk_disciplina_id'] for v in vinculos_raw]
        return jsonify({"sala_id": sala_id, "disciplinas": disciplinas_ids})
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar vínculos de disciplinas: {e}", "status": 500}), 500

@app.route('/api/horarios_fixos/<nivel_ensino>', methods=['GET'])
def api_get_horarios_fixos(nivel_ensino):
    try:
        response = supabase.table('d_horarios_fixos').select('*').eq('nivel_ensino', nivel_ensino).order('dia_semana').execute()
        horarios = handle_supabase_response(response)
        return jsonify(horarios)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar horários fixos: {e}", "status": 500}), 500

@app.route('/api/agenda_semanal', methods=['GET'])
def api_get_agenda_semanal():
    sala_id = request.args.get('sala_id')
    data_referencia = request.args.get('data_referencia')
    if not sala_id or not data_referencia:
        return jsonify({"error": "Parâmetros sala_id e data_referencia são obrigatórios.", "status": 400}), 400
    try:
        response = supabase.table('f_agenda_aulas').select('id, dia_semana, ordem_aula, tema_aula, tipo_aula, fk_disciplina_id, fk_professor_id').eq('fk_sala_id', int(sala_id)).eq('data_referencia', data_referencia).execute()
        agenda_raw = handle_supabase_response(response)
        agenda = []
        for item in agenda_raw:
            disc_nome = None
            prof_nome = None
            if item.get('fk_disciplina_id'):
                dresp = supabase.table('d_disciplinas').select('nome').eq('id', item['fk_disciplina_id']).single().execute()
                ddata = handle_supabase_response(dresp)
                disc_nome = ddata.get('nome') if isinstance(ddata, dict) else None
            if item.get('fk_professor_id'):
                presp = supabase.table('d_funcionarios').select('nome').eq('id', item['fk_professor_id']).single().execute()
                pdata = handle_supabase_response(presp)
                prof_nome = pdata.get('nome') if isinstance(pdata, dict) else None
            agenda.append({
                "id": str(item.get('id')),
                "dia_semana": item.get('dia_semana'),
                "ordem_aula": item.get('ordem_aula'),
                "tema_aula": item.get('tema_aula'),
                "tipo_aula": item.get('tipo_aula'),
                "disciplina_nome": disc_nome,
                "professor_nome": prof_nome
            })
        return jsonify(agenda)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar agenda semanal: {e}", "status": 500}), 500

@app.route('/api/guia_aprendizagem', methods=['GET'])
def api_get_guia_aprendizagem():
    disciplina_id = request.args.get('disciplina_id')
    bimestre = request.args.get('bimestre')
    serie = request.args.get('serie')
    if not disciplina_id or not bimestre or not serie:
        return jsonify({"error": "Parâmetros disciplina, bimestre e série são obrigatórios.", "status": 400}), 400
    try:
        response = supabase.table('f_guia_aprendizagem').select('*').eq('fk_disciplina_id', disciplina_id).eq('bimestre', int(bimestre)).eq('serie', serie).execute()
        guia = handle_supabase_response(response)
        if guia and isinstance(guia, list) and guia[0].get('habilidades_planejadas'):
            guia[0]['habilidades_planejadas'] = json.dumps(guia[0]['habilidades_planejadas'])
        return jsonify(guia)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar Guia de Aprendizagem: {e}", "status": 500}), 500


@app.route('/api/cadastrar_sala', methods=['POST'])
def api_cadastrar_sala():
    data = request.json
    sala = data.get('sala')
    nivel_ensino = data.get('nivel_ensino')
    if not sala or not nivel_ensino:
        return jsonify({"error": "Nome da sala e nível de ensino são obrigatórios.", "status": 400}), 400
    try:
        nova_sala = {"sala": sala, "nivel_ensino": nivel_ensino}
        response = supabase.table('d_salas').insert(nova_sala).execute()
        handle_supabase_response(response)
        return jsonify({"message": f"Sala {sala} cadastrada com sucesso!", "status": 201}), 201
    except Exception as e:
        if "unique constraint" in str(e):
            return jsonify({"error": f"Erro: A sala '{sala}' já existe. Não foi cadastrada.", "status": 409}), 409
        logging.error(f"Erro no Supabase durante o cadastro de sala: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

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
            "id": data.get('id') if 'id' in data else None,
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

@app.route('/api/cadastrar_clube', methods=['POST'])
def api_cadastrar_clube():
    data = request.json
    nome = data.get('nome')
    semestre = data.get('semestre')
    if not nome or not semestre:
        return jsonify({"error": "Nome do clube e semestre são obrigatórios.", "status": 400}), 400
    try:
        novo_clube = {"nome": nome, "semestre": semestre}
        response = supabase.table('d_clubes').insert(novo_clube).execute()
        handle_supabase_response(response)
        return jsonify({"message": f"Clube '{nome}' cadastrado com sucesso!", "status": 201}), 201
    except Exception as e:
        if "unique constraint" in str(e):
            return jsonify({"error": f"Erro: Clube '{nome}' já existe neste semestre.", "status": 409}), 409
        return jsonify({"error": f"Falha ao cadastrar clube: {e}", "status": 500}), 500

@app.route('/api/cadastrar_eletiva', methods=['POST'])
def api_cadastrar_eletiva():
    data = request.json
    nome = data.get('nome')
    semestre = data.get('semestre')
    if not nome or not semestre:
        return jsonify({"error": "Nome da eletiva e semestre são obrigatórios.", "status": 400}), 400
    try:
        nova_eletiva = {"nome": nome, "semestre": semestre}
        response = supabase.table('d_eletivas').insert(nova_eletiva).execute()
        handle_supabase_response(response)
        return jsonify({"message": f"Eletiva '{nome}' cadastrada com sucesso!", "status": 201}), 201
    except Exception as e:
        if "unique constraint" in str(e):
            return jsonify({"error": f"Erro: Eletiva '{nome}' já existe neste semestre.", "status": 409}), 409
        return jsonify({"error": f"Falha ao cadastrar eletiva: {e}", "status": 500}), 500

@app.route('/api/cadastrar_equipamento', methods=['POST'])
def api_cadastrar_equipamento():
    data = request.json
    colmeia = data.get('colmeia')
    equipamento_id = data.get('equipamento_id')
    if not colmeia or not equipamento_id:
        return jsonify({"error": "Colmeia e ID do equipamento são obrigatórios.", "status": 400}), 400
    try:
        novo_equipamento = {"colmeia": colmeia, "equipamento_id": int(equipamento_id), "status": "DISPONÍVEL"}
        response = supabase.table('d_inventario_equipamentos').insert(novo_equipamento).execute()
        handle_supabase_response(response)
        return jsonify({"message": f"Equipamento {equipamento_id} da {colmeia} cadastrado com sucesso!", "status": 201}), 201
    except Exception as e:
        if "unique constraint" in str(e):
            return jsonify({"error": f"Erro: O Equipamento {equipamento_id} na {colmeia} já existe.", "status": 409}), 409
        return jsonify({"error": f"Falha ao cadastrar equipamento: {e}", "status": 500}), 500

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
        novo_aluno = {"ra": ra, "nome": nome, "sala_id": sala_id_bigint, "tutor_id": tutor_id_bigint}
        response = supabase.table('d_alunos').insert(novo_aluno).execute()
        handle_supabase_response(response)
        return jsonify({"message": f"Aluno(a) {nome} (RA: {ra}) cadastrado com sucesso!", "status": 201}), 201
    except Exception as e:
        if "unique constraint" in str(e):
            return jsonify({"error": f"Erro: O RA '{ra}' já está cadastrado no sistema.", "status": 409}), 409
        logging.error(f"Erro no Supabase durante o cadastro de aluno: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

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
            status = item.get('status')
            registro = {
                "fk_aluno_id": aluno_id_bigint,
                "fk_sala_id": sala_id_bigint,
                "data": item.get('data'),
                "status": status
            }
            if status and status.upper() in ('PA', 'ATRASO', 'PRESENTE_ATRASADO'):
                registro['hora_atraso'] = item.get('hora') or item.get('hora_registro')
                registro['motivo_atraso'] = item.get('motivo')
                registro['responsavel_atraso'] = item.get('responsavel')
                registro['telefone_atraso'] = item.get('telefone')
            elif status and status.upper() in ('PS', 'SAIDA', 'SAIDA_ANTECIPADA'):
                registro['hora_saida'] = item.get('hora') or item.get('hora_registro')
                registro['motivo_saida'] = item.get('motivo')
                registro['responsavel_saida'] = item.get('responsavel')
                registro['telefone_saida'] = item.get('telefone')
            registros_a_inserir.append(registro)
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
            "hora_atraso": data['hora'],
            "motivo_atraso": data['motivo'],
            "status": "PA",
            "responsavel_atraso": data.get('responsavel'),
            "telefone_atraso": data.get('telefone')
        }
        response = supabase.table('f_frequencia').insert(registro).execute()
        handle_supabase_response(response)
        return jsonify({"message": "Registro de Atraso salvo com sucesso!", "status": 201}), 201
    except Exception as e:
        if "unique constraint" in str(e):
            return jsonify({"error": "Erro: Já existe um registro de frequência para este aluno na data.", "status": 409}), 409
        logging.error(f"Erro no Supabase ao salvar atraso: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

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
            "hora_saida": data['hora'],
            "motivo_saida": data['motivo'],
            "status": "PS",
            "responsavel_saida": data.get('responsavel'),
            "telefone_saida": data.get('telefone')
        }
        response = supabase.table('f_frequencia').insert(registro).execute()
        handle_supabase_response(response)
        return jsonify({"message": "Registro de Saída Antecipada salvo com sucesso!", "status": 201}), 201
    except Exception as e:
        if "unique constraint" in str(e):
            return jsonify({"error": "Erro: Já existe um registro de frequência para este aluno na data.", "status": 409}), 409
        logging.error(f"Erro no Supabase ao salvar saída: {e}")
        return jsonify({"error": f"Erro interno do servidor: {e}", "status": 500}), 500

@app.route('/api/registrar_ocorrencia', methods=['POST'])
def api_registrar_ocorrencia():
    data = request.json
    try:
        prof_id_bigint = int(data.get('prof_id')) if data.get('prof_id') else None
        aluno_id_bigint = int(data.get('aluno_id')) if data.get('aluno_id') else None
        sala_id_bigint = int(data.get('sala_id')) if data.get('sala_id') else None
    except ValueError:
        prof_id_bigint, aluno_id_bigint, sala_id_bigint = None, None, None
    descricao = data.get('descricao')
    atendimento_professor = data.get('atendimento_professor')
    if not prof_id_bigint or not aluno_id_bigint or not sala_id_bigint or not descricao or not atendimento_professor:
        return jsonify({"error": "Dados obrigatórios (Professor, Aluno, Sala, Descrição e Atendimento Professor) são necessários.", "status": 400}), 400
    try:
        nova_ocorrencia = {
            "professor_id": prof_id_bigint,
            "aluno_id": aluno_id_bigint,
            "sala_id": sala_id_bigint,
            "data_hora": "now()",
            "descricao": descricao,
            "atendimento_professor": atendimento_professor,
            "aluno_nome": data.get('aluno_nome'),
            "tutor_nome": data.get('tutor_nome'),
            "tipo": data.get('tipo', 'Comportamental'),
            "status": "Aberta",
            "solicitado_tutor": data.get('solicitar_tutor', False),
            "solicitado_coordenacao": data.get('solicitar_coordenacao', False),
            "solicitado_gestao": data.get('solicitar_gestao', False),
        }
        response = supabase.table('ocorrencias').insert(nova_ocorrencia).execute()
        handle_supabase_response(response)
        return jsonify({"message": "Ocorrência registrada com sucesso! Aguardando atendimento.", "status": 201}), 201
    except Exception as e:
        logging.error(f"Erro no Supabase ao registrar ocorrência: {e}")
        return jsonify({"error": f"Falha ao registrar ocorrência: {e}", "status": 500}), 500

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

@app.route('/api/salvar_parametros', methods=['POST'])
def api_salvar_parametros():
    data = request.json
    if not data:
        return jsonify({"error": "Nenhum parâmetro enviado.", "status": 400}), 400
    try:
        updates = []
        for key, value in data.items():
            updates.append({"parametro": key, "valor": value})
        response = supabase.table('cfg_parametros').upsert(updates, on_conflict='parametro').execute()
        handle_supabase_response(response)
        return jsonify({"message": "Parâmetros de configuração salvos com sucesso!", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao salvar configurações: {e}", "status": 500}), 500

@app.route('/api/salvar_agenda', methods=['POST'])
def api_salvar_agenda():
    data = request.json
    registros = data.get('registros')
    if not registros or not isinstance(registros, list):
        return jsonify({"error": "Nenhum registro de agenda válido enviado.", "status": 400}), 400
    try:
        registros_a_salvar = []
        for item in registros:
            disciplina_id = item['fk_disciplina_id']
            registros_a_salvar.append({
                "fk_sala_id": int(item['fk_sala_id']),
                "fk_professor_id": int(item['fk_professor_id']),
                "data_referencia": item['data_referencia'],
                "dia_semana": item['dia_semana'],
                "ordem_aula": int(item['ordem_aula']),
                "fk_disciplina_id": disciplina_id,
                "tema_aula": item['tema_aula'],
                "tipo_aula": item['tipo_aula'],
            })
        response = supabase.table('f_agenda_aulas').upsert(registros_a_salvar, on_conflict='fk_sala_id, data_referencia, dia_semana, ordem_aula').execute()
        handle_supabase_response(response)
        return jsonify({"message": f"{len(registros_a_salvar)} registros de agenda salvos/atualizados com sucesso!", "status": 200}), 200
    except Exception as e:
        logging.error(f"Erro ao salvar agenda: {e}")
        return jsonify({"error": f"Falha ao salvar agenda: {e}", "status": 500}), 500

@app.route('/api/atualizar_ocorrencia/<ocorrencia_id>', methods=['PUT'])
def api_atualizar_ocorrencia(ocorrencia_id):
    data = request.json
    if not data:
        return jsonify({"error": "Nenhum dado de atualização enviado.", "status": 400}), 400
    try:
        ocorrencia_id_bigint = int(ocorrencia_id)
        response = supabase.table('ocorrencias').update(data).eq('numero', ocorrencia_id_bigint).execute()
        handle_supabase_response(response)
        return jsonify({"message": "Ocorrência atualizada com sucesso.", "status": 200}), 200
    except Exception as e:
        return jsonify({"error": f"Falha ao atualizar ocorrência: {e}", "status": 500}), 500

@app.route('/api/finalizar_retirada_equipamento', methods=['POST'])
def api_finalizar_retirada_equipamento():
    data = request.json
    agendamento_id = data.get('agendamento_id')
    vinculacoes = data.get('vinculacoes')
    status_agendamento = data.get('status_agendamento')
    if not agendamento_id or not status_agendamento:
        return jsonify({"error": "ID do agendamento e Status são obrigatórios.", "status": 400}), 400
    try:
        update_data = {"status": status_agendamento, "data_retirada_geral": data.get('data_retirada_geral'), "termo_aceite_registro": data.get('termo_aceite_registro')}
        supabase.table('reservas_equipamentos').update(update_data).eq('id', agendamento_id).execute()
        if vinculacoes:
            registros = []
            for v in vinculacoes:
                registros.append({
                    "fk_agendamento_id": int(agendamento_id),
                    "fk_aluno_id": int(v['aluno_id']),
                    "equipamento_id": v['equipamento_id'],
                    "data_retirada": v['data_retirada']
                })
            if registros:
                supabase.table('rastreamento_equipamento').insert(registros).execute()
        return jsonify({"message": f"Retirada do agendamento {agendamento_id} finalizada e equipamentos vinculados!", "status": 200}), 200
    except Exception as e:
        logging.error(f"Erro ao finalizar retirada: {e}")
        return jsonify({"error": f"Erro interno ao finalizar retirada: {e}", "status": 500}), 500

@app.route('/api/finalizar_devolucao_equipamento', methods=['POST'])
def api_finalizar_devolucao_equipamento():
    data = request.json
    agendamento_id = data.get('agendamento_id')
    if not agendamento_id:
        return jsonify({"error": "ID do agendamento é obrigatório.", "status": 400}), 400
    try:
        update_data = {"status": "FINALIZADO", "data_devolucao": data.get('data_devolucao', 'now()')}
        supabase.table('reservas_equipamentos').update(update_data).eq('id', agendamento_id).execute()
        return jsonify({"message": f"Devolução do agendamento {agendamento_id} finalizada com sucesso!", "status": 200}), 200
    except Exception as e:
        logging.error(f"Erro ao finalizar devolução: {e}")
        return jsonify({"error": f"Erro interno ao finalizar devolução: {e}", "status": 500}), 500

@app.route('/api/vincular_disciplina_sala', methods=['POST'])
def api_vincular_disciplina_sala():
    data = request.json
    sala_id = data.get('sala_id')
    disciplinas_ids = data.get('disciplinas')
    if not sala_id:
        return jsonify({"error": "ID da sala é obrigatório.", "status": 400}), 400
    try:
        sala_id_bigint = int(sala_id)
        supabase.table('vinculos_disciplina_sala').delete().eq('fk_sala_id', sala_id_bigint).execute()
        if disciplinas_ids:
            registros = [{"fk_sala_id": sala_id_bigint, "fk_disciplina_id": d_id} for d_id in disciplinas_ids]
            supabase.table('vinculos_disciplina_sala').insert(registros).execute()
        return jsonify({"message": f"Vínculos da sala {sala_id} atualizados com sucesso.", "status": 200}), 200
    except Exception as e:
        logging.error(f"Erro ao salvar vínculos de disciplina: {e}")
        return jsonify({"error": f"Falha ao salvar vínculos de disciplina: {e}", "status": 500}), 500

@app.route('/api/vincular_tutor_aluno', methods=['POST'])
def api_vincular_tutor_aluno():
    data = request.json
    tutor_id = data.get('tutor_id')
    vinculos = data.get('vinculos')
    if not tutor_id or not vinculos:
        return jsonify({"error": "Dados de tutor e vínculos são obrigatórios.", "status": 400}), 400
    try:
        tutor_id_bigint = int(tutor_id)
        alunos_a_vincular_ids = [int(v['aluno_id']) for v in vinculos]
        sala_id = int(vinculos[0]['sala_id'])
        alunos_na_sala_raw = supabase.table('d_alunos').select('id').eq('sala_id', sala_id).execute()
        alunos_na_sala_ids = [int(a['id']) for a in handle_supabase_response(alunos_na_sala_raw)]
        alunos_a_desvincular_ids = [a_id for a_id in alunos_na_sala_ids if a_id not in alunos_a_vincular_ids]
        if alunos_a_desvincular_ids:
            supabase.table('d_alunos').update({'tutor_id': None}).in_('id', alunos_a_desvincular_ids).execute()
        for v in vinculos:
            supabase.table('d_alunos').update({'tutor_id': tutor_id_bigint}).eq('id', int(v['aluno_id'])).execute()
        return jsonify({"message": "Vínculos atualizados com sucesso.", "status": 200}), 200
    except Exception as e:
        logging.error(f"Erro ao vincular tutor/aluno: {e}")
        return jsonify({"error": f"Falha ao vincular tutor/aluno: {e}", "status": 500}), 500

@app.route('/api/ocorrencia_detalhes')
def ocorrencia_detalhes():
    try:
        numero = request.args.get('numero')
        if not numero:
            return jsonify({'error': 'Número da ocorrência não fornecido'}), 400

        # Busca a ocorrência principal
        dados = supabase.table('ocorrencias').select('*').eq('numero', numero).single().execute()
        ocorrencia = dados.data

        if not ocorrencia:
            return jsonify({'error': 'Ocorrência não encontrada'}), 404

        # Inicializa nomes vazios
        professor_nome = None
        sala_nome = None

        # Busca o nome do professor (se tiver ID)
        if ocorrencia.get('professor_id'):
            prof = supabase.table('professores').select('nome').eq('id', ocorrencia['professor_id']).single().execute()
            if prof.data:
                professor_nome = prof.data['nome']

        # Busca o nome da sala (se tiver ID)
        if ocorrencia.get('sala_id'):
            sala = supabase.table('salas').select('nome').eq('id', ocorrencia['sala_id']).single().execute()
            if sala.data:
                sala_nome = sala.data['nome']

        # Monta resposta completa com nomes legíveis
        resposta = {
            'numero': ocorrencia.get('numero'),
            'aluno_nome': ocorrencia.get('aluno_nome'),
            'descricao': ocorrencia.get('descricao'),
            'status': ocorrencia.get('status'),
            'atendimento_professor': ocorrencia.get('atendimento_professor'),
            'atendimento_tutor': ocorrencia.get('atendimento_tutor'),
            'atendimento_coordenacao': ocorrencia.get('atendimento_coordenacao'),
            'atendimento_gestao': ocorrencia.get('atendimento_gestao'),
            'tutor_nome': ocorrencia.get('tutor_nome'),
            'professor_nome': professor_nome,
            'sala_nome': sala_nome
        }

        return jsonify(resposta)

    except Exception as e:
        print('Erro ao buscar detalhes da ocorrência:', e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/registrar_atendimento', methods=['POST'])
def registrar_atendimento():
    try:
        dados = request.get_json()
        numero = dados.get('numero')
        nivel = dados.get('nivel')
        texto = dados.get('texto')

        if not numero or not nivel or not texto:
            return jsonify({'error': 'Campos obrigatórios ausentes'}), 400

        campo = f'atendimento_{nivel}'
        supabase.table('ocorrencias').update({campo: texto}).eq('numero', numero).execute()

        return jsonify({'success': True, 'message': 'Atendimento salvo com sucesso'})

    except Exception as e:
        print('Erro ao registrar atendimento:', e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))



