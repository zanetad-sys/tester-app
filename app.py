import json
import streamlit as st
import pandas as pd
import requests

# ===================== ZÁKLADNÍ NASTAVENÍ =====================
st.set_page_config(page_title="Jak se stát testerem", page_icon="🐞", layout="wide")

# ===================== STAV (checkboxy) =====================
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
    return int(100 * sum(d.values()) / len(d)) if d else 0

# ===================== MENU V SIDEBARU =====================
menu = st.sidebar.radio(
    "📚 Navigace",
    [
        "Úvod",
        "Základy",
        "Nástroje",
        "Portfolio",
        "Mini kvíz",
        "Timeline",
        "Zdroje",
        "📖 Teorie",
        "🧭 QA tahák",
        "🌐 API tester",
    ],
    index=0,
)

# ===================== STRÁNKY =====================

def page_uvod():
    st.title("Jak se stát testerem – mini průvodce")
    st.write("Postupně a v klidu. Základy a praxe. Zaškrtávej splněné kroky a sleduj postup.")

    st.metric("Splněno", f"{percent()} %")

    if st.button("Resetuj postup"):
        for k in st.session_state.done:
            st.session_state.done[k] = False
        st.rerun()

    st.info("Tip: Používej menu vlevo. Každá sekce se zobrazí tady v hlavní části.")

def page_zaklady():
    st.header("1) Základy")
    st.checkbox("Rozdíl: manuální vs. automatizované testování", key="manual_vs_auto")
    st.checkbox("Základy webu (HTML/CSS/JS)", key="web_basics")
    st.checkbox("Základy SQL", key="sql")
    st.checkbox("Verzování (Git) a GitHub", key="git")
    st.checkbox("Základy práce s test casy", key="testcases")

def page_nastroje():
    st.header("2) Nástroje")
    st.checkbox("Jira / Trello – evidence úkolů a bugů", key="jira")
    st.checkbox("Postman – testování API", key="api")
    st.checkbox("Automatizace – Python + Playwright/pytest", key="auto")

def page_portfolio():
    st.header("3) Portfolio a práce")
    st.checkbox("Miniprojekty na GitHubu (testovací skripty, ukázky)", key="projects")
    st.checkbox("README s popisem projektů a nástrojů", key="readme")
    st.checkbox("CV (zaměřené na QA) + LinkedIn profil", key="cv")

def page_kviz():
    st.header("🧩 Mini kvíz – pohovorové otázky")
    st.write("👉 Sem můžeš přidat své kvízové otázky.")

def page_timeline():
    st.header("🗓️ Doporučená timeline")
    timeline = pd.DataFrame({
        "Týden": ["1–2", "3–4", "5–6", "7–8"],
        "Fokus": [
            "Základy testování",
            "Git, web základy, SQL",
            "Nástroje: Jira, Postman",
            "Automatizace: Python, Playwright"
        ]
    })
    st.table(timeline)

def page_zdroje():
    st.header("📚 Užitečné zdroje")
    st.markdown("- [ISTQB Foundation sylabus](https://www.istqb.org/)\n"
                "- [SQLZoo](https://sqlzoo.net/)\n"
                "- [Postman Learning Center](https://learning.postman.com/)\n"
                "- [Playwright docs](https://playwright.dev/python/docs/intro)\n")

def page_teorie():
    st.header("📖 Teorie testování")
    st.write("Základní pojmy, typy testů, severity vs priority…")

def page_qatahaky():
    st.header("🧭 QA tahák")
    st.write("Rychlé taháky pro praxi testera.")

def page_api_tester():
    st.header("🌐 API tester")
    st.write("Jednoduchý tester pro volání API.")

# ===================== ROUTER =====================
if menu == "Úvod":
    page_uvod()
elif menu == "Základy":
    page_zaklady()
elif menu == "Nástroje":
    page_nastroje()
elif menu == "Portfolio":
    page_portfolio()
elif menu == "Mini kvíz":
    page_kviz()
elif menu == "Timeline":
    page_timeline()
elif menu == "Zdroje":
    page_zdroje()
elif menu == "📖 Teorie":
    page_teorie()
elif menu == "🧭 QA tahák":
    page_qatahaky()
elif menu == "🌐 API tester":
    page_api_tester()

