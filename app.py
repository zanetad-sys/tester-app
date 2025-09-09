import json
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Jak se stát testerem", page_icon="✅", layout="wide")

# ========== STAV (checkboxy) ==========
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

# ========== MENU V SIDEBARU ==========
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

# ========== STRÁNKY ==========
def page_uvod():
    st.title("Jak se stát testerem – mini průvodce")
    st.write("Postupně a v klidu. Základy a praxe. Zaškrtávej splněné kroky a sleduj postup.")
    col1, col2 = st.columns([1, 2], vertical_alignment="center")
    with col1:
        st.metric("Splněno", f"{percent()} %")
        if st.button("Resetuj postup"):
            for k in st.session_state.done:
                st.session_state.done[k] = False
            st.rerun()
    with col2:
        st.info("Tip: Používej menu vlevo. Každá sekce se zobrazí tady v hlavní části.")

def page_zaklady():
    st.header("1) Základy QA – kompletní přehled")

    # ============ BLOK 1: Co je QA =============
    st.subheader("🎯 Co je QA a role testera")
    st.session_state.done["qa_definition"] = st.checkbox(
        "Co je testování / QA",
        value=st.session_state.done.get("qa_definition", False),
    )
    st.session_state.done["qa_roles"] = st.checkbox(
        "Role: tester vs. vývojář vs. produkták",
        value=st.session_state.done.get("qa_roles", False),
    )
    st.session_state.done["qa_sdlc"] = st.checkbox(
        "Životní cyklus vývoje softwaru (SDLC, agilní, waterfall)",
        value=st.session_state.done.get("qa_sdlc", False),
    )
    st.session_state.done["qa_types"] = st.checkbox(
        "Typy testů – úrovně (unit, integrační, systémové, akceptační)",
        value=st.session_state.done.get("qa_types", False),
    )
    st.session_state.done["qa_vv"] = st.checkbox(
        "Rozdíl mezi verifikací a validací",
        value=st.session_state.done.get("qa_vv", False),
    )
    st.session_state.done["qa_sevpri"] = st.checkbox(
        "Severity vs. priorita bugů",
        value=st.session_state.done.get("qa_sevpri", False),
    )

    with st.expander("📖 Vysvětlivky – QA základy"):
        st.markdown("""
- **QA** = zajištění kvality (procesy + testování).  
- **Role testera** = hledá chyby, přemýšlí za uživatele, zajišťuje, že produkt odpovídá požadavkům.  
- **SDLC** = waterfall (fáze po sobě) vs. agile (Scrum, iterace).  
- **Verifikace** = děláme věci správně, **Validace** = děláme správné věci.  
- **Severity** = dopad chyby, **Priorita** = jak rychle ji opravit.
""")

    st.divider()

    # ============ BLOK 2: Technické minimum ============
    st.subheader("🖥️ Technické minimum")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.done["tech_web"] = st.checkbox(
            "Web (HTML, CSS, JS)", value=st.session_state.done.get("tech_web", False)
        )
        st.session_state.done["tech_sql"] = st.checkbox(
            "Databáze + SQL", value=st.session_state.done.get("tech_sql", False)
        )
    with col2:
        st.session_state.done["tech_git"] = st.checkbox(
            "Git/GitHub", value=st.session_state.done.get("tech_git", False)
        )
        st.session_state.done["tech_logs"] = st.checkbox(
            "Logy (application/system/security)",
            value=st.session_state.done.get("tech_logs", False),
        )
    with col3:
        st.session_state.done["tech_http"] = st.checkbox(
            "HTTP/HTTPS základy", value=st.session_state.done.get("tech_http", False)
        )
        st.session_state.done["tech_api"] = st.checkbox(
            "API (REST/JSON, SOAP/XML)",
            value=st.session_state.done.get("tech_api", False),
        )

    with st.expander("📖 Vysvětlivky – Technické minimum"):
        st.markdown("""
- **Web** = HTML struktura, CSS styly, JS logika.  
- **SQL** = SELECT, JOIN, INSERT, UPDATE, klíče.  
- **Git** = commit, push, pull request.  
- **Logy** = application (chyby appky), system (OS, služby), security (přihlášení).  
- **HTTP** = request/response, status kódy (200, 404, 500).  
- **API** = REST (JSON, lehké), SOAP (XML, enterprise).
""")

    st.divider()

    # ============ BLOK 3: Praktické nástroje ============
    st.subheader("🛠️ Praktické nástroje")
    st.session_state.done["tools_bugtracking"] = st.checkbox(
        "Bug tracking (Jira, Trello, Bugzilla)",
        value=st.session_state.done.get("tools_bugtracking", False),
    )
    st.session_state.done["tools_testmgmt"] = st.checkbox(
        "Test management (TestRail, Xray, Excel šablony)",
        value=st.session_state.done.get("tools_testmgmt", False),
    )
    st.session_state.done["tools_postman"] = st.checkbox(
        "Postman (API testing) / SOAP UI",
        value=st.session_state.done.get("tools_postman", False),
    )
    st.session_state.done["tools_devtools"] = st.checkbox(
        "DevTools v prohlížeči (network, console, cookies)",
        value=st.session_state.done.get("tools_devtools", False),
    )

    with st.expander("📖 Vysvětlivky – Praktické nástroje"):
        st.markdown("""
- **Jira/Trello** = evidence úkolů a bugů.  
- **TestRail/Xray/Excel** = správa testů a výsledků.  
- **Postman/SOAP UI** = testování API.  
- **DevTools** = prohlížení síťových požadavků, logů a cookies.
""")

    st.divider()

    # ============ BLOK 4: Automatizace + Bonus ============
    st.subheader("🤖 Automatizace + Bonus")
    st.session_state.done["auto_python"] = st.checkbox(
        "Základy Pythonu/jiného jazyka",
        value=st.session_state.done.get("auto_python", False),
    )
    st.session_state.done["auto_framework"] = st.checkbox(
        "Framework (pytest, Playwright, Selenium)",
        value=st.session_state.done.get("auto_framework", False),
    )
    st.session_state.done["auto_ci"] = st.checkbox(
        "Principy CI/CD (GitHub Actions, GitLab CI)",
        value=st.session_state.done.get("auto_ci", False),
    )
    st.session_state.done["bonus_security"] = st.checkbox(
        "Základy bezpečnostního testování (XSS, SQLi)",
        value=st.session_state.done.get("bonus_security", False),
    )
    st.session_state.done["bonus_performance"] = st.checkbox(
        "Performance testy (JMeter, k6 – teorie)",
        value=st.session_state.done.get("bonus_performance", False),
    )
    st.session_state.done["bonus_cloud"] = st.checkbox(
        "Cloud/prostředí (docker, staging vs. prod)",
        value=st.session_state.done.get("bonus_cloud", False),
    )
    st.session_state.done["bonus_linux"] = st.checkbox(
        "Základy Linux shellu (navigace, grep, logy)",
        value=st.session_state.done.get("bonus_linux", False),
    )

    with st.expander("📖 Vysvětlivky – Automatizace a Bonus"):
        st.markdown("""
- **Python/Java** = základní syntaxe, funkce, testovací skripty.  
- **Pytest/Playwright/Selenium** = frameworky pro automatizaci.  
- **CI/CD** = kontinuální integrace a nasazování (např. GitHub Actions).  
- **Security** = základní útoky jako XSS, SQLi na demo aplikacích.  
- **Performance** = JMeter, k6 pro zátěžové testy.  
- **Cloud** = docker, prostředí dev/stage/prod.  
- **Linux** = práce v shellu, logy, grep.
""")

    # Checklist download
    all_items = [k for k, v in st.session_state.done.items() if k.startswith(("qa_", "tech_", "tools_", "auto_", "bonus_"))]
    checklist = "\n".join(f"- {k}" for k in all_items)
    st.download_button("⬇️ Stáhnout checklist všech základů", checklist, "qa-zaklady-checklist.txt")


