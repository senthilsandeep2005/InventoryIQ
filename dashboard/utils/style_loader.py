import streamlit as st
from pathlib import Path


def load_css():
    css_path = Path(__file__).resolve().parents[1] / "styles" / "main.css"

    with open(css_path) as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )