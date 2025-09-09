import json
import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components

# ===================== ZÁKLADNÍ NASTAVENÍ =====================
st.set_page_config(page_title="Jak se stát testerem", page_icon="🐞", layout="wide")

# ---- Globální CSS: širší obsah + menší horní mezera ----
st.markdown("""
<style>
.block-container {
  max-width: 1600px;            /* změň klidně na 1400/1500 nebo 100% !important */
  padding-left: 2rem;
  padding-right: 2rem;
}
main .block-container {          /* menší vertikální mezera nahoře */
  padding-top: 0.75rem !important;
}
h1 { margin-top: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ---- Sidebar vzhled ----
st.markdown("""
<style>
[data-testid="stSidebar"] h2 {
  font-size: 22px !important;
  font-weight: 700 !important;
  margin: 0 0 10px 0 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] > label { padding: 6px 0 !important; }
[data-testid="stSidebar"] [role="radiogroup"] p { font-size: 16px !important; }
</style>
""", unsafe_allow_html=True)

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

def progress_pct() -> int:
    d = st.session_state.get("done", {})
    return int(100 * sum(d.values()) / len(d)) if d else 0

# ===================== MENU (URL ?page=...) =====================
PAGES = [
    ("Úvod", "uvod"),
    ("Základy", "zaklady"),
    ("Nástroje", "nastroje"),
    ("Portfolio", "portfolio"),
    ("Mini kvíz", "mini-kviz"),
    ("Timeline", "timeline"),
    ("Zdroje", "zdroje"),
    ("📖 Teorie", "teorie"),
    ("🧭 QA tahák", "qa-tahak"),
    ("🌐 API tester", "api-tester"),
]
titles = [t for t, _ in PAGES]
slugs  = {t: s for t, s in PAGES}
from_slug = {s: t for t, s in PAGES}

# 1) Načti slug z URL
try:
    qp = st.query_params
    current_slug = qp.get("page", "uvod")
    if isinstance(current_slug, list):  # pro jistotu
        current_slug = current_slug[0]
except Exception:
    qp = st.experimental_get_query_params()
    current_slug = qp.get("page", ["uvod"])[0]

# 2) Předvol index rádia podle URL
default_title = from_slug.get(current_slug, "Úvod")
default_index = titles.index(default_title)

# 3) Sidebar + radio
st.sidebar.markdown("<h2>📚 Navigace</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("", titles, index=default_index)

# 4) Zapiš vybranou stránku zpět do URL (?page=...)
chosen_slug = slugs[menu]
try:
    st.query_params["page"] = chosen_slug
except Exception:
    st.experimental_set_query_params(page=chosen_slug)

# 5) Vyčisti hash v URL (zabíjí staré #bdd-...). Pokud chceš hash podle sekce,
#    změň url.hash = "" na url.hash = "#%s" a použij % chosen_slug.
components.html("""
<script>
(function () {
  try {
    const url = new URL(window.parent.location.href);
    url.hash = "";
    window.parent.history.replaceState(null, "", url.toString());
  } catch (e) {}
})();
</script>
""", height=0)

# ===================== STRÁNKY =====================
def page_uvod():
    st.title("Jak se stát testerem – mini průvodce")
    st.write("Postupně a v klidu. Základy a praxe. Zaškrtávej splněné kroky a sleduj postup.")
    col1, col2 = st.columns([1, 2], vertical_alignment="center")
    with col1:
        st.metric("Splněno", f"{progress_pct()} %")
        if st.button("Resetuj postup"):
            for k in st.session_state.done:
                st.session_state.done[k] = False
            st.rerun()
    with col2:
        st.info("Tip: Používej menu vlevo. Každá sekce se zobrazí tady v hlavní části.")

def page_zaklady():
    st.header("1) Základy")

    st.session_state.done["manual_vs_auto"] = st.checkbox(
        "Rozdíl: manuální vs. automatizované testování",
        va