def page_nastroje():
    st.header("2) Nástroje a praxe")
    st.session_state.done["jira"] = st.checkbox(
        "Jira/Trello – evidence úkolů",
        value=st.session_state.done["jira"],
    )
    st.session_state.done["testcases"] = st.checkbox(
        "Test cases a bug reporting",
        value=st.session_state.done["testcases"],
    )
    st.session_state.done["api"] = st.checkbox(
        "API testování (Postman)",
        value=st.session_state.done["api"],
    )
    st.session_state.done["auto"] = st.checkbox(
        "Automatizace – Python + Playwright/pytest",
        value=st.session_state.done["auto"],
    )

def page_portfolio():
    st.header("3) Portfolio a práce")
    st.session_state.done["projects"] = st.checkbox(
        "Miniprojekty na GitHubu",
        value=st.session_state.done["projects"],
    )
    st.session_state.done["readme"] = st.checkbox(
        "README a ukázkové bug reporty",
        value=st.session_state.done["readme"],
    )
    st.session_state.done["cv"] = st.checkbox(
        "CV + LinkedIn – zdůraznit praxi",
        value=st.session_state.done["cv"],
    )

    st.divider()
    with st.form("plan"):
        st.subheader("🗺️ Týdenní plán")
        jmeno = st.text_input("Jméno (volitelné)", "")
        hodin = st.slider("Kolik hodin týdně zvládneš?", 1, 20, 5)
        fokus = st.selectbox(
            "Hlavní fokus na týden",
            ["Základy", "API testování", "Automatizace", "Portfolio/README"],
        )
        submit = st.form_submit_button("Vygenerovat plán")
        if submit:
            body = {
                "Základy": [
                    "• 2 h Git + GitHub",
                    "• 2 h HTML/CSS/JS",
                    "• 1 h SQL",
                ],
                "API testování": [
                    "• 2 h Postman základy",
                    "• 2 h psaní requestů",
                    "• 1 h dokumentace",
                ],
                "Automatizace": [
                    "• 2 h Python",
                    "• 2 h Playwright/pytest",
                    "• 1 h refaktor",
                ],
                "Portfolio/README": [
                    "• 2 h README + ukázky",
                    "• 2 h miniprojekt",
                    "• 1 h polishing",
                ],
            }
            st.success((f"{jmeno}, " if jmeno else "") + f"tvůj plán na {hodin} h/týden:")
            st.write("\n".join(body[fokus]))

