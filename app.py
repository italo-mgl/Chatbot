import streamlit as st
import requests
import json
import time

# --- 🎨 Configuração e Estilo GOCASE REVISADO ---
COLOR_GOCASE_PRIMARY = "#005CAA"   # Azul GOCASE Vibrante
COLOR_GOCASE_SECONDARY = "#FCFFFC" # Branco Suave / Off-White (Para texto em contraste)
COLOR_GOCASE_BACKGROUND = "#1E1E1E" # Fundo Escuro (Usado no tema geral)
COLOR_GOCASE_TEXT = "#FCFFFC"      # Texto Off-White
COLOR_GOCASE_DARK_CARD = "#333333" # Fundo das Mensagens do Bot

# URL da Logo Fornecida
LOGO_URL = "https://i.ibb.co/KxJXrfb0/gocase-brasil-square-Logo-1706732705121.webp"

# URLs dos Ícones (ATUALIZADO)
ICON_GITHUB_URL = "https://i.ibb.co/TBp0mSbj/github-mark-white.png"
ICON_LINKEDIN_URL = "https://i.ibb.co/kVCHNDF2/Linked-In-icon-svg.png" 


def set_gocase_theme():
    """Aplica o estilo CSS para personalizar o Streamlit com o tema GOCASE."""
    st.set_page_config(
        page_title="GoChat",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS customizado para o tema
    st.markdown(f"""
        <style>
        /* Estilo da Página */
        .stApp {{
            background-color: {COLOR_GOCASE_BACKGROUND};
            color: {COLOR_GOCASE_TEXT};
        }}
        
        /* Cabeçalho */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }}

        /* Título Principal (Para centralizar o conteúdo) */
        h1 {{
            color: {COLOR_GOCASE_PRIMARY};
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center; 
        }}
        
        /* Estilo da imagem no título */
        .logo-title {{
            width: 40px; 
            height: 40px; 
            margin-right: 15px; 
            border-radius: 50%; 
            object-fit: contain;
        }}

        /* Mensagens do Usuário */
        .stChatMessage[data-testid="stChatMessage"][data-user="true"] {{
            background-color: {COLOR_GOCASE_SECONDARY};
            border-left: 5px solid {COLOR_GOCASE_PRIMARY};
            color: #000000; 
        }}
        
        /* Mensagens do Bot */
        .stChatMessage[data-testid="stChatMessage"][data-user="false"] {{
            background-color: {COLOR_GOCASE_DARK_CARD};
            border-left: 5px solid {COLOR_GOCASE_PRIMARY}; 
            color: {COLOR_GOCASE_TEXT};
        }}
        
        /* Input de Chat */
        .stTextInput > div > div > input {{
            border: 2px solid {COLOR_GOCASE_PRIMARY};
            background-color: #333333;
            color: {COLOR_GOCASE_TEXT};
        }}
        
        /* Botão de Enviar (Customizado) */
        .stButton>button {{
            background-color: {COLOR_GOCASE_PRIMARY};
            color: {COLOR_GOCASE_SECONDARY};
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            font-weight: bold;
        }}
        
        /* Customizando a Sidebar */
        .stSidebar {{
            background-color: #000000;
        }}

        /* Botão de Exemplo na Sidebar */
        .stSidebar .stButton>button {{
            background-color: {COLOR_GOCASE_PRIMARY};
            color: {COLOR_GOCASE_SECONDARY};
        }}
        
        /* NOVO: Estilo para a barra de ícones */
        .social-icons {{
            display: flex;
            justify-content: space-around;
            padding: 15px 0;
            margin-top: 10px; 
        }}
        .social-icons a {{
            color: {COLOR_GOCASE_SECONDARY}; 
            text-decoration: none;
            transition: opacity 0.3s;
        }}
        .social-icons a:hover {{
            opacity: 0.7; /* Efeito de hover */
        }}
        .social-icons img {{
            width: 30px; /* Tamanho da imagem do ícone */
            height: 30px;
        }}

        </style>
    """, unsafe_allow_html=True)

# --- 🤖 Função de Integração n8n ---
# CORRIGIDO: Usando a URL de PRODUÇÃO (sem "-test")
N8N_WEBHOOK_URL = "https://webhook-dev.hostweb.com.br/webhook/665fe20a-b0c4-42fc-a8e0-78a07ef8f9d8" 

def call_n8n_chatbot(prompt: str) -> str:
    """
    Envia a mensagem do usuário para o webhook do n8n e retorna a resposta.
    """
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": prompt},
            timeout=15
        )
        # Se a URL não existir ou ocorrer erro 4xx/5xx, levanta exceção
        response.raise_for_status() 
        
        # O Streamlit espera um JSON com a chave 'response'
        try:
            data = response.json()
            return data.get("response", f"AVISO: n8n retornou Status 200, mas a chave 'response' está faltando no JSON. Retorno: {json.dumps(data, ensure_ascii=False)}")
            
        except requests.exceptions.JSONDecodeError:
            return f"Erro: n8n retornou uma resposta não-JSON (Status {response.status_code}). Configure o 'Respond to Webhook'."
            
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar/processar o n8n: {e}")
        # A mensagem de erro sugere verificar se o n8n está ativo e a URL correta
        return "Desculpe, falha na conexão com o servidor de automação (n8n). Verifique se o fluxo está **ATIVO** (URL de produção)."


