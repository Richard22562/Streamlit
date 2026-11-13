import io

import streamlit as st

from math_mastermind import math_generate
from teaching_assistant import teaching_generate


def export_bytes(history: list[dict[str, str]], question_key: str, answer_key: str) -> io.BytesIO:
    text = "".join(
        f"Q{i}: {item[question_key]}\nA{i}: {item[answer_key]}\n\n"
        for i, item in enumerate(history, 1)
    )
    return io.BytesIO(text.encode("utf-8"))


def render_teaching_assistant() -> None:
    st.title("🤖 AI Teaching Assistant")
    st.write("Ask about any subject and get a clear, educational explanation.")
    st.session_state.setdefault("teaching_history", [])
    history = st.session_state["teaching_history"]

    col_clear, col_export = st.columns([1, 2])
    with col_clear:
        if st.button("🧹 Clear Conversation", key="clear_teaching"):
            st.session_state["teaching_history"] = []
            st.rerun()
    with col_export:
        if history:
            st.download_button(
                label="📤 Export Chat History",
                data=export_bytes(history, "question", "answer"),
                file_name="AI_Teaching_Assistant_Conversation.txt",
                mime="text/plain",
            )

    with st.form("teaching_form", clear_on_submit=True):
        question = st.text_input("Enter your question here:")
        submitted = st.form_submit_button("Ask")

    if submitted:
        question = question.strip()
        if question:
            with st.spinner("Generating AI response..."):
                answer = teaching_generate(question)
            st.session_state["teaching_history"].insert(
                0, {"question": question, "answer": answer}
            )
            st.rerun()
        else:
            st.warning("⚠️ Please enter a question before clicking Ask.")

    st.markdown("### Conversation History")
    for index, item in enumerate(st.session_state["teaching_history"], 1):
        st.markdown(f"**Q{index}: {item['question']}**")
        st.markdown(item["answer"])


def render_math_mastermind() -> None:
    st.title("🧮 Math Mastermind")
    st.write("Solve any math problem with detailed step-by-step explanations.")

    with st.expander("📌 Examples"):
        st.markdown(
            '- Algebra: "Solve 2x² + 5x − 3 = 0"\n'
            '- Calculus: "Derivative of sin(x²) + ln(x)"\n'
            '- Geometry: "Area of triangle (0,0),(3,4),(6,0)"\n'
            '- Probability: "P(sum=7 with two dice)"'
        )

    st.session_state.setdefault("math_history", [])
    st.session_state.setdefault("math_question_key", 0)
    history = st.session_state["math_history"]

    col_clear, col_export = st.columns([1, 2])
    with col_clear:
        if st.button("🗑️ Clear", key="clear_math"):
            st.session_state["math_history"] = []
            st.rerun()
    with col_export:
        if history:
            st.download_button(
                "📄 Export",
                export_bytes(history, "question", "answer"),
                "Math_Mastermind_Solutions.txt",
                "text/plain",
            )

    with st.form("math_form", clear_on_submit=True):
        question = st.text_area(
            "📝 Enter your math problem:",
            height=100,
            placeholder="Example: Solve x² + 5x + 6 = 0",
            key=f"math_question_{st.session_state['math_question_key']}",
        )
        col_solve, col_level = st.columns([3, 1])
        solve = col_solve.form_submit_button("🧠 Solve", use_container_width=True)
        level = col_level.selectbox(
            "Level", ["Basic", "Intermediate", "Advanced"], index=1
        )

    if solve:
        question = question.strip()
        if not question:
            st.warning("⚠️ Enter a problem first.")
        else:
            with st.spinner("Solving..."):
                answer = math_generate(question, level)
            st.session_state["math_history"].insert(
                0, {"question": question, "answer": answer, "level": level}
            )
            st.session_state["math_question_key"] += 1
            st.rerun()

    if st.session_state["math_history"]:
        st.markdown("### 🧾 Solution History (Latest First)")
        for index, item in enumerate(st.session_state["math_history"], 1):
            st.markdown(f"**Q{index}: {item['question']}** · {item['level']}")
            st.markdown(item["answer"])


def main() -> None:
    st.set_page_config(page_title="AI Learning Assistant", layout="centered")
    mode = st.selectbox(
        "Choose an assistant",
        ["Teaching Assistant", "Math Mastermind"],
    )
    if mode == "Math Mastermind":
        render_math_mastermind()
    else:
        render_teaching_assistant()


if __name__ == "__main__":
    main()