def page_kviz():
    st.header("🧩 Mini kvíz")
    odp = st.radio(
        "Co je Pull Request (PR) na GitHubu?",
        [
            "Přímé nahrání kódu do main",
            "Návrh změn z větve, který ostatní zkontrolují a sloučí",
            "Záloha repozitáře",
        ],
    )
    if st.button("Vyhodnotit"):
        if odp == "Návrh změn z větve, který ostatní zkontrolují a sloučí":
            st.success("Správně! 👍")
        else:
            st.error("Ještě jednou: PR je návrh změn z větve, který se po schválení mergne do main.")

def page_timeline():
    st.header("🗓️ Doporučená timeline")
    timeline = pd.DataFrame(
        {
            "Týden": ["1", "2", "3", "4"],
            "Fokus": ["Základy + Git", "API testování", "Automatizace", "Portfolio/README"],
        }
    )
    st.table(timeline)

def page_zdroje():
    st.header("📚 Užitečné zdroje")
    zdroje = pd.DataFrame(
        {
            "Téma": ["Git", "Postman (API)", "Playwright", "Streamlit"],
            "Tip": [
                "Procházej vlastní repozitáře a dělej malé commity.",
                "Trénuj collection + environment + test scripts.",
                "Začni s UI testy, pak přidej fixtures a parametrizaci.",
                "Rychlé prototypy a dashboardy – tak jako tahle appka!",
            ],
        }
    )
    st.dataframe(zdroje, use_container_width=True)

def page_teorie():
    st.header("📖 Základní teorie testování")

    st.subheader("Typy testů")
    st.markdown("""
- **Funkční** vs. **Nefunkční**  
- **Smoke**, **Sanity**, **Regresní**  
- **Jednotkové (unit)**, **Integrační**, **Systémové**, **Akceptační**
""")

    st.subheader("Verifikace vs. Validace")
    st.markdown("""
- **Verifikace** = Ověřuji, zda produkt odpovídá specifikaci (*Stavíme správně?*).  
- **Validace** = Ověřuji, zda produkt splňuje potřeby uživatele (*Stavíme správnou věc?*).
""")

    st.subheader("Severity vs. Priorita")
    st.markdown("""
- **Severity** = jak vážná je chyba (dopad).  
- **Priorita** = jak rychle se má opravit (pořadí práce).
""")

    st.subheader("Bug vs. Defect vs. Failure")
    st.markdown("""
- **Bug** = chyba nalezená při testování.  
- **Defect** = nesoulad se specifikací (většinou v kódu).  
- **Failure** = projev chyby v běžícím systému.
""")

    st.subheader("API základy")
    st.markdown("""
- **API** = rozhraní pro komunikaci mezi systémy.  
- **HTTP metody**: GET, POST, PUT, PATCH, DELETE  
- **Status kódy**: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Server Error  
- **REST + JSON** (lehké, běžné), **SOAP + XML** (formálnější, často enterprise).
""")

    st.subheader("Metody testování (Black/White/Gray box)")
    st.markdown("""
- **Blackbox** = testuji vstupy/výstupy, neřeším kód.  
- **Whitebox** = znám vnitřní strukturu kódu.  
- **Graybox** = něco z obou (např. znáš schémata DB, logiku).
""")

    st.subheader("SQL – základy")
    st.markdown("""
- **DDL**: `CREATE`, `ALTER`, `DROP`  
- **DML**: `INSERT`, `UPDATE`, `DELETE`  
- **DQL**: `SELECT`  
- **DCL**: `GRANT`, `REVOKE`  
- **JOIN**: `INNER`, `LEFT`, `RIGHT`  
- **Primární klíč** = jednoznačný identifikátor záznamu  
- **Cizí klíč** = odkaz na primární klíč jiné tabulky
""")

    st.subheader("Logy – typy")
    st.markdown("""
- **Application log** (chyby v aplikaci)  
- **System log** (OS, služby)  
- **Security log** (přihlášení, audit)
""")

    st.subheader("BDD – Behavior Driven Development")
    st.markdown("""
**Given** (předpoklad) – **When** (akce) – **Then** (výsledek)

Příklad:  
*Given uživatel je přihlášen*  
*When klikne na „Odhlásit“*  
*Then systém ho odhlásí a přesměruje na login stránku*.
""")

