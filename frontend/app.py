import streamlit as st
import requests
import json

# --- CONFIGURATION ---
st.set_page_config(page_title="DevOps Log Agent", page_icon="🤖", layout="wide")

# Sidebar for API Configuration
with st.sidebar:
    st.header("Configuration")
    st.write("Connect this UI to your AWS Backend.")
    
    # User pastes the URL from 'terraform apply' output here
    api_url = st.text_input(
        "API Gateway URL", 
        placeholder="https://xyz.execute-api.us-east-1.amazonaws.com/chat",
        help="Paste the 'deploy_url' from your Terraform output here."
    )
    
    st.markdown("---")
    st.write("### Status")
    if api_url:
        st.success("API URL Configured")
    else:
        st.warning("Please enter API URL")

# --- MAIN CHAT INTERFACE ---
st.title("DevOps Log Analysis Agent")
st.caption("Powered by Gemini 2.0 Flash, FAISS, and AWS Lambda")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Describe the error (e.g., '503 Redis Error')..."):
    
    if not api_url:
        st.error("Please enter your API Gateway URL in the sidebar first!")
        st.stop()

    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Call AWS API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analyzing logs & documentation")
        
        try:
            # Send POST Request to AWS
            payload = {"question": prompt}
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, str):
                    data = json.loads(data)
                
                if "body" in data:
                    inner_body = json.loads(data["body"])
                    final_answer = inner_body.get("answer", "No answer found.")
                else:
                    final_answer = data.get("answer", "No answer found.")
                
                message_placeholder.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
            
            else:
                error_msg = f"❌ Error {response.status_code}: {response.text}"
                message_placeholder.error(error_msg)
        
        except Exception as e:
            message_placeholder.error(f"Connection Failed: {str(e)}")