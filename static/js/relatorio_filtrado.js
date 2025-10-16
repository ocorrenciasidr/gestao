document.addEventListener('DOMContentLoaded', function() {
    carregarSalas();

    document.getElementById('sala').addEventListener('change', carregarAlunos);
    document.getElementById('btn-carregar-ocorrencias').addEventListener('click', carregarOcorrencias);

    async function carregarSalas() {
        let salaSelect = document.getElementById('sala');
        salaSelect.innerHTML = '<option value="">Carregando...</option>';
        const resp = await fetch('/api/salas_com_ocorrencias');
        const salas = await resp.json();
        salaSelect.innerHTML = '<option value="">Selecione...</option>';
        salas.forEach(s => {
            salaSelect.innerHTML += `<option value="${s.id}">${s.nome}</option>`;
        });
        document.getElementById('aluno').innerHTML = '<option value="">Selecione a sala primeiro</option>';
    }

    async function carregarAlunos() {
        let salaId = document.getElementById('sala').value;
        let alunoSelect = document.getElementById('aluno');
        if(!salaId) {
            alunoSelect.innerHTML = '<option value="">Selecione a sala primeiro</option>';
            return;
        }
        alunoSelect.innerHTML = '<option value="">Carregando...</option>';
        const resp = await fetch(`/api/alunos_com_ocorrencias_por_sala/${salaId}`);
        const alunos = await resp.json();
        alunoSelect.innerHTML = '<option value="">Selecione...</option>';
        alunos.forEach(a => {
            alunoSelect.innerHTML += `<option value="${a.id}">${a.nome}</option>`;
        });
    }

    async function carregarOcorrencias() {
        let alunoId = document.getElementById('aluno').value;
        let area = document.getElementById('area-ocorrencias');
        area.innerHTML = '';
        if(!alunoId) {
            area.innerHTML = '<p class="text-red-400">Selecione o aluno.</p>';
            return;
        }
        area.innerHTML = 'Carregando ocorrências...';
        const resp = await fetch(`/api/ocorrencias_por_aluno/${alunoId}`);
        const ocorrencias = await resp.json();
        if(!ocorrencias || ocorrencias.length === 0) {
            area.innerHTML = '<p class="text-yellow-400">Nenhuma ocorrência encontrada para o aluno.</p>';
            return;
        }
        // Lista com checkbox
        let alunoNome = ocorrencias[0]?.aluno_nome || '';
        let html = `<h3 class="text-lg mb-2">Ocorrências de <b>${alunoNome}</b></h3>
            <form id="form-ocorrencias">
            <ul class="mb-4">`;
        ocorrencias.forEach(o => {
            html += `<li class="mb-2">
                <label>
                    <input type="checkbox" name="ocorrencia" value="${o.numero}" class="checkbox-ocorrencia mr-2">
                    <b>Nº ${o.numero}</b> - ${o.data_hora} (${o.status})<br>
                    <span class="text-sm">${o.descricao}</span>
                </label>
            </li>`
        });
        html += '</ul>';
        html += `<button type="submit" class="px-4 py-2 rounded bg-green-600 text-white hover:bg-green-700">Gerar PDF</button>
            </form>`;
        area.innerHTML = html;

        document.getElementById('form-ocorrencias').onsubmit = async function(ev) {
            ev.preventDefault();
            let selecionadas = Array.from(document.querySelectorAll('.checkbox-ocorrencia:checked')).map(x => x.value);
            if(selecionadas.length === 0){
                alert('Selecione ao menos uma ocorrência!');
                return;
            }
            // POST para gerar PDF
            const res = await fetch('/api/gerar_pdf_ocorrencias', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({numeros: selecionadas})
            });
            if(res.ok) {
                // Recebe o PDF como blob
                const blob = await res.blob();
                // Download com nome do aluno
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${alunoNome.replace(/\s/g,'_')}_ocorrencias.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                // Desabilitar checkboxes
                document.querySelectorAll('.checkbox-ocorrencia').forEach(cb => cb.disabled = true);
                document.getElementById('area-pdf').innerHTML = '<p class="text-green-400">PDF gerado e download iniciado!</p>';
            } else {
                document.getElementById('area-pdf').innerHTML = '<p class="text-red-400">Erro ao gerar PDF.</p>';
            }
        }
    }
});
