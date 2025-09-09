import json
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Jak se stát testerem", page_icon="✅", layout="wide")

# ---------- SAFE STATE KEYS ----------
if "done" not in st.session_state:
    st.session_state.done = {}

DEFAULT_KEYS = {
    # Basics
    "qa_definition": False, "qa_roles": False, "qa_sdlc": False,
    "qa_types": False, "qa_vv": False, "qa_sevpri": False,
    "tech_web": False, "tech_sql": False, "tech_git": False, "tech_logs": False,
    "tech_http": False, "tech_api": False,
    # Tools
    "tools_jira": False, "tools_testmgmt": False, "tools_postman": False, "tools_soapui": False,
    "tools_curl": False, "tools_git": False,
    "tools_python": False, "tools_playwright": False, "tools_selenium": False, "tools_pytest": False,
    "tools_selide": False, "tools_devtools": False, "tools_logs": False, "tools_cicd": False,
    "tools_db_clients": False, "tools_docker": False, "tools_ide": False, "tools_perf": False,
    # Portfolio
    "projects": False, "readme": False, "cv": False,
}
for k, v in DEFAULT_KEYS.items():
    st.session_state.done.setdefault(k, v)

def percent():
    d = st.session_state.done
    return int(100 * sum(1 for v in d.values() if v) / len(d)) if d else 0

# ---------- MENU ----------
menu = st.sidebar.radio(
    "📚 Navigace",
    ["Úvod", "Základy", "Nástroje", "Portfolio", "Mini kvíz", "Timeline", "Zdroje", "📖 Teorie", "🧭 QA tahák", "🌐 API tester"],
    index=0,
)

# ---------- PAGES ----------
def page_uvod():
    st.title("Jak se stát testerem – mini průvodce")
    st.write("Postupně a v klidu. Základy a praxe. Zaškrtávej splněné kroky a sleduj postup.")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Splněno", f"{percent()} %")
        if st.button("Resetuj postup"):
            for k in st.session_state.done:
                st.session_state.done[k] = False
            st.rerun()
    with c2:
        st.info("Používej menu vlevo. Každá sekce se zobrazí v hlavní části.")

