import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
import json
from datetime import datetime

# =========================================================
# CONFIGURAÇÕES INICIAIS
# =========================================================

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("As variáveis SUPABASE_URL e SUPABASE_KEY devem ser configuradas no arquivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__, template_folder='templates')


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

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

def _to_bool(value):
    if value is True or value == 1:
        return True
    if value is False or value == 0 or value is None:
        return False
    s = str(value).strip().lower()
    if s in ('true', '1', 't', 'y', 'yes', 'sim'):
        return True
    if s in ('false', '0', 'f', 'n', 'no', 'nao', 'não'):
        return False
    return False

DEFAULT_AUTOTEXT = "ATENDIMENTO NÃO SOLICITADO PELO RESPONSÁVEL DA OCORRÊNCIA"


# =========================================================
# ROTAS DE PÁGINA PRINCIPAIS
# =========================================================

@app.route('/')
def home():
    return render_template('home.html')


# =========================================================
# OCORRÊNCIAS - REVISADO
# =========================================================

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

            # Preenche atendimento automático quando não solicitado
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

            # Atualiza status automaticamente no Supabase se necessário
            if item.get('status') != novo_status:
                update_fields['status'] = novo_status
                try:
                    supabase.table('ocorrencias').update(update_fields).eq('numero', numero).execute()
                    logging.info(f"[OCORRÊNCIA] Nº {numero} atualizada → {novo_status}")
                except Exception as e:
                    logging.error(f"Falha ao atualizar ocorrência {numero}: {e}")

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
        q = supabase.table('ocorrencias').select(
            "numero, data_hora, status, aluno_nome, tutor_nome, solicitado_tutor, solicitado_coordenacao, solicitado_gestao, atendimento_tutor, atendimento_coordenacao, atendimento_gestao, professor_id(nome), sala_id(sala)"
        ).order('data_hora', desc=True)

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
                try:
                    supabase.table('ocorrencias').update(update_fields).eq('numero', numero).execute()
                    logging.info(f"[OCORRÊNCIA] Nº {numero} atualizada → {novo_status}")
                except Exception as e:
                    logging.error(f"Falha ao atualizar ocorrência {numero}: {e}")

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


# =========================================================
# CORREÇÃO ROTA /api/alunos
# =========================================================

@app.route('/api/alunos', methods=['GET'])
def api_get_alunos_all():
    try:
        response = supabase.table('d_alunos').select('id, ra, nome, sala_id, tutor_id').order('nome').execute()
        alunos_raw = handle_supabase_response(response)
        alunos = []
        for a in alunos_raw:
            try:
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
            except Exception as inner_e:
                logging.warning(f"Erro ao processar aluno {a.get('nome')}: {inner_e}")
                continue
        return jsonify(alunos)
    except Exception as e:
        logging.exception("Erro /api/alunos")
        return jsonify({"error": f"Erro ao buscar todos os alunos: {e}", "status": 500}), 500


# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
