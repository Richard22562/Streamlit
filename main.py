import streamlit as st
import requests
import urllib.parse
st.set_page_config(page_title="Safe AI Image Generator", page_icon=":art:", layout="wide")
st.title("Safe AI Image Generator")
st.write("Type a prompt below to create a fun safe AI picture")
BLOCKED_WORDS = [ "gun", "weapon", "blood", "dead", "body", "corpse", "kill", "murder", "nude", "naked", "nsfw", "violence", "knife", "gore", "explode", "death" ]
def check_safety(user_prompt):
    prompt_lower=user_prompt.lower()
    for words in BLOCKED_WORDS:
        if words in prompt_lower:
            return False, f"The prompt is not allowed for safety measures, Blocked words: {words}"
    return True,"Safe,Generated"
user_prompt=st.text_input(
    "Enter your image prompt:",
    placeholder="e.g., A cat wearing an astronaut suit on mars"
)
col1, col2 = st.columns(2) 
with col1: 
    width = st.slider("Image Width", min_value=256, max_value=768, value=512, step=128) 
with col2: 
    height = st.slider("Image Height", min_value=256, max_value=768, value=512, step=128)
if st.button("Generate Image"):
    if not user_prompt.strip():
        st.warning("Please type a description first")
    else:
        is_safe, message = check_safety(user_prompt)
        if not is_safe:
            st.error(f"Blocked Content: {message}")
            st.info("Please change your prompt to something suitable")
        else:
            with st.spinner("Creating your image........ Please wait........"):
                safe_prompt = f"{user_prompt}, high quality, kid friendly, digital art, vibrant"
                encoded_prompt = urllib.parse.quote(safe_prompt) 
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
                
                try:
                    # Add User-Agent header so the server accepts the Python request
                    headers = {"User-Agent": "Mozilla/5.0"}
                    response = requests.get(image_url, headers=headers)
                    
                    if response.status_code == 200:
                        # Pass response.content (the raw image bytes) instead of the url string
                        st.image(response.content, caption="Generated Image", use_container_width=True)
                    else:
                        st.error(f"Failed to generate image (Status Code: {response.status_code}). Please try again.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")