def page_zaklady():
    st.header("1) Základy QA – kompletní přehled")

    st.subheader("🎯 Co je QA a role testera")
    st.session_state.done["qa_definition"] = st.checkbox("Co je testování / QA", value=st.session_state.done["qa_definition"])
    st.session_state.done["qa_roles"] = st.checkbox("Role: tester vs. vývojář vs. produkták", value=st.session_state.done["qa_roles"])
    st.session_state.done["qa_sdlc"] = st.checkbox("Životní cyklus vývoje (SDLC, agilní, waterfall)", value=st.session_state.done["qa_sdlc"])
    st.session_state.done["qa_types"] = st.checkbox("Typy testů – úrovně (unit, integrační, systémové, akceptační)", value=st.session_state.done["qa_types"])
    st.session_state.done["qa_vv"] = st.checkbox("Verifikace vs. Validace", value=st.session_state.done["qa_vv"])
    st.session_state.done["qa_sevpri"] = st.checkbox("Severita vs. priorita bugů", value=st.session_state.done["qa_sevpri"])

    with st.expander("📖 Vysvětlivky – QA základy"):
        st.markdown(
            "- QA = zajištění kvality (procesy + testování)\n"
            "- SDLC = waterfall (fáze po sobě) vs. agile (iterace)\n"
            "- Verifikace = děláme věci správně; Validace = děláme správné věci\n"
            "- Severita = dopad chyby; Priorita = rychlost řešení\n"
        )

    st.divider()

    st.subheader("🖥️ Technické minimum")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.done["tech_web"] = st.checkbox("Web (HTML, CSS, JS)", value=st.session_state.done["tech_web"])
        st.session_state.done["tech_sql"] = st.checkbox("Databáze + SQL", value=st.session_state.done["tech_sql"])
    with c2:
        st.session_state.done["tech_git"] = st.checkbox("Git/GitHub", value=st.session_state.done["tech_git"])
        st.session_state.done["tech_logs"] = st.checkbox("Logy (application/system/security)", value=st.session_state.done["tech_logs"])
    with c3:
        st.session_state.done["tech_http"] = st.checkbox("HTTP/HTTPS základy", value=st.session_state.done["tech_http"])
        st.session_state.done["tech_api"] = st.checkbox("API (REST/JSON, SOAP/XML)", value=st.session_state.done["tech_api"])

    with st.expander("📖 Vysvětlivky – Technické minimum"):
        st.markdown(
            "- Web = HTML, CSS, JS\n"
            "- SQL = SELECT, JOIN, INSERT, UPDATE\n"
            "- Git = commit, push, pull request\n"
            "- HTTP = request/response, status kódy (200, 404, 500)\n"
            "- API = REST (JSON), SOAP (XML)\n"
        )

    st.divider()

    st.subheader("🛠️ Praktické nástroje")
    st.session_state.done["tools_postman"] = st.checkbox("Postman / SOAP UI", value=st.session_state.done["tools_postman"])
    st.session_state.done["tools_devtools"] = st.checkbox("DevTools (network, console, cookies)", value=st.session_state.done["tools_devtools"])

    st.subheader("🤖 Automatizace + Bonus")
    st.session_state.done["auto_python"] = st.checkbox("Základy Pythonu/jiného jazyka", value=st.session_state.done["auto_python"])
    st.session_state.done["auto_framework"] = st.checkbox("Framework (pytest, Playwright, Selenium)", value=st.session_state.done["auto_framework"])
    st.session_state.done["auto_ci"] = st.checkbox("CI/CD (GitHub Actions, GitLab CI)", value=st.session_state.done["auto_ci"])

    # Export checklistu
    items = [k for k in st.session_state.done if k.startswith(("qa_", "tech_", "tools_", "auto_"))]
    st.download_button("⬇️ Stáhnout checklist základů", "\\n".join(f"- {k}" for k in items), "qa-zaklady-checklist.txt")

def page_nastroje():
    st.header("2) Nástroje – co by měl tester znát")

    st.subheader("📂 Organizace & bug tracking")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.done["tools_jira"] = st.checkbox("Jira / Trello / Asana / Bugzilla", value=st.session_state.done["tools_jira"])
    with c2:
        st.session_state.done["tools_testmgmt"] = st.checkbox("Test management: TestRail / Xray / Zephyr / Azure DevOps / Sheets", value=st.session_state.done["tools_testmgmt"])

    st.divider()

    st.subheader("🌐 API & komunikace")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.done["tools_postman"] = st.checkbox("Postman – kolekce, environmenty, test scripts", value=st.session_state.done["tools_postman"])
    with c2:
        st.session_state.done["tools_soapui"] = st.checkbox("SOAP UI – testování SOAP (XML)", value=st.session_state.done["tools_soapui"])
    with c3:
        st.session_state.done["tools_curl"] = st.checkbox("curl – rychlé volání API v terminálu", value=st.session_state.done["tools_curl"])

    st.divider()

    st.subheader("🔁 Verzování")
    st.session_state.done["tools_git"] = st.checkbox("Git + GitHub/GitLab/Bitbucket (commity, PR/MR, review)", value=st.session_state.done["tools_git"])

    st.divider()

    st.subheader("🤖 Automatizace testů")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.session_state.done["tools_python"] = st.checkbox("Python / (Java/JS dle firmy)", value=st.session_state.done["tools_python"])
    with c2:
        st.session_state.done["tools_playwright"] = st.checkbox("Playwright (UI testy)", value=st.session_state.done["tools_playwright"])
    with c3:
        st.session_state.done["tools_selenium"] = st.checkbox("Selenium (UI testy)", value=st.session_state.done["tools_selenium"])
    with c4:
        st.session_state.done["tools_pytest"] = st.checkbox("pytest (fixtures, reporty)", value=st.session_state.done["tools_pytest"])
    st.session_state.done["tools_selide"] = st.checkbox("Selenium IDE (rychlé prototypy)", value=st.session_state.done["tools_selide"])

    st.divider()

    st.subheader("🧰 DevTools & logy")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.done["tools_devtools"] = st.checkbox("Chrome/Edge DevTools (Network, Console, Storage, Cookies)", value=st.session_state.done["tools_devtools"])
    with c2:
        st.session_state.done["tools_logs"] = st.checkbox("Logy: application / system / security", value=st.session_state.done["tools_logs"])

    st.divider()

    st.subheader("⚙️ CI/CD")
    st.session_state.done["tools_cicd"] = st.checkbox("GitHub Actions / GitLab CI – testy po commitu", value=st.session_state.done["tools_cicd"])

    st.divider()

    st.subheader("🗄️ Databáze")
    st.session_state.done["tools_db_clients"] = st.checkbox("DBeaver / pgAdmin / MySQL Workbench (GUI pro SQL)", value=st.session_state.done["tools_db_clients"])

    st.divider()

    st.subheader("🧩 Doplňkové")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.done["tools_docker"] = st.checkbox("Docker – lokální dev/test prostředí", value=st.session_state.done["tools_docker"])
    with c2:
        st.session_state.done["tools_ide"] = st.checkbox("IDE: VS Code / PyCharm (debugging, linting)", value=st.session_state.done["tools_ide"])
    with c3:
        st.session_state.done["tools_perf"] = st.checkbox("Výkonnostní testy: JMeter / k6", value=st.session_state.done["tools_perf"])

    chosen = [k for k, v in st.session_state.done.items() if k.startswith("tools_") and v]
    st.download_button("⬇️ Stáhnout checklist nástrojů", "\\n".join(f"- {x}" for x in chosen) if chosen else "Zatím nic nezaškrtnuto.", "nastroje-checklist.txt")

