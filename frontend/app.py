import streamlit as st
import requests

st.set_page_config(page_title="EduBot - Subject Tutor", layout="centered")

st.markdown(
    "<h1 style='text-align: center;'>🎓 EduBot - Subject Tutor</h1>", unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Ask questions from <b>Math</b>, <b>Science</b>, or <b>History</b>.</p>",
    unsafe_allow_html=True,
)

# Subject dropdown
subject = st.selectbox("📘 Choose a subject:", ["math", "science", "history"])

# Question input
question = st.text_input("✏️ Enter your question:")

# Ask button
if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            res = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question, "subject": subject}
            )

            if res.status_code == 200:
                response_json = res.json()
                if "answer" in response_json:
                    st.success(response_json["answer"])
                else:
                    st.error("❌ Server response missing 'answer':")
                    st.json(response_json)
            else:
                st.error(f"❌ Error {res.status_code}: {res.text}")
        
        except Exception as e:
            st.error(f"🚫 Request failed:\n{str(e)}")
