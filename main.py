import streamlit as st
from bedrock_client import BedrockKBClient, RAGResponse
from config import KNOWLEDGE_BASE_ID, REGION, MODEL_ID
import logging

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="MEDHA!",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=Space+Mono:wght@400;700&display=swap');

:root {
    --accent:        #c9a96e;
    --accent2:       #7eb8c9;
    --glass-border:  rgba(255,255,255,0.09);
    --text-primary:  #f0ede6;
    --text-muted:    #6e6c66;
    --header-h:      56px;
}

/* ── base reset ── */
html, body, .stApp {
    background: #0f0e14 !important;
    margin: 0; padding: 0;
}
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }


.medha-header {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: var(--header-h);
    z-index: 99999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 36px;
    background: rgba(13, 12, 20, 0.97);
    border-bottom: 1px solid var(--glass-border);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 1px 0 rgba(255,255,255,0.03),
                0 4px 32px rgba(0,0,0,0.6);
}

.brand { display: flex; align-items: center; gap: 13px; }
.brand-bar {
    width: 3px; height: 26px;
    border-radius: 2px;
    background: linear-gradient(180deg, #c9a96e 0%, #7eb8c9 100%);
    box-shadow: 0 0 10px rgba(201,169,110,0.45);
    flex-shrink: 0;
}
.brand-text { display: flex; flex-direction: column; gap: 1px; }
.brand-name { display: flex; align-items: baseline; gap: 1px; line-height: 1; }
.brand-medha {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 1.42rem;
    letter-spacing: 0.14em;
    background: linear-gradient(125deg, #c9a96e 0%, #eedaa4 45%, #7eb8c9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.brand-bang {
    font-family: 'Space Mono', monospace;
    font-size: 1.28rem;
    color: #7eb8c9;
    -webkit-text-fill-color: #7eb8c9;
    margin-left: 2px;
}
.brand-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.60rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding-left: 1px;
}
.status-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    color: #6e6c66;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 5px 15px;
    letter-spacing: 0.04em;
}
.sdot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4ade80;
    flex-shrink: 0;
    animation: blink 2.2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.2} }


section[data-testid="stSidebar"] {
    background: #0d0c18 !important;
    border-right: 1px solid var(--glass-border) !important;
    margin-top: var(--header-h) !important;
}
section[data-testid="stSidebar"] > div:first-child { padding-top: 26px !important; }
section[data-testid="stSidebar"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.70rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
section[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg, #c9a96e, #7eb8c9) !important;
    border: none !important;
    box-shadow: 0 0 8px rgba(201,169,110,0.5) !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, rgba(201,169,110,0.10), rgba(126,184,201,0.10)) !important;
    border: 1px solid rgba(201,169,110,0.18) !important;
    border-radius: 10px !important;
    color: var(--accent) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.07em !important;
    width: 100% !important;
    padding: 8px 0 !important;
    transition: all 0.25s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, rgba(201,169,110,0.22), rgba(126,184,201,0.18)) !important;
    border-color: rgba(201,169,110,0.45) !important;
    box-shadow: 0 0 18px rgba(201,169,110,0.22) !important;
}
section[data-testid="stSidebar"] .stCaptionContainer p {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.64rem !important;
    color: #3a3848 !important;
}
.sb-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.08rem;
    background: linear-gradient(135deg, #c9a96e, #7eb8c9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2px;
}
.sb-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #3a3848;
    margin-bottom: 22px;
}
.tips-card {
    background: linear-gradient(135deg, rgba(201,169,110,0.06), rgba(126,184,201,0.04));
    border: 1px solid rgba(201,169,110,0.12);
    border-radius: 12px;
    padding: 13px 15px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.74rem;
    color: #6e6c66;
    line-height: 1.65;
}
.tips-card strong { color: #c9a96e; }


.main > div:first-child { margin-top: var(--header-h) !important; }

.empty-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: calc(100vh - 170px);
    gap: 0;
    padding: 0 20px;
    /* NO background or gradient here */
    background: transparent;
}
.empty-avatar {
    width: 150px; height: 50px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(201,169,110,0.15) 0%, rgba(126,184,201,0.10) 100%);
    border: 1px solid rgba(201,169,110,0.22);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: var(--accent);
    margin-bottom: 20px;
    box-shadow: 0 0 28px rgba(201,169,110,0.18),
                inset 0 1px 0 rgba(255,255,255,0.06);
}
.empty-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.38rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 10px;
    text-align: center;
}
.empty-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.86rem;
    color: var(--text-muted);
    text-align: center;
    line-height: 1.7;
    max-width: 360px;
    margin-bottom: 26px;
}
.empty-chips { display: flex; gap: 9px; flex-wrap: wrap; justify-content: center; }
.echip {
    background: rgba(201,169,110,0.06);
    border: 1px solid rgba(201,169,110,0.16);
    border-radius: 16px;
    padding: 5px 15px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.74rem;
    color: rgba(201,169,110,0.7);
    letter-spacing: 0.03em;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, rgba(201,169,110,0.09), rgba(201,169,110,0.04)) !important;
    border: 1px solid rgba(201,169,110,0.16) !important;
    border-radius: 18px 18px 5px 18px !important;
    backdrop-filter: blur(10px) !important;
    margin-bottom: 14px !important;
    padding: 15px 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: linear-gradient(135deg, rgba(126,184,201,0.07), rgba(126,184,201,0.03)) !important;
    border: 1px solid rgba(126,184,201,0.14) !important;
    border-radius: 18px 18px 18px 5px !important;
    backdrop-filter: blur(10px) !important;
    margin-bottom: 14px !important;
    padding: 15px 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25) !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
    font-size: 0.93rem !important;
    line-height: 1.74 !important;
}
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--accent) !important;
}
[data-testid="stChatMessage"] code {
    font-family: 'Space Mono', monospace !important;
    background: rgba(0,0,0,0.42) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 5px !important;
    color: #7eb8c9 !important;
    font-size: 0.79rem !important;
    padding: 1px 5px !important;
}
[data-testid="stChatMessage"] pre {
    background: rgba(0,0,0,0.48) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-left: 3px solid var(--accent) !important;
    border-radius: 12px !important;
}

