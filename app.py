import streamlit as st

st.set_page_config(page_title="Jak se stát testerem", page_icon="✅", layout="wide")

st.title("Jak se stát testerem – mini průvodce")
st.write("Postupně a v klidu. Začni základy a přidávej praxi.")

st.header("1) Základy")
st.checkbox("Rozdíl: manuální vs. automatizované testování")
st.checkbox("Základy webu (HTML/CSS/JS)")
st.checkbox("Základy SQL")
st.checkbox("Verzování (Git) a GitHub")

st.header("2) Nástroje a praxe")
st.checkbox("Jira/Trello – evidence úkolů")
st.checkbox("Test cases a bug reporting")
st.checkbox("API testování (Postman)")
st.checkbox("Automatizace – Python + Playwright/pytest")

st.header("3) Portfolio a práce")
st.checkbox("Miniprojekty na GitHubu")
st.checkbox("README a bug reporty")
st.checkbox("CV + LinkedIn – zdůraznit testovací praxi")

st.success("Hotovo? To je první verze mé tester-appky 🚀")
