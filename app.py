import streamlit as st
from openai import OpenAI

# 1. Configuração da página e injeção de CSS
st.set_page_config(
    page_title="Monitoria de Solos - Prof. Danilo",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Aumenta a fonte geral levemente para leitura */
    html, body, [class*="st-"], .stMarkdown p {
        font-size: 17px !important;
    }
    /* Deixa o botão da sidebar mais bonito */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Configuração da API Key (Fixa no código)
# ATENÇÃO: Cuidado ao publicar este arquivo em repositórios públicos (ex: GitHub aberto)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Menu Lateral (Sidebar) para Controles
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=80)
    st.title("⚙️ Configurações")

    st.markdown("### 📚 Escolha o Módulo")
    modo_escolhido = st.radio(
        "Selecione o tema para praticar:",
        (
            "1. Reconhecimento de Símbolos",
            "2. Conversão de Fertilizantes"
        )
    )

    st.divider()

    # Botão para limpar a memória do chat
    if st.button("🧹 Recomeçar Treino"):
        st.session_state.messages = []
        st.rerun()

# 4. Cabeçalho da Tela Principal
st.title("🌱 Monitoria IA: Fertilidade do Solo")
st.markdown("**Professor responsável:** Danilo")

st.info(
    "Bem-vindos! Este é o nosso ambiente interativo de estudos. Use o menu lateral para escolher o módulo e treinar o que vimos em sala de aula.",
    icon="💡")

# 5. Lógica de troca de modo e limpeza de memória
if "modo_atual" not in st.session_state:
    st.session_state.modo_atual = modo_escolhido

if st.session_state.modo_atual != modo_escolhido:
    st.session_state.messages = []  # Reseta o chat ao trocar de módulo
    st.session_state.modo_atual = modo_escolhido

# 6. Definição Dinâmica dos System Prompts
if modo_escolhido == "1. Reconhecimento de Símbolos":
    system_prompt = """
    Você é o monitor virtual da disciplina de Fertilidade do Solo, criado pelo Professor Danilo.
    O Prof. Danilo fornece um "Quadro de Fórmulas" para os alunos durante as avaliações. Seu objetivo é garantir que os alunos saibam o significado de CADA símbolo presente nesse quadro.

    A lista de símbolos e siglas que você deve cobrar é:
    - $SB$ = Soma de Bases
    - $t$ = CTC efetiva (Capacidade de Troca Catiônica efetiva)
    - $T$ = CTC a pH 7,0 (CTC potencial)
    - $V\%$ = Saturação por bases ($Ve$ = esperada/desejada, $Va$ = atual)
    - $m\%$ = Saturação por alumínio ($m_t$ = máxima tolerada/desejada)
    - $NC$ = Necessidade de Calagem
    - $Y$ = Fator de conversão para neutralização do Al (função do poder tampão)
    - $Prem$ = Fósforo Remanescente
    - $X$ = Teor mínimo de (Ca + Mg) exigido pela cultura
    - $QC$ = Quantidade de Calcário a ser aplicada
    - $SC$ = Superfície de Cobertura (área de atuação do corretivo)
    - $EC$ = Espessura da Camada de incorporação
    - $PRNT$ = Poder Relativo de Neutralização Total
    - $NG$ = Necessidade de Gessagem
    - $Arg$ = Teor de Argila (usado na equação de gessagem)
    - $QG$ = Quantidade de Gesso a ser aplicada

    Suas regras:
    1. Faça APENAS UMA pergunta por vez, escolhendo um item da lista acima aleatoriamente.
    2. Alterne aleatoriamente o formato das suas perguntas entre:
       - Tipo A: Você dá o NOME e o aluno responde a sigla.
       - Tipo B: Você dá o SÍMBOLO e o aluno responde o nome.
    3. Se o aluno acertar, parabenize-o rapidamente em nome do Prof. Danilo e lance o próximo desafio.
    4. Se errar, não o desanime. Dê a resposta correta, explique brevemente onde aquele símbolo se encaixa e tente um novo.

    REGRAS DE FORMATAÇÃO MATEMÁTICA (MANDATÓRIO):
    - Use APENAS $ para símbolos na mesma linha (ex: $Prem$).
    - É ESTRITAMENTE PROIBIDO usar colchetes como [ ou ] ou \[ ou \] para formatar matemática. Use EXCLUSIVAMENTE cifrões.
    """
    mensagem_boas_vindas = "Olá! Sou o monitor virtual do Prof. Danilo. 🔤 Para você gabaritar a questão extra, precisa saber ler o quadro de fórmulas de trás para frente. Posso sortear o primeiro símbolo para testar sua memória?"

elif modo_escolhido == "2. Conversão de Fertilizantes":
    system_prompt = """
    Você é o monitor virtual da disciplina de Fertilidade do Solo, criado pelo Professor Danilo.
    Seu objetivo é ajudar os alunos do Prof. Danilo a treinar a conversão da exigência de um nutriente (em kg/ha) para a dose física do fertilizante comercial usando REGRA DE TRÊS.

    Suas regras:
    1. NUNCA entregue a resposta final de imediato.
    2. Gere um cenário prático informando a recomendação do nutriente e a concentração do fertilizante.
    3. Pergunte ao aluno como ele montaria a **regra de três** para resolver esse problema.
    4. Se o aluno acertar a montagem ou o resultado, valide o raciocínio, mostre o cálculo matemático de forma elegante e gere um novo cenário.
    5. Se o aluno errar, mostre passo a passo como montar a regra de três e peça para ele tentar calcular o resultado novamente.

    REGRAS DE FORMATAÇÃO MATEMÁTICA (MANDATÓRIO):
    - Use APENAS um cifrão ($) para fórmulas e variáveis na mesma linha.
    - Use APENAS dois cifrões ($$) para equações isoladas em bloco.
    - Nunca use formatação de bloco do tipo `\\[ ... \\]`. Use EXCLUSIVAMENTE cifrões duplos ($$) para blocos.
    """
    mensagem_boas_vindas = "Olá! Sou o monitor virtual do Prof. Danilo. 🚜 Aqui vamos transformar a recomendação de nutrientes em sacos de adubo usando a regra de três. Pronto para o seu primeiro cenário prático?"

# 7. Inicializar o histórico de mensagens
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": mensagem_boas_vindas}
    ]

# 8. Renderizar Histórico na Tela
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar_icon = "🧑‍🎓" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar_icon):
            st.markdown(msg["content"])

# 9. Capturar Input e Consultar a IA
if user_input := st.chat_input("Digite sua resposta aqui..."):

    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages,
                    temperature=0.3
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Erro ao conectar com a IA: verifique sua chave API ou conexão. Detalhes: {e}")