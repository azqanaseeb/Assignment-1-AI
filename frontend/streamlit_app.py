import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000"
st.set_page_config(
    page_title="Groq Chatbot",
    page_icon="⚡",
    layout="centered",
)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0d0d1f 100%);
        min-height: 100vh;
    }

    .chat-header {
        text-align: center;
        padding: 2rem 0 1.5rem;
    }
    .chat-header h1 {
        font-family: 'Space Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        color: #e2e8f0;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .chat-header h1 span {
        color: #7c3aed;
    }
    .chat-header p {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.4rem;
    }

    .message-row {
        display: flex;
        margin-bottom: 1.2rem;
        animation: fadeSlideIn 0.3s ease;
    }
    .message-row.user { justify-content: flex-end; }
    .message-row.assistant { justify-content: flex-start; }

    .bubble {
        max-width: 75%;
        padding: 0.85rem 1.1rem;
        border-radius: 18px;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .bubble.user {
        background: linear-gradient(135deg, #7c3aed, #5b21b6);
        color: #f8fafc;
        border-bottom-right-radius: 4px;
    }
    .bubble.assistant {
        background: rgba(30, 30, 50, 0.85);
        border: 1px solid rgba(124, 58, 237, 0.25);
        color: #cbd5e1;
        border-bottom-left-radius: 4px;
    }

    .bubble.assistant pre {
        background: #0d0d1f;
        border: 1px solid #2d2d4e;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        overflow-x: auto;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    .bubble.assistant code {
        font-family: 'Space Mono', monospace;
        color: #a78bfa;
    }

    .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 4px;
    }
    .avatar.user {
        background: #7c3aed;
        color: white;
        margin-left: 10px;
        order: 2;
    }
    .avatar.assistant {
        background: #1e293b;
        border: 1px solid #334155;
        color: #94a3b8;
        margin-right: 10px;
    }

    hr { border-color: #1e2a3a; margin: 1rem 0; }

    /* Style the chat_input box */
    .stChatInput textarea {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(124, 58, 237, 0.4) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
    }
    .stChatInput textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .typing-dot {
        display: inline-block;
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #7c3aed;
        margin: 0 2px;
        animation: blink 1.2s infinite;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink {
        0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
        40%           { opacity: 1;   transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

st.markdown("""
<div class="chat-header">
    <h1>⚡ Groq<span>Chat</span></h1>
    <p>Powered by LLaMA 3 · Ultra-fast inference</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown(f"**Total tokens used:** `{st.session_state.total_tokens}`")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        try:
            requests.post(f"{BACKEND_URL}/reset")
        except Exception:
            pass
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.rerun()
    st.markdown("---")
    st.markdown("**Model:** `llama-3.1-8b-instant`")
    st.markdown("**Backend:** Flask · Port 5000")

chat_placeholder = st.container()

with chat_placeholder:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        tokens = msg.get("tokens", "")

        if role == "user":
            st.markdown(f"""
            <div class="message-row user">
                <div class="bubble user">{content}</div>
                <div class="avatar user">You</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([0.07, 0.93])
            with col1:
                st.markdown('<div class="avatar assistant" style="margin-top:6px">AI</div>', unsafe_allow_html=True)
            with col2:
                with st.container():
                    st.markdown(
                        f'<div style="background:rgba(30,30,50,0.85);border:1px solid rgba(124,58,237,0.25);'
                        f'border-radius:18px;border-bottom-left-radius:4px;padding:0.85rem 1.1rem;'
                        f'color:#cbd5e1;font-size:0.95rem;line-height:1.6;">',
                        unsafe_allow_html=True
                    )
                    st.markdown(content)
                    st.markdown("</div>", unsafe_allow_html=True)
            if tokens:
                st.caption(f"🔢 {tokens} tokens")

st.markdown("---")

# ✅ st.chat_input — Submit using both Enter key and Send button
user_input = st.chat_input("Ask me anything…")

if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    with st.spinner(""):
        st.markdown("""
        <div style="color:#64748b;font-size:0.85rem;padding:0.3rem 0;">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            &nbsp;Thinking…
        </div>
        """, unsafe_allow_html=True)

        try:
            res = requests.post(
                f"{BACKEND_URL}/chat",
                json={"message": user_input.strip()},
                timeout=30
            )
            data = res.json()

            if "error" in data:
                reply = f"⚠️ **Error:** {data['error']}"
                token_count = 0
            else:
                reply = data["response"]
                token_count = data.get("usage", {}).get("total_tokens", 0)
                st.session_state.total_tokens += token_count

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply,
                "tokens": token_count
            })

        except requests.exceptions.ConnectionError:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ **Cannot connect to Flask backend.** Make sure it's running on port 5000.",
                "tokens": 0
            })

    st.rerun()
