import streamlit as st
import requests
import pandas as pd

# Set page config
st.set_page_config(page_title="Medical Text Mapper", layout="wide")

# Load secrets
API_URL = st.secrets["API_URL"]
API_KEY = st.secrets["API_KEY"]

# App title
st.title("🧠 Medical Text Mapper")
st.markdown("Enter your medical notes or terms below and click **Analyze** to map them to standard concepts.")

# Text input
user_input = st.text_area("✏️ Enter medical text:", height=200)

if st.button("🔍 Analyze"):
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Sending request to API..."):
            try:
                response = requests.post(
                    API_URL,
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={"text": user_input}
                )
                response.raise_for_status()
                data = response.json()

                st.success("✅ Analysis complete!")

                for item in data:
                    with st.expander(f"🔹 {item['input_text']} — *{item['detected_domain']}*"):
                        candidates = item.get("mapping_candidates", [])
                        if not candidates:
                            st.info("No candidates found.")
                            continue

                        df = pd.DataFrame(candidates)
                        df["score"] = df["score"].round(3)
                        df = df.rename(columns={
                            "concept_id": "Concept ID",
                            "concept_name": "Concept Name",
                            "concept_code": "Code",
                            "vocabulary_id": "Vocabulary",
                            "domain_id": "Domain",
                            "score": "Score"
                        })

                        st.dataframe(df, use_container_width=True)

            except requests.exceptions.RequestException as e:
                st.error(f"❌ API request failed: {e}")
