import streamlit as st
from assistant_core import CareerResearchAssistant

st.set_page_config(page_title="AI Career & GenAI Research Assistant", page_icon="🧭", layout="wide")
st.title("AI Career & GenAI Research Assistant")
st.caption("GenAI capstone: OpenAI, prompt engineering, RAG, tools, and agent workflow.")

with st.sidebar:
    st.header("Knowledge base")
    uploads = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if st.button("Index documents"):
        if not uploads:
            st.warning("Upload at least one document.")
        else:
            try:
                count = CareerResearchAssistant().index_files(uploads)
                st.success(f"Indexed {count} chunks.")
            except Exception as e:
                st.error(str(e))

mode = st.selectbox("Assistant mode", ["Career Coach", "GenAI Researcher", "Document Q&A", "Interview Practice"])
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

question = st.chat_input("Ask a career, GenAI research, interview, or document question...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Preparing response..."):
            try:
                answer = CareerResearchAssistant().answer(question, mode)
            except Exception as e:
                answer = f"**Application error:** {e}"
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