# --- 🚀 Lógica da Aplicação Streamlit ---

# 1. Aplica o tema
set_gocase_theme()

# 2. Título da Aplicação com a Logo
st.markdown(f"""
    <h1 style='color: {COLOR_GOCASE_PRIMARY};'>
        <img src="{LOGO_URL}" class="logo-title">
        GoChat! 💬 Gocase Assistant
    </h1>
""", unsafe_allow_html=True)
st.markdown("---") # Divisor

# 3. Inicialização do Histórico de Conversa
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Olá! Eu sou o assistente virtual da GOCASE. Como posso te ajudar hoje?"})

# 4. Sidebar (sem alterações)
with st.sidebar:
    st.image(LOGO_URL, use_container_width=True) 
    st.header("ChatBot Business Case")
    st.info(f"""
        - Chat criado para desafio técnico Gocase.
        - **Ítalo Magalhães | Data Analyst**
    """)
    st.button("Limpar Histórico de Chat", on_click=lambda: st.session_state.update(messages=[]))

    st.markdown("---") 

    st.markdown(
        f"""
        <div class="social-icons">
            <a href="https://github.com/italo-mgl" target="_blank" title="GitHub">
                <img src="{ICON_GITHUB_URL}" alt="GitHub Logo">
            </a>
            <a href="https://www.linkedin.com/in/magalhaes-italo/" target="_blank" title="LinkedIn">
                <img src="{ICON_LINKEDIN_URL}" alt="LinkedIn Logo">
            </a>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("<p style='text-align: center; color: #555;'>Conecte-se!</p>", unsafe_allow_html=True)


# 5. Exibir Histórico de Mensagens
for message in st.session_state.messages:
    avatar = "😎" if message["role"] == "user" else "🌟"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# --- NOVO: Função de Callback (st.experimental_rerun REMOVIDO) ---
def handle_chat_submit():
    # Pega o prompt digitado
    prompt = st.session_state.chat_input_key
    
    if prompt:
        # Adiciona a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Limpa o input
        st.session_state.chat_input_key = ""
        # O Streamlit RE-EXECUTA AUTOMATICAMENTE APÓS O CALLBACK


# 6. Capturar a Entrada do Usuário
st.chat_input(
    "Pergunte algo ao assistente GOCASE...", 
    on_submit=handle_chat_submit, 
    key='chat_input_key' 
)


# 7. Lógica de Chamada do n8n (Executada durante a re-execução)
# Verifica se a última mensagem foi do usuário E se ainda não foi respondida
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    
    last_user_message = st.session_state.messages[-1]["content"]
    
    # Exibe o placeholder de carregamento
    with st.chat_message("assistant", avatar="🌟"):
        with st.spinner("Pensando... (Conectando com n8n)"):
            # CHAMA A FUNÇÃO REAL DA API
            response = call_n8n_chatbot(last_user_message)
            st.markdown(response)

    # Adiciona a resposta do assistente ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})