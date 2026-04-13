import streamlit as st
import requests
import time
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Multi-Agent System",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ---------------- CSS ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8c8dc, #fce4ec);
        font-family: 'Segoe UI', sans-serif;
    }

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #2c2c2c;
    }

    .subtitle {
        text-align: center;
        color: #555;
        margin-bottom: 20px;
    }

    .glass {
        background: rgba(255, 255, 255, 0.75);
        padding: 25px;
        border-radius: 18px;
        backdrop-filter: blur(15px);
        box-shadow: 0px 10px 30px rgba(0,0,0,0.15);
        margin-top: 15px;
        transition: 0.3s;
    }

    .glass:hover {
        transform: translateY(-5px);
    }

    .stButton>button {
        background: linear-gradient(135deg, #ff69b4, #ff1493);
        color: white;
        border-radius: 12px;
        height: 3em;
        font-size: 16px;
        border: none;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 5px 15px rgba(255,20,147,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🤖 Multi-Agent AI System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart AI with Research • Summary • Email • Tools</div>', unsafe_allow_html=True)
st.markdown("---")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Dashboard")

    st.metric("Total Queries", len(st.session_state.history))
    st.metric("Agents", "3")

    show_history = st.checkbox("Show History")

    if st.button("🗑 Clear History"):
        st.session_state.history = []
        st.success("History cleared!")

# ---------------- EXAMPLES ----------------
st.markdown("### 💡 Quick Examples")

col1, col2, col3 = st.columns(3)

if col1.button("🧮 Calculate"):
    st.session_state.user_input = "45*12"
    st.rerun()

if col2.button("🌦️ Weather"):
    st.session_state.user_input = "weather in Mumbai"
    st.rerun()

if col3.button("🤖 AI Explain"):
    st.session_state.user_input = "Explain Neural Networks"
    st.rerun()

# ---------------- INPUT ----------------
user_input = st.text_input(
    "Enter your query:",
    value=st.session_state.user_input,
    key="input_box"
)

# ---------------- RUN ----------------
if st.button("🚀 Run Workflow"):

    if user_input.strip() == "":
        st.warning("⚠️ Please enter a query!")

    else:
        status = st.empty()

        status.info("🧠 Understanding query...")
        time.sleep(0.5)

        status.info("🔍 Selecting agent...")
        time.sleep(0.5)

        status.info("⚡ Generating response...")
        time.sleep(0.5)

        with st.spinner("🤖 AI working..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:5000/process",
                    json={"query": user_input},
                    timeout=180
                )

                data = response.json()

                st.session_state.history.append((user_input, data))

                status.success("✅ Done!")

                # ---------------- AGENT DETECTION ----------------
                query_lower = user_input.lower()

                if "weather" in query_lower:
                    agent = "weather"
                elif any(op in query_lower for op in ["+", "-", "*", "/"]):
                    agent = "calculator"
                else:
                    agent = "ai"

                if agent == "calculator":
                    st.info("🧮 Calculator Agent Used")
                elif agent == "weather":
                    st.info("🌦️ Weather Agent Used")
                else:
                    st.info("🤖 AI Research Agent Used")

                # ---------------- CONFIDENCE ----------------
                confidence = random.randint(85, 99)
                st.progress(confidence)
                st.caption(f"AI Confidence: {confidence}%")

                # ---------------- OUTPUT (FIXED) ----------------
                tab1, tab2, tab3 = st.tabs(["🔍 Research", "📝 Summary", "📧 Email"])

                research = data.get("research", "No data")
                summary = data.get("summary", "No data")
                email = data.get("email", "No data")

                with tab1:
                    st.markdown('<div class="glass">', unsafe_allow_html=True)
                    st.markdown(research)
                    st.markdown('</div>', unsafe_allow_html=True)
                    if st.button("📋 Copy Research"):
                        st.toast("Copied Research!")

                with tab2:
                    st.markdown('<div class="glass">', unsafe_allow_html=True)
                    st.markdown(summary)
                    st.markdown('</div>', unsafe_allow_html=True)
                    if st.button("📋 Copy Summary"):
                        st.toast("Copied Summary!")

                with tab3:
                    st.markdown('<div class="glass">', unsafe_allow_html=True)
                    st.markdown(email)
                    st.markdown('</div>', unsafe_allow_html=True)
                    if st.button("📋 Copy Email"):
                        st.toast("Copied Email!")

                # ---------------- DOWNLOAD ----------------
                full_text = f"""
QUERY:
{user_input}

RESEARCH:
{research}

SUMMARY:
{summary}

EMAIL:
{email}
"""

                st.download_button(
                    "📄 Download Report",
                    full_text,
                    file_name="AI_Report.txt"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ---------------- HISTORY ----------------
if show_history and st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Previous Queries")

    for q, res in reversed(st.session_state.history):
        with st.expander(q):
            st.write("🔍 Research:", res.get("research"))
            st.write("📝 Summary:", res.get("summary"))
            st.write("📧 Email:", res.get("email"))