def page_portfolio():
    st.header("3) Portfolio a práce")

    st.session_state.done["projects"] = st.checkbox("Miniprojekty na GitHubu", value=st.session_state.done["projects"])
    st.session_state.done["readme"] = st.checkbox("README a ukázkové bug reporty", value=st.session_state.done["readme"])
    st.session_state.done["cv"] = st.checkbox("CV + LinkedIn – zdůraznit praxi", value=st.session_state.done["cv"])

    st.info("Každý miniprojekt ukazuje konkrétní skill. Krátké, ale čitelné README je klíčové.")
    st.divider()

    # Týdenní plán
    with st.form("plan"):
        st.subheader("🗺️ Týdenní plán")
        jmeno = st.text_input("Jméno (volitelné)", "")
        hodin = st.slider("Kolik hodin týdně zvládneš?", 1, 20, 5)
        fokus = st.selectbox("Hlavní fokus na týden", ["Základy", "API testování", "Automatizace", "Portfolio/README"])
        submit = st.form_submit_button("Vygenerovat plán")
        if submit:
            body = {
                "Základy": ["• 2 h Git+GitHub", "• 2 h HTML/CSS/JS", "• 1 h SQL"],
                "API testování": ["• 2 h Postman", "• 2 h requesty", "• 1 h dokumentace"],
                "Automatizace": ["• 2 h Python", "• 2 h Playwright/pytest", "• 1 h refaktor"],
                "Portfolio/README": ["• 2 h README", "• 2 h miniprojekt", "• 1 h polishing"],
            }
            st.success((f"{jmeno}, " if jmeno else "") + f"tvůj plán na {hodin} h/týden:")
            st.write("\\n".join(body[fokus]))

    st.divider()

    # Generátor README (download mimo form)
    st.subheader("🧩 Generátor README.md pro miniprojekt")
    with st.form("readme_form"):
        proj = st.text_input("Název projektu", "qa-api-tests")
        popis = st.text_area("Krátký popis", "Sada API testů pro demo službu (REST).")
        technologie = st.text_input("Technologie", "Python, pytest, requests, Postman")
        kroky = st.text_area("Jak spustit", "pip install -r requirements.txt\\npytest -q")
        co_testuju = st.text_area("Co se testuje", "- Smoke testy endpointů\\n- Pozitivní/negativní scénáře\\n- Validace status kódů a JSON schema")
        odkaz = st.text_input("Odkaz (repo / appka)", "https://github.com/uzivatel/qa-api-tests")
        submitted = st.form_submit_button("Vygenerovat README")
        if submitted:
            md = f"# {proj}\\n\\n{popis}\\n\\n## Technologie\\n{technologie}\\n\\n## Jak spustit\\n```
{kroky}
```\\n\\n## Co se testuje\\n{co_testuju}\\n\\n## Odkazy\\n- Repo/App: {odkaz}\\n"
            st.session_state["generated_readme"] = md

    if st.session_state.get("generated_readme"):
        st.code(st.session_state["generated_readme"], language="markdown")
        st.download_button("⬇️ Stáhnout README.md", st.session_state["generated_readme"], file_name="README.md")
        if st.button("Vymazat výsledek"):
            st.session_state["generated_readme"] = None
            st.rerun()

    st.divider()

    # Šablony
    st.subheader("📑 Šablony do portfolia")
    bug = (
        "Název: [Checkout] 500 při prázdném košíku\\n"
        "Prostředí: test, v1.2.3 (build #456), Chrome 127\\n"
        "Kroky: 1) Otevřít /checkout 2) Kliknout 'Zaplatit' s prázdným košíkem\\n"
        "Očekávané: Validace 'Košík je prázdný'\\n"
        "Aktuální: HTTP 500, bílá stránka\\n"
        "Důkazy: screenshot.png, network.har\\n"
        "Sev/Pri: High / P1  Pozn.: Regrese od v1.2.2\\n"
    )
    tc = (
        "ID: TC-LOGIN-001\\n"
        "Cíl: Přihlášení validního uživatele\\n"
        "Kroky: 1) Otevřít /login  2) Vyplnit platné údaje  3) Odeslat\\n"
        "Očekávané: Přesměrování na /dashboard\\n"
        "Priorita: P1  Data: user@test.com / *****  Stav: PASS/FAIL\\n"
    )
    st.download_button("⬇️ Stáhnout Bug report (MD)", bug, file_name="bug-report.md")
    st.download_button("⬇️ Stáhnout Test Case (MD)", tc, file_name="test-case.md")

    chosen = [k for k, v in st.session_state.done.items() if k in ("projects", "readme", "cv") and v]
    st.download_button("⬇️ Stáhnout checklist portfolia", "\\n".join(f"- {x}" for x in chosen) if chosen else "Zatím nic nezaškrtnuto.", "portfolio-checklist.txt")

def page_kviz():
    st.header("🧩 Mini kvíz")
    odp = st.radio("Co je Pull Request (PR) na GitHubu?", ["Přímé nahrání kódu do main", "Návrh změn z větve, který ostatní zkontrolují a sloučí", "Záloha repozitáře"])
    if st.button("Vyhodnotit"):
        st.success("Správně! 👍" if odp == "Návrh změn z větve, který ostatní zkontrolují a sloučí" else "Ještě jednou: PR je návrh změn z větve, který se po schválení mergne do main.")

def page_timeline():
    st.header("🗓️ Doporučená timeline")
    st.table(pd.DataFrame({"Týden": ["1", "2", "3", "4"], "Fokus": ["Základy + Git", "API testování", "Automatizace", "Portfolio/README"]}))

def page_zdroje():
    st.header("📚 Užitečné zdroje – kurátorský seznam")
    st.markdown("- Pro Git (kniha): https://git-scm.com/book/en/v2")
    st.markdown("- Postman Learning Center: https://learning.postman.com/")
    st.markdown("- JSONPlaceholder: https://jsonplaceholder.typicode.com/")
    st.markdown("- Swagger Petstore: https://petstore.swagger.io/")
    st.markdown("- MDN Web Docs: https://developer.mozilla.org/")
    st.markdown("- SQLBolt: https://sqlbolt.com/")

    resources_md = (
        "# Užitečné zdroje (QA starter pack)\\n"
        "- Git & GitHub: Pro Git, PR workflow\\n"
        "- Web: MDN (HTML/CSS/JS)\\n"
        "- SQL: SQLBolt\\n"
        "- API: HTTP status codes, Postman, Swagger Petstore, JSONPlaceholder\\n"
    )
    st.download_button("⬇️ Stáhnout seznam zdrojů (Markdown)", resources_md, file_name="uzitecne-zdroje.md")

def page_teorie():
    st.header("📖 Základní teorie testování")
    st.markdown("- Typy testů: Smoke, Regrese, Unit, Integrační, Systémové, Akceptační")
    st.markdown("- Verifikace vs. Validace — děláme věci správně vs. správné věci")
    st.markdown("- Severity vs. Priorita — dopad vs. rychlost řešení")
    st.markdown("- REST/JSON vs. SOAP/XML, HTTP metody a status kódy")
    st.markdown("- SQL: DDL, DML, DQL, DCL; JOIN (INNER/LEFT/RIGHT)")

def page_qatahaky():
    st.header("🧭 QA tahák (proces + šablony)")
    st.markdown("- Příprava: cíl & rozsah, rizika, prostředí & data, DoD")
    st.markdown("- Návrh: ekvivalence, hranice, pairwise; nejdřív smoke")
    st.markdown("- Provedení: scripted + exploratory; evidence PASS/FAIL")
    bug = (
        "Název: [Checkout] 500 při prázdném košíku\\n"
        "Prostředí: test, v1.2.3, Chrome\\n"
        "Kroky: 1) Otevřít /checkout 2) Kliknout 'Zaplatit' s prázdným košíkem\\n"
        "Očekávané: Validace 'Košík je prázdný'\\n"
    )
    st.download_button("⬇️ Stáhnout Bug report", bug, file_name="bug-report.md")

def page_api_tester():
    st.header("🌐 API dokumentace + rychlý tester")
    with st.expander("📖 Demo API: JSONPlaceholder"):
        st.markdown("Base URL: https://jsonplaceholder.typicode.com  (např. GET /todos/1)")
    colA, colB = st.columns([3, 1])
    with colA:
        url = st.text_input("URL endpointu", "https://jsonplaceholder.typicode.com/todos/1")
    with colB:
        metoda = st.selectbox("Metoda", ["GET", "POST", "PUT", "PATCH", "DELETE"])
    headers_text = st.text_area("HTTP headers (Klíč: Hodnota)", "Content-Type: application/json", height=80)
    body_text = st.text_area("Request JSON body", '{\\n  "title": "Test úkol",\\n  "completed": false\\n}', height=120)
    exp1, exp2 = st.columns(2)
    with exp1:
        expected_status = st.number_input("Očekávaný status kód", value=200, step=1)
    with exp2:
        validate_json = st.checkbox("Validovat JSON odpověď", value=False)

    def parse_headers(text: str) -> dict:
        headers = {}
        for line in text.splitlines():
            if ":" in line:
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
                r = None

            if r is not None:
                st.write("Status:", r.status_code)
                if r.headers.get("Content-Type", "").startswith("application/json"):
                    try:
                        st.json(r.json())
                    except Exception:
                        st.text(r.text[:2000])
                else:
                    st.text(r.text[:2000])

                if r.status_code == int(expected_status):
                    st.success(f"PASS – status {r.status_code} = očekávaný {expected_status}")
                else:
                    st.error(f"FAIL – status {r.status_code} ≠ očekávaný {expected_status}")

                if validate_json:
                    try:
                        _ = r.json()
                        st.info("JSON odpověď vypadá validně.")
                    except Exception as e:
                        st.warning(f"JSON nelze načíst: {e}")
        except Exception as e:
            st.error(f"Chyba při volání API: {e}")

# ---------- ROUTER ----------
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
