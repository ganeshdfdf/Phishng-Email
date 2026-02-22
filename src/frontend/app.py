import streamlit as st
import requests

st.set_page_config(page_title="Phishing Email Detector", page_icon="🚫")

st.title("Phishing Email Detector 📧")
st.markdown("Enter the content of an email below to check if it's safe or phishing.")

email_text = st.text_area("Email Content", height=200)

if st.button("Analyze"):
    if not email_text:
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            try:
                # Assumes API is running on localhost:8000
                response = requests.post(
                    "http://localhost:8000/predict",
                    json={"content": email_text}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    is_phishing = result['is_phishing']
                    confidence = result['confidence']
                    features = result['features']
                    
                    if is_phishing:
                        st.error(f"🚨 **PHISHING DETECTED** (Confidence: {confidence:.2%})")
                    else:
                        st.success(f"✅ **SAFE EMAIL** (Confidence: {confidence:.2%})")
                    
                    st.subheader("Analysis Details")
                    # Use columns for better layout
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Suspicious Keywords", features['keyword_count'])
                        st.metric("URLs Found", features['url_count'])
                    with col2:
                        st.metric("IP Address in URL", 'Yes' if features['ip_in_url'] else 'No')
                        st.metric("Email Length", features['email_length'])
                    
                else:
                    st.error("Error communicating with the analysis server.")
                    st.write(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server. Is it running?")
