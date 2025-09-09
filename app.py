import streamlit as st
import pandas as pd

st.set_page_config(page_title="Jak se stát testerem", page_icon="✅", layout="wide")

# ---------- Stav (aby se zaškrtávátka pamatovala) ----------
if "done" not in st.session_state:
    st.session_state.done = {
        "manual_vs_auto": False,
        "web_basics": False,
        "sql": False,
        "git": False,
        "jira": False,
        "testcases": False,
        "api": False,
        "auto": False,
        "projects": False,
        "readme": False,
        "cv": False,
    }

def percent():
    d = st.session_state.done
    return int(100 * sum(d.values()) / len(d))

# ---------- Sidebar: stav studia ----------
with st.sidebar:
    st.header("📈 Stav studia")
    st.progress(percent())
    st.metric("Splněno", f"{percent()} %")
    if st.button("Reset progresa"):
        for k in st.session_state.done:
            st.session_state.done[k] = False
        st.experimental_rerun()

st.title("Jak se stát testerem – mini průvodce")
st.write("Postupně a v klidu. Začni základy a přidávej praxi. Zaškrtávej splněné kroky a sleduj postup v levém panelu.")

# ---------- 1) Základy ----------
st.subheader("1) Základy")
st.session_state.done["manual_vs_auto"] = st.checkbox("Rozdíl: manuální vs. automatizované testování", value=st.session_state.done["manual_vs_auto"])
st.session_state.done["web_basics"]    = st.checkbox("Základy webu (HTML/CSS/JS)", value=st.session_state.done["web_basics"])
st.session_state.done["sql"]           = st.checkbox("Základy SQL", value=st.session_state.done["sql"])
st.session_state.done["git"]           = st.checkbox("Verzování (Git) a GitHub", value=st.session_state.done["git"])

# ---------- 2) Nástroje a praxe ----------
st.subheader("2) Nástroje a praxe")
st.session_state.done["jira"]      = st.checkbox("Jira/Trello – evidence úkolů", value=st.session_state.done["jira"])
st.session_state.done["testcases"] = st.checkbox("Test cases a bug reporting", value=st.session_state.done["testcases"])
st.session_state.done["api"]       = st.checkbox("API testování (Postman)", value=st.session_state.done["api"])
st.session_state.done["auto"]      = st.checkbox("Automatizace – Python + Playwright/pytest", value=st.session_state.done["auto"])

# ---------- 3) Portfolio a práce ----------
st.subheader("3) Portfolio a práce")
st.session_state.done["projects"] = st.checkbox("Miniprojekty na GitHubu", value=st.session_state.done["projects"])
st.session_state.done["readme"]   = st.checkbox("README a ukázkové bug reporty", value=st.session_state.done["readme"])
st.session_state.done["cv"]       = st.checkbox("CV + LinkedIn – zdůraznit praxi", value=st.session_state.done["cv"])

st.divider()

# ---------- Formulář: osobní plán ----------
with st.form("plan"):
    st.subheader("🗺️ Týdenní plán")
    jmeno = st.text_input("Jméno (volitelné)", "")
    hodin = st.slider("Kolik hodin týdně zvládneš?", 1, 20, 5)
    fokus = st.selectbox("Hlavní fokus na týden", ["Základy", "API testování", "Automatizace", "Portfolio/README"])
    submit = st.form_submit_button("Vygenerovat plán")
    if submit:
        body = {
            "Základy":        ["• 2 h Git + GitHub", "• 2 h HTML/CSS/JS", "• 1 h SQL"],
            "API testování":  ["• 2 h Postman základy", "• 2 h psaní requestů", "• 1 h dokumentace"],
            "Automatizace":   ["• 2 h Python", "• 2 h Playwright/pytest", "• 1 h refaktor"],
            "Portfolio/README":["• 2 h README + ukázky", "• 2 h miniprojekt", "• 1 h polishing"],
        }
        st.success((f"{jmeno}, " if jmeno else "") + f"tvůj plán na {hodin} h/týden:")
        st.write("\n".join(body[fokus]))

# ---------- Mini kvíz ----------
st.subheader("🧩 Mini kvíz (1 otázka)")
odp = st.radio("Co je Pull Request (PR) na GitHubu?",
               ["Přímé nahrání kódu do main",
                "Návrh změn z větve, který ostatní zkontrolují a sloučí",
                "Záloha repozitáře"])
if st.button("Vyhodnotit"):
    if odp == "Návrh změn z větve, který ostatní zkontrolují a sloučí":
        st.success("Správně! 👍")
    else:
        st.error("Ještě jednou: PR je návrh změn z větve, který se po schválení mergne do main.")

# ---------- „Timeline“ kroků ----------
st.subheader("🗓️ Doporučená timeline")
timeline = pd.DataFrame({
    "Týden": ["1", "2", "3", "4"],
    "Fokus": ["Základy + Git", "API testování", "Automatizace", "Portfolio/README"]
})
st.table(timeline)

# ---------- Zdroje ----------
st.subheader("📚 Užitečné zdroje")
zdroje = pd.DataFrame({
    "Téma": ["Git", "Postman (API)", "Playwright", "Streamlit"],
    "Tip": [
        "Procházej vlastní repozitáře a dělej malé commity.",
        "Trénuj collection + environment + test scripts.",
        "Začni s UI testy, pak přidej fixtures a parametrizaci.",
        "Rychlé prototypy a dashboardy – tak jako tahle appka!"
    ],
})
st.dataframe(zdroje, use_container_width=True)
