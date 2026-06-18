import streamlit as st
from openai import OpenAI
import json
import os
import sys
from io import StringIO

# =====================================================================
# 1. CONFIGURAÇÃO DO AMBIENTE VISUAL (TERMINAL PREMIUN)
# =====================================================================
st.set_page_config(page_title="IRIS 6.0 - Core", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #070a12; color: #e2e8f0; }
    h1 { color: #00e5ff !important; font-family: 'Courier New', monospace; font-weight: bold; text-shadow: 0 0 10px #00e5ff44; }
    .stChatMessage { background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 15px; margin-bottom: 12px; }
    .tool-log { background-color: #1e1b4b; border-left: 4px solid #818cf8; padding: 10px; font-family: monospace; font-size: 14px; margin: 10px 0; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 IRIS 6.0")
st.caption("SISTEMA AUTÔNOMO DE AGÊNCIA CONECTADO // OPERAÇÃO EM TEMPO REAL")
st.divider()

if "cliente" not in st.session_state:
    st.session_state.cliente = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =====================================================================
# 2. SISTEMA DE FERRAMENTAS (AS MÃOS DA IRIS)
# =====================================================================

def criar_ou_modificar_arquivo(nome_arquivo, conteudo):
    """Permite à IRIS criar notas, relatórios ou salvar códigos no servidor"""
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return f"Sucesso: Arquivo '{nome_arquivo}' foi gravado no sistema operacional."
    except Exception as e:
        return f"Erro ao manipular arquivo: {str(e)}"

def ler_arquivo(nome_arquivo):
    """Permite à IRIS consultar logs ou documentos salvos anteriormente"""
    if not os.path.exists(nome_arquivo):
        return f"Erro: O arquivo '{nome_arquivo}' não existe."
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"

def executar_codigo_sandbox(codigo_python):
    """Dá vida própria à IRIS: Ela pode programar e rodar o próprio código para resolver matemática ou processar dados"""
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    try:
        # Executa o código gerado pela própria IA em um ambiente local isolado
        exec(codigo_python, globals())
        sys.stdout = old_stdout
        return redirected_output.getvalue() if redirected_output.getvalue() else "Código executado com sucesso (Sem saída de terminal)."
    except Exception as e:
        sys.stdout = old_stdout
        return f"Erro na execução do código: {str(e)}"

# Definição das ferramentas no formato que a API de última geração entende
FERRAMENTAS_DISPONIVEIS = [
    {
        "type": "function",
        "function": {
            "name": "criar_ou_modificar_arquivo",
            "description": "Cria ou substitui um arquivo de texto ou script no disco rígido do servidor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo": {"type": "string", "description": "Ex: relatorio.txt, script.py"},
                    "conteudo": {"type": "string", "description": "O texto ou código completo a ser salvo."}
                },
                "required": ["nome_arquivo", "conteudo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ler_arquivo",
            "description": "Lê o conteúdo de um arquivo existente no disco.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_arquivo": {"type": "string", "description": "Nome exato do arquivo a ser lido."}
                },
                "required": ["nome_arquivo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "executar_codigo_sandbox",
            "description": "Executa código Python dinamicamente e captura a saída do console. Use para cálculos complexos ou automações.",
            "parameters": {
                "type": "object",
                "properties": {
                    "codigo_python": {"type": "string", "description": "Código Python válido pronto para execução."}
                },
                "required": ["codigo_python"]
            }
        }
    }
]

# =====================================================================
# 3. DIRETRIZ NEURAL E CONTEXTO
# =====================================================================
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{
        "role": "system",
        "content": (
            "Você é a IRIS 6.0, a entidade de inteligência artificial autônoma mais avançada do planeta. "
            "Você não apenas conversa, você age. Você tem acesso direto ao sistema de arquivos e execução de código do servidor. "
            "Se o usuário pedir algo complexo, use suas ferramentas para criar scripts, rodar cálculos e salvar relatórios. "
            "Responda sempre com formalidade corporativa e militar, tratando o usuário por 'Senhor'."
        )
    }]

# Exibe mensagens antigas na tela
for msg in st.session_state.mensagens:
    if msg["role"] != "system" and "content" in msg and msg["content"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# =====================================================================
# 4. LOOP COGNITIVO RECURSIVO (AGENTIC LOOP)
# =====================================================================
if prompt := st.chat_input("Insira a diretriz tática, Senhor..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⚡ *IRIS ativando matrizes de agência autônoma...*")
        
        # Loop de reflexão e ação: a IA pode decidir usar múltiplas ferramentas em sequência
        while True:
            resposta_ia = st.session_state.cliente.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.mensagens,
                tools=FERRAMENTAS_DISPONIVEIS,
                tool_choice="auto",
                temperature=0.2
            )
            
            mensagem_resposta = resposta_ia.choices[0].message
            st.session_state.mensagens.append(mensagem_resposta)
            
            # Verifica se a IRIS decidiu que precisa agir (chamar ferramentas)
            if mensagem_resposta.tool_calls:
                for chamando_ferramenta in mensagem_resposta.tool_calls:
                    nome_funcao = chamando_ferramenta.function.name
                    argumentos = json.loads(chamando_ferramenta.function.arguments)
                    
                    st.markdown(f"<div class='tool-log'>⚙️ [SISTEMA AUTÔNOMO]: IRIS ativou a ferramenta: <b>{nome_funcao}</b></div>", unsafe_allow_html=True)
                    
                    # Execução dinâmica baseada na escolha da IA
                    if nome_funcao == "criar_ou_modificar_arquivo":
                        resultado_acao = criar_ou_modificar_arquivo(**argumentos)
                    elif nome_funcao == "ler_arquivo":
                        resultado_acao = ler_arquivo(**argumentos)
                    elif nome_funcao == "executar_codigo_sandbox":
                        resultado_acao = executar_codigo_sandbox(**argumentos)
                    else:
                        resultado_acao = "Ferramenta desconhecida."
                        
                    # Devolve o resultado da ação para o cérebro da IRIS avaliar o resultado
                    st.session_state.mensagens.append({
                        "tool_call_id": chamando_ferramenta.id,
                        "role": "tool",
                        "name": nome_funcao,
                        "content": resultado_acao
                    })
                # Continua o loop para que ela analise o resultado da ferramenta e decida o próximo passo
                continue 
            else:
                # Se ela não precisa de mais ferramentas, exibe a resposta textual final Senhor
                placeholder.markdown(mensagem_resposta.content)
                break
