from groq import generate_response
import re
import streamlit as st
def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip())<10:
        return True
    t=text.strip()
    if text.endswith(("**","*","-",":",",","(","[","{")):
        return True
    if not re.search(r"[.!?]\s*$", t):
        return True
    return False
def complete_answer(question:str, max_rounds:int=2)->str:
    base_prompt=(
        "Answer clearly in numbered points"
        "Do not cut sentences, finish each point fullt\n\n"
        f"Question:{question}"
    )
    answer=generate_response(base_prompt,temperature=0.3,max_tokens=1024)
    rounds=0
    while rounds<max_rounds and looks_incomplete(answer):
        cont_prompt=(
            "Continue exactly from where you stopped"
            "Do not repeat earlier text"
            "Finish the incomplete point and complete the answer\n\n"
            f"Question: {question}\n\n"
            f"Answer so far:\n{answer}\n\nContinue:"
        )
        more=generate_response(cont_prompt,temperature=0.3,max_tokens=1024)
        if not more or more.strip() in answer:
            break
        answer=(answer.rstrip() + "\n" + more.lstrip()).strip()
        rounds+=1
    return answer
def main():
    st.title("AI Teaching Assistant")
    st.write("Ask me anything, and ill provide a clear answer")
    user_input=st.text_input("Enter your question:")
    if user_input:
        response=complete_answer(user_input)
        st.write("**AIs answer:")
        st.markdown(response)
    else:
        st.info("Please enter a question to get started")
if __name__=="__main__":
    main()

