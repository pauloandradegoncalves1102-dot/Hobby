import os
import re
import pandas as pd
import gradio as gr

# Infraestrutura de armazenamento local
CAMINHO_MATRICULAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Matriculas_Nexus.csv")

def inicializar_banco():
    if not os.path.exists(CAMINHO_MATRICULAS):
        colunas = ["Data_Registro", "Contexto_Servico", "Nome", "CPF", "Nascimento", "Endereco", "Linguagem_Foco", "Forma_Pagamento"]
        pd.DataFrame(columns=colunas).to_csv(CAMINHO_MATRICULAS, index=False, encoding='utf-8')

inicializar_banco()

def processar_registro_hub(contexto, nome, cpf, nascimento, endereco, lang_foco, pagamento):
    if not nome.strip() or not cpf.strip():
        return "⚠️ ERRO OPERACIONAL: Campos obrigatórios ausentes."
    
    cpf_limpo = re.sub(r'\D', '', cpf)
    if len(cpf_limpo) != 11:
        return "⚠️ ERRO DE VALIDACAO: O CPF deve conter rigorosamente 11 dígitos."
        
    try:
        df = pd.read_csv(CAMINHO_MATRICULAS)
        novo = {
            "Data_Registro": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Contexto_Servico": contexto,
            "Nome": nome.strip(),
            "CPF": cpf_limpo,
            "Nascimento": nascimento,
            "Endereco": endereco.strip(),
            "Linguagem_Foco": lang_foco if lang_foco else "N/A",
            "Forma_Pagamento": pagamento
        }
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        df.to_csv(CAMINHO_MATRICULAS, index=False, encoding='utf-8')
        return f"✅ SUCESSO: Registro computado no banco corporativo.\nAtivo: {nome.upper()}"
    except Exception as e:
        return f"❌ FALHA CRÍTICA NO SERVIDOR: {str(e)}"

# Interface de Telemetria do Administrador (FIAP Tech Light/Dark Style)
with gr.Blocks(title="Nexus Core Pipeline") as app:
    gr.HTML("<div style='padding:15px; background:#0b0f19; border-bottom:1px solid #1f2937;'>"
            "<h1 style='color:#00f0ff; font-family:monospace; margin:0; font-size:20px;'>🤖 NEXUS CORE PIPELINE v6.0</h1>"
            "</div>")
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Console de Monitoramento")
            out_terminal = gr.Textbox(label="Logs de Transações", lines=10, interactive=False)
            btn_refresh = gr.File(label="Planilha de Cadastros Consolidada (.csv)", value=CAMINHO_MATRICULAS)

if __name__ == "__main__":
    app.launch(port=8000, inbrowser=False)