def page_qatahaky():
    st.header("🧭 QA tahák (proces + šablony)")
    st.markdown("Rychlé taháky pro praxi testera. Stáhni si šablony a používej ve svých projektech.")

    st.markdown("### 0) Příprava")
    st.write("""
- **Cíl & rozsah**, **Rizika/priorita**, **Prostředí & data**, **DoD**
""")
    st.markdown("### 1) Návrh testů")
    st.write("""
- Techniky: ekvivalence, hranice, stavové přechody, pairwise  
- Úrovně: unit/API/UI; typy: funkční, negativní, regresní, smoke  
- Minimal viable set: nejdřív **smoke**, pak kritické cesty, pak okraje  
""")
    st.markdown("### 2) Provedení")
    st.write("""
- Scripted + Exploratory ~ 70/30 (timebox 30–60 min)  
- Evidence: PASS/FAIL, screenshot/log/HAR u failů  
- Verzování: drž v Gitu (README, `tests/`, `testcases.xlsx`)  
""")
    st.markdown("### 3) Bug report – šablona")
    bug = """Název: [Checkout] 500 při prázdném košíku
Prostředí: test, v1.2.3 (build #456), Chrome 127
Kroky: 1) Otevřít /checkout 2) Kliknout „Zaplatit“ s prázdným košíkem
Očekávané: Validace „Košík je prázdný“
Aktuální: HTTP 500, bílá stránka
Důkazy: screenshot.png, network.har
Sev/Pri: High / P1  Pozn.: Regrese od v1.2.2
"""
    st.code(bug, language="markdown")
    st.download_button("⬇️ Stáhnout Bug report", bug, file_name="bug-report.md")

    st.markdown("### Test case – šablona")
    tc = """ID: TC-LOGIN-001
Cíl: Přihlášení validního uživatele
Kroky: 1) Otevřít /login  2) Vyplnit platné údaje  3) Odeslat
Očekávané: Přesměrování na /dashboard
Priorita: P1  Data: user@test.com / *****  Stav: PASS/FAIL
"""
    st.code(tc, language="markdown")
    st.download_button("⬇️ Stáhnout Test Case", tc, file_name="test-case.md")

    st.markdown("### PR checklist")
    pr = """PR checklist:
- [ ] Projde lokální smoke
- [ ] Test data/seed aktualizovány
- [ ] Přidané/změněné testy
- [ ] Bezpečnostní dopad zhodnocen
- [ ] Aktualizován README/CHANGELOG
"""
    st.code(pr, language="markdown")
    st.download_button("⬇️ Stáhnout PR checklist", pr, file_name="pr-checklist.md")

def page_api_tester():
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

    colA, colB = st.columns([3, 1])
    with colA:
        url = st.text_input("URL endpointu", "https://jsonplaceholder.typicode.com/todos/1")
    with colB:
        metoda = st.selectbox("Metoda", ["GET", "POST", "PUT", "PATCH", "DELETE"])

    hdrs_default = "Content-Type: application/json"
    headers_text = st.text_area("HTTP headers (Klíč: Hodnota na řádek)", hdrs_default, height=80)
    body_text = st.text_area("Request JSON body (pro POST/PUT/PATCH)", '{\n  "title": "Test úkol",\n  "completed": false\n}', height=140)

    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        expected_status = st.number_input("Očekávaný status kód", value=200, step=1)
    with exp_col2:
        validate_json = st.checkbox("Validovat JSON odpověď", value=False)

    def parse_headers(text: str) -> dict:
        headers = {}
        for line in text.splitlines():
            if not line.strip() or ":" not in line:
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
                r = None
                st.error("Neznámá metoda.")

            if r is not None:
                st.write("**Status kód:**", r.status_code)
                if r.headers.get("Content-Type", "").startswith("application/json"):
                    try:
                        st.json(r.json())
                    except Exception:
                        st.text(r.text[:2000])
                else:
                    st.text(r.text[:2000])

                # jednoduché PASS/FAIL
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

# ========== ROUTER ==========
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

