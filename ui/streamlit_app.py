import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:5000")

st.set_page_config(page_title="Feedback Analyzer")
st.title("Feedback Analyzer")
st.caption("Analyse de sentiment avec VADER (fonctionne surtout en anglais)")

text = st.text_area("Ton avis :", height=120)

if st.button("Analyser"):
    if not text.strip():
        st.warning("Ecris un texte d'abord.")
    else:
        try:
            r = requests.post(f"{API_URL}/analyze", json={"text": text}, timeout=5)
            r.raise_for_status()
            data = r.json()

            sentiment = data["sentiment"]
            score = data["score"]

            if sentiment == "positive":
                st.success(f"POSITIVE (score : {score})")
            elif sentiment == "negative":
                st.error(f"NEGATIVE (score : {score})")
            else:
                st.info(f"NEUTRAL (score : {score})")

            st.progress((score + 1) / 2)
        except requests.RequestException as e:
            st.error(f"Impossible de joindre l'API : {e}")