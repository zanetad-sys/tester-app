import json
import streamlit as st
import pandas as pd
import requests

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
    if st.button("Resetuj postup"):
        for k in st.session_state.done:
            st.session_state.done[k] = False
        st.rerun()

st.title("Jak se stát testerem – mini průvodce")
st.write("Postupně a v klidu. Základy a praxe. Zaškrtávej splněné kroky a sleduj postup v levém panelu.")

# ---------- 1) Základy ----------
st.subheader("1) Základy")
st.session_state.done["manual_vs_auto"] = st.checkbox(
    "Rozdíl: manuální vs. automatizované testování",
    value=st.session_state.done["manual_vs_auto"]
)
st.session_state.done["web_basics"] = st.checkbox(
    "Základy webu (HTML/CSS/JS)",
    value=st.session_state.done["web_basics"]
)
st.session_state.done["sql"] = st.checkbox(
    "Základy SQL",
    value=st.session_state.done["sql"]
)
st.session_state.done["git"] = st.checkbox(
    "Verzování (Git) a GitHub",
    value=st.session_state.done["git"]
)

# ---------- 2) Nástroje a praxe ----------
st.subheader("2) Nástroje a praxe")
st.session_state.done["jira"] = st.checkbox(
    "Jira/Trello – evidence úkolů",
    value=st.session_state.done["jira"]
)
st.session_state.done["testcases"] = st.checkbox(
    "Test cases a bug reporting",
    value=st.session_state.done["testcases"]
)
st.session_state.done["api"] = st.checkbox(
    "API testování (Postman)",
    value=st.session_state.done["api"]
)
st.session_state.done["auto"] = st.checkbox(
    "Automatizace – Python + Playwright/pytest",
    value=st.session_state.done["auto"]
)

# ---------- 3) Portfolio a práce ----------
st.subheader("3) Portfolio a práce")
st.session_state.done["projects"] = st.checkbox(
    "Miniprojekty na GitHubu",
    value=st.session_state.done["projects"]
)
st.session_state.done["readme"] = st.checkbox(
    "README a ukázkové bug reporty",
    value=st.session_state.done["readme"]
)
st.session_state.done["cv"] = st.checkbox(
    "CV + LinkedIn – zdůraznit praxi",
    value=st.session_state.done["cv"]
)

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

st.divider()

# ========================  API DOKUMENTACE + TESTER  ========================

st.header("🌐 API dokumentace + rychlý tester")

with st.expander("📖 Dokumentace (demo: JSONPlaceholder)"):
    st.markdown("""
**Todos API**
- `GET /todos/1` → detail jednoho úkolu  
- `GET /todos`   → seznam úkolů  
- `POST /todos`  → vytvoří nový úkol (JSON body)

**Users API**
- `GET /users/1` → detail uživatele  
- `GET /users`   → seznam uživatelů

Základní URL: `https://jsonplaceholder.typicode.com`
""")

st.subheader("🔍 Vyzkoušej endpoint")
colA, colB = st.columns([3, 1])
with colA:
    url = st.text_input("URL endpointu", "https://jsonplaceholder.typicode.com/todos/1")
with colB:
    metoda = st.selectbox("Metoda", ["GET", "POST", "PUT", "PATCH", "DELETE"])

hdrs_default = "Content-Type: application/json"
headers_text = st.text_area("HTTP headers (každý na nový řádek, ve formátu Klíč: Hodnota)", hdrs_default, height=80)
body_text = st.text_area("Request JSON body (pro POST/PUT/PATCH)", '{\n  "title": "Test úkol",\n  "completed": false\n}', height=140)

exp_col1, exp_col2 = st.columns(2)
with exp_col1:
    expected_status = st.number_input("Očekávaný status kód", value=200, step=1)
with exp_col2:
    validate_json = st.checkbox("Validovat JSON odpověď", value=False)

def parse_headers(text: str) -> dict:
    headers = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        headers[k.strip()] = v.strip()
    return headers

