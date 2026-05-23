import streamlit as st
import requests

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="QA AI Agent",
    page_icon="🧠",
    layout="wide"
)

# ============================================
# HEADER
# ============================================
st.title("🧠 QA AI Agent")

st.markdown("""
Offline AI-Powered QA Assistant using:

- Ollama
- ChromaDB
- RAG
- FastAPI
""")

# ============================================
# USER INPUT
# ============================================
question = st.text_area(
    "Ask your QA question:",
    height=150
)

# ============================================
# ASK BUTTON
# ============================================
if st.button("Ask AI"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating response..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": question
                    }
                )

                data = response.json()

                st.success("Response Generated")

                # ====================================
                # ANSWER
                # ====================================
                st.subheader("🧠 RAG Answer")

                st.write(
                    data.get(
                        "answer",
                        "No answer found."
                    )
                )

                # ====================================
                # CONFIDENCE SCORE
                # ====================================
                confidence = data.get(
                    "confidence_score",
                    0
                )

                st.metric(
                    "Confidence Score",
                    f"{confidence}%"
                )

                # ====================================
                # PROGRESS BAR
                # ====================================
                st.progress(
                    min(
                        int(confidence),
                        100
                    )
                )

            except Exception as e:

                st.error(
                    f"Error connecting to API: {e}"
                )