/* ── chat input ── */
[data-testid="stChatInput"] {
    background: rgba(13,12,20,0.97) !important;
    border-top: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(20px) !important;
    padding: 14px 28px !important;
}
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 13px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(201,169,110,0.40) !important;
    box-shadow: 0 0 18px rgba(201,169,110,0.10) !important;
    outline: none !important;
}

details summary {
    background: rgba(201,169,110,0.04) !important;
    border: 1px solid rgba(201,169,110,0.12) !important;
    border-radius: 9px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-muted) !important;
    font-size: 0.77rem !important;
    padding: 8px 14px !important;
}

.medha-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    background: rgba(10,9,16,0.98);
    border-top: 1px solid var(--glass-border);
    backdrop-filter: blur(16px);
    z-index: 99998;
    pointer-events: none;
}
.footer-l {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #2e2c3a;
    letter-spacing: 0.18em;
}
.footer-r {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    color: #2e2c3a;
}
.fa { color: rgba(201,169,110,0.45); }

/* scrollbar */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--accent), var(--accent2));
    border-radius: 2px;
}
</style>

<div class="medha-header">
  <div class="brand">
    <div class="brand-bar"></div>
    <div class="brand-text">
      <div class="brand-name">
        <span class="brand-medha">MEDHA</span>
        <span class="brand-bang">!</span>
      </div>
      <div class="brand-sub">Enterprise Knowledge Intelligence</div>
    </div>
  </div>
  <div class="status-pill">
    <div class="sdot"></div>
    AI Online &nbsp;·&nbsp; Knowledge Base Active
  </div>
</div>

<div class="medha-footer">
  <div class="footer-l">MEDHA! · ENTERPRISE KNOWLEDGE INTELLIGENCE · v2.0</div>
  <div class="footer-r">
    Powered by <span class="fa">Amazon Bedrock</span>
    &nbsp;·&nbsp; <span class="fa">Nova Pro</span>
    &nbsp;·&nbsp; Streamlit
  </div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None

@st.cache_resource
def get_client() -> BedrockKBClient:
    return BedrockKBClient(
        knowledge_base_id=KNOWLEDGE_BASE_ID,
        region=REGION,
        model_id=MODEL_ID
    )

with st.sidebar:
    st.markdown('<div class="sb-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">Configuration</div>', unsafe_allow_html=True)

    max_results = st.slider("Retrieved Chunks", 3, 10, 5)
    st.markdown("<br>", unsafe_allow_html=True)
    temperature  = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

    st.divider()
    st.caption(f"Model: {MODEL_ID}")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="tips-card">
        💡 <strong>Tips</strong><br>
        Ask detailed questions for richer answers.
        Use <em>Clear Conversation</em> to reset the session.
    </div>
    """, unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-wrap">
      <div class="empty-avatar">MEDHA</div>
      <div class="empty-title">How can I help you today?</div>
      <div class="empty-desc">
        Ask me anything about DS Questions.<br>
        I'll search the knowledge base and give you precise, cited answers.
      </div>
      <div class="empty-chips">
        <span class="echip">Document Q&amp;A</span>
        <span class="echip">Knowledge Search</span>
        <span class="echip">Code Explanations</span>
        <span class="echip">Summarization</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander(f"Sources ({len(msg['citations'])})"):
                for i, c in enumerate(msg["citations"], 1):
                    st.markdown(f"**{i}. {c['source'].split('/')[-1]}**")
                    st.caption(c["text"])
                    st.divider()

if question := st.chat_input("Ask MEDHA! anything…"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base…"):
            try:
                client = get_client()
                result: RAGResponse = client.query(
                    question=question,
                    session_id=st.session_state.session_id,
                    max_results=max_results,
                    temperature=temperature,
                )
                st.session_state.session_id = result.session_id
                st.markdown(result.answer)

                if result.citations:
                    with st.expander(f"Sources ({len(result.citations)})"):
                        for i, c in enumerate(result.citations, 1):
                            st.markdown(f"**{i}. {c['source'].split('/')[-1]}**")
                            st.caption(c["text"])
                            st.divider()

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.answer,
                    "citations": result.citations
                })

            except Exception as e:
                st.error(f"Query failed: {e}")