def parse_json_or_none(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None

if st.button("Spustit dotaz"):
    headers = parse_headers(headers_text)
    json_body = parse_json_or_none(body_text)

    try:
        if metoda == "GET":
            r = requests.get(url, headers=headers, timeout=10)
        elif metoda == "POST":
            r = requests.post(url, headers=headers, json=json_body, timeout=10)
        elif metoda == "PUT":
            r = requests.put(url, headers=headers, json=json_body, timeout=10)
        elif metoda == "PATCH":
            r = requests.patch(url, headers=headers, json=json_body, timeout=10)
        elif metoda == "DELETE":
            r = requests.delete(url, headers=headers, timeout=10)
        else:
            st.error("Neznámá metoda.")
            r = None

        if r is not None:
            st.write("**Status kód:**", r.status_code)
            if r.headers.get("Content-Type", "").startswith("application/json"):
                try:
                    st.json(r.json())
                except Exception:
                    st.text(r.text[:2000])
            else:
                st.text(r.text[:2000])

            # jednoduché vyhodnocení PASS/FAIL
            if r.status_code == int(expected_status):
                st.success(f"PASS – status {r.status_code} = očekávaný {expected_status}")
            else:
                st.error(f"FAIL – status {r.status_code} ≠ očekávaný {expected_status}")

            if validate_json:
                try:
                    _ = r.json()
                    st.info("JSON odpověď vypadá validně ✅")
                except Exception as e:
                    st.warning(f"JSON nelze načíst: {e}")

    except Exception as e:
        st.error(f"Chyba při volání API: {e}")

st.divider()

# ---------- QA TAHÁK V SIDEBARU ----------
with st.sidebar.expander("🧭 QA tahák", expanded=False):
    st.markdown("### 0) Příprava (než začneš testovat)")
    st.write("""
- **Cíl & rozsah:** co ověřuju a proč (1–2 věty)  
- **Rizika/priorita:** co je nejkritičtější  
- **Prostředí & data:** dev/test/prod-like, reálná vs. syntetická data  
- **DoD:** co musí projít, aby to bylo „OK“  
""")

    st.markdown("### 1) Návrh testů")
    st.write("""
- Techniky: ekvivalence, hranice, stavové přechody, pairwise  
- Úrovně: unit/API/UI; typy: funkční, negativní, regresní, smoke  
- Minimal viable set: nejdřív **smoke**, pak kritické cesty, pak okraje  
- Test case: **ID, kroky, očekávané, priorita**  
""")

    st.markdown("### 2) Provedení")
    st.write("""
- Scripted + Exploratory ~ **70/30** (timebox 30–60 min)  
- Evidence: PASS/FAIL, screenshot/log/HAR u failů  
- Verzování: drž v Gitu (README, `tests/`, případně `testcases.xlsx`)  
""")

    st.markdown("### 3) Bug report (stručný)")
    st.write("""
**Název** (co/kde), **Prostředí** (verze, URL), **Kroky 1..n**,  
**Očekávané vs. Aktuální**, **Důkazy**, **Sev/Pri**, pozn.: regrese?  
Propoj na commit/branch/PR, pokud víš.
""")

    st.markdown("### 4) Re-test & Regrese")
    st.write("""
- Po opravě: **re-test** + cílená **regrese** souvisejících částí  
- Před releasem: krátký smoke/regrese dle rizika  
""")

    st.markdown("### 5) Metriky & komunikace")
    st.write("""
- Viditelnost: Pass/Fail tabulka, otevřené bugy, rizika  
- Lehká KPI: % pokrytí kritických cest, # high bugů otevř./uzavř., čas do re-testu  
- Retrospektiva: co zlepšit příště (nástroje, data, přístup)  
""")

    st.markdown("### Denní best practice")
    st.write("""
- **Ráno:** nové buildy/PR → smoke + priority  
- **Během dne:** kritické cesty, krátké kvalitní bugy  
- **Průběžně:** malé a časté commity, test data pod verzemi  
- **Na konci:** aktualizuj stav, rizika, blokery  
""")

    st.markdown("### Šablony (kopi/stažení)")
    tc = """ID: TC-LOGIN-001
Cíl: Přihlášení validního uživatele
Kroky: 1) Otevřít /login  2) Vyplnit platné údaje  3) Odeslat
Očekávané: Přesměrování na /dashboard
Priorita: P1  Data: user@test.com / *****  Stav: PASS/FAIL
"""
    bug = """Název: [Checkout] 500 při prázdném košíku
Prostředí: test, v1.2.3 (build #456), Chrome 127
Kroky: 1) Otevřít /checkout 2) Kliknout „Zaplatit“ s prázdným košíkem
Očekávané: Validace „Košík je prázdný“
Aktuální: HTTP 500, bílá stránka
Důkazy: screenshot.png, network.har
Sev/Pri: High / P1  Pozn.: Regrese od v1.2.2
"""
    pr = """PR checklist:
- [ ] Projde lokální smoke
- [ ] Test data/seed aktualizovány
- [ ] Přidané/změněné testy
- [ ] Bezpečnostní dopad zhodnocen
- [ ] Aktualizován README/CHANGELOG
"""

    st.code(tc, language="markdown")
    st.download_button("⬇️ Stáhnout Test Case", tc, file_name="test-case.md")

    st.code(bug, language="markdown")
    st.download_button("⬇️ Stáhnout Bug report", bug, file_name="bug-report.md")

    st.code(pr, language="markdown")
    st.download_button("⬇️ Stáhnout PR checklist", pr, file_name="pr-checklist.md")
