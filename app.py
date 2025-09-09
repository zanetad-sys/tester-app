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
        "Severita vs. priorita bugů",
        value=st.session_state.done.get("qa_sevpri", False),
    )

    with st.expander("📖 Vysvětlivky – QA základy"):
        st.markdown("""
- **QA** = zajištění kvality (procesy + testování).  
- **Role testera** = hledá chyby, přemýšlí za uživatele, zajišťuje, že produkt odpovídá požadavkům.  
- **SDLC** = waterfall (fáze po sobě) vs. agile (Scrum, iterace).  
- **Verifikace** = děláme věci správně, **Validace** = děláme správné věci.  
- **Severita** = dopad chyby, **Priorita** = jak rychle ji opravit.
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
# ---------- Inicializace klíčů pro stránku "Nástroje" ----------
_tools_keys = [
    "tools_jira", "tools_testmgmt",
    "tools_postman", "tools_soapui", "tools_curl",
    "tools_git",
    "tools_python", "tools_playwright", "tools_selenium", "tools_pytest", "tools_selide",
    "tools_devtools", "tools_logs",
    "tools_cicd",
    "tools_db_clients",
    "tools_docker", "tools_ide", "tools_perf",
]
for _k in _tools_keys:
    st.session_state.done.setdefault(_k, False)

def page_nastroje():
    st.header("2) Nástroje – co by měl tester znát")

    # ============== ORGANIZACE & BUG TRACKING ==============
    st.subheader("📂 Organizace & bug tracking")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.done["tools_jira"] = st.checkbox(
            "Jira / Trello / Asana / Bugzilla – evidence úkolů a bugů",
            value=st.session_state.done.get("tools_jira", False)
        )
    with c2:
        st.session_state.done["tools_testmgmt"] = st.checkbox(
            "Test management: TestRail / Xray / Zephyr / Azure DevOps / Excel/Sheets",
            value=st.session_state.done.get("tools_testmgmt", False)
        )
    with st.expander("🎓 Tipy – workflow & reporty"):
        st.markdown("""
- **Workflow:** To Do → In Progress → In Review → Done  
- **Bug report:** název, prostředí, kroky, očekávané vs. aktuální, důkazy, **Sev/Pri**  
- **Vazby:** ticket ↔️ PR/MR ↔️ test cases ↔️ release notes
""")

    st.divider()

    # ============== API & KOMUNIKACE ==============
    st.subheader("🌐 API & komunikace")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.done["tools_postman"] = st.checkbox(
            "Postman – kolekce, environmenty, test scripts",
            value=st.session_state.done.get("tools_postman", False)
        )
    with c2:
        st.session_state.done["tools_soapui"] = st.checkbox(
            "SOAP UI – testování SOAP (XML) služeb",
            value=st.session_state.done.get("tools_soapui", False)
        )
    with c3:
        st.session_state.done["tools_curl"] = st.checkbox(
            "curl – rychlé volání API v terminálu",
            value=st.session_state.done.get("tools_curl", False)
        )
    with st.expander("🎓 Tahák – HTTP & API"):
        st.code("""# GET
curl -i https://jsonplaceholder.typicode.com/todos/1

# POST (JSON body)
curl -i -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","completed":false}'
""", language="bash")

    st.divider()

    # ============== VERZOVÁNÍ ==============
    st.subheader("🔁 Verzování")
    st.session_state.done["tools_git"] = st.checkbox(
        "Git + GitHub/GitLab/Bitbucket (commity, PR/MR, code review)",
        value=st.session_state.done.get("tools_git", False)
    )
    with st.expander("🎓 Tahák – Git"):
        st.code("""git checkout -b feat/x
git add .
git commit -m "feat: x"
git push -u origin feat/x
# otevři PR/MR → review → merge
""", language="bash")

    st.divider()

    # ============== AUTOMATIZACE TESTŮ ==============
    st.subheader("🤖 Automatizace testů")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.session_state.done["tools_python"] = st.checkbox(
            "Python / Java/JS (dle firmy)",
            value=st.session_state.done.get("tools_python", False)
        )
    with c2:
        st.session_state.done["tools_playwright"] = st.checkbox(
            "Playwright (UI testy)",
            value=st.session_state.done.get("tools_playwright", False)
        )
    with c3:
        st.session_state.done["tools_selenium"] = st.checkbox(
            "Selenium (UI testy)",
            value=st.session_state.done.get("tools_selenium", False)
        )
    with c4:
        st.session_state.done["tools_pytest"] = st.checkbox(
            "pytest (spouštění, fixtures, reporty)",
            value=st.session_state.done.get("tools_pytest", False)
        )
    st.session_state.done["tools_selide"] = st.checkbox(
        "Selenium IDE? (klikací záznam – spíš na rychlé prototypy)",
        value=st.session_state.done.get("tools_selide", False)
    )

    st.divider()

    # ============== DEVTOOLS & LOGY ==============
    st.subheader("🧰 DevTools & logy")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.done["tools_devtools"] = st.checkbox(
            "Chrome/Edge DevTools (Network, Console, Storage, Cookies)",
            value=st.session_state.done.get("tools_devtools", False)
        )
    with c2:
        st.session_state.done["tools_logs"] = st.checkbox(
            "Logy: application/system/security (např. logcat, journald, server logy)",
            value=st.session_state.done.get("tools_logs", False)
        )
    with st.expander("🎓 K čemu logy?"):
        st.markdown("""
- **Application**: stack trace, chybové hlášky, custom logy  
- **System/journald**: služby, paměť, síť  
- **Security**: přihlášení, 403/401, audit
""")

    st.divider()

    # ============== CI/CD ==============
    st.subheader("⚙️ CI/CD")
    st.session_state.done["tools_cicd"] = st.checkbox(
        "GitHub Actions / GitLab CI – spouštět testy po commitu",
        value=st.session_state.done.get("tools_cicd", False)
    )
    with st.expander("🎓 Příklad (GitHub Actions – pytest)"):
        st.code("""# .github/workflows/tests.yml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: pytest -q
""", language="yaml")

    st.divider()

    # ============== DATABÁZE ==============
    st.subheader("🗄️ Databáze")
    st.session_state.done["tools_db_clients"] = st.checkbox(
        "DBeaver / pgAdmin / MySQL Workbench (GUI pro SQL)",
        value=st.session_state.done.get("tools_db_clients", False)
    )
    with st.expander("🎓 Jak do toho zapadá MySQL, MS SQL, Oracle, PHP?"):
        st.markdown("""
- **MySQL, PostgreSQL, MS SQL, Oracle** = **SŘBD** (databázové servery).  
- **DBeaver/pgAdmin/MySQL Workbench** = **GUI klienti** pro práci s těmito DB.  
- **SQL** je jazyk dotazů (SELECT/INSERT/UPDATE/DELETE, JOINy).  
- **PHP** je **programovací jazyk** pro backend – přes SQL driver se připojí k DB (stejně jako Python/Java/JS).
""")

    st.divider()

    # ============== DOPLŇKOVÉ ==============
    st.subheader("🧩 Doplňkové")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.done["tools_docker"] = st.checkbox(
            "Docker – lokální dev/test prostředí",
            value=st.session_state.done.get("tools_docker", False)
        )
    with c2:
        st.session_state.done["tools_ide"] = st.checkbox(
            "IDE: VS Code / PyCharm (debugging, linting)",
            value=st.session_state.done.get("tools_ide", False)
        )
    with c3:
        st.session_state.done["tools_perf"] = st.checkbox(
            "Výkonnostní testy: JMeter / k6 (aspoň základy)",
            value=st.session_state.done.get("tools_perf", False)
        )

    st.divider()

    # ============== Export checklistu ==============
    chosen = [
        k for k, v in st.session_state.done.items()
        if k.startswith("tools_") and v
    ]
    text = "Nástroje – splněno:\n" + "\n".join(f"- {x}" for x in chosen) if chosen else "Zatím nic nezaškrtnuto."
    st.download_button("⬇️ Stáhnout checklist nástrojů (TXT)", text, "nastroje-checklist.txt")


    st.divider()

    # ============== API & KOMUNIKACE ==============
    st.subheader("🌐 API & komunikace")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.done["tools_postman"] = st.checkbox(
            "Postman – kolekce, environmenty, test scripts",
            value=st.session_state.done["tools_postman"]
        )
    with c2:
        st.session_state.done["tools_soapui"] = st.checkbox(
            "SOAP UI – testování SOAP (XML) služeb",
            value=st.session_state.done["tools_soapui"]
        )
    with c3:
        st.session_state.done["tools_curl"] = st.checkbox(
            "curl – rychlé volání API v terminálu",
            value=st.session_state.done["tools_curl"]
        )
    with st.expander("🎓 Tahák – HTTP & API"):
        st.code("""# GET
curl -i https://jsonplaceholder.typicode.com/todos/1

# POST (JSON body)
curl -i -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","completed":false}'
""", language="bash")

    st.divider()

    # ============== VERZOVÁNÍ ==============
    st.subheader("🔁 Verzování")
    st.session_state.done["tools_git"] = st.checkbox(
        "Git + GitHub/GitLab/Bitbucket (commity, PR/MR, code review)",
        value=st.session_state.done["tools_git"]
    )
    with st.expander("🎓 Tahák – Git"):
        st.code("""git checkout -b feat/x
git add .
git commit -m "feat: x"
git push -u origin feat/x
# otevři PR/MR → review → merge
""", language="bash")

    st.divider()

    # ============== AUTOMATIZACE TESTŮ ==============
    st.subheader("🤖 Automatizace testů")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.session_state.done["tools_python"] = st.checkbox(
            "Python / (Java/JS dle firmy)",
            value=st.session_state.done["tools_python"]
        )
    with c2:
        st.session_state.done["tools_playwright"] = st.checkbox(
            "Playwright (UI testy)",
            value=st.session_state.done["tools_playwright"]
        )
    with c3:
        st.session_state.done["tools_selenium"] = st.checkbox(
            "Selenium (UI testy)",
            value=st.session_state.done["tools_selenium"]
        )
    with c4:
        st.session_state.done["tools_pytest"] = st.checkbox(
            "pytest (spouštění, fixtures, reporty)",
            value=st.session_state.done["tools_pytest"]
        )
    st.session_state.done["tools_selide"] = st.checkbox(
        "Selenium IDE? (základní klikací záznam – spíš na rychlé prototypy)",
        value=st.session_state.done["tools_selide"]
    )

    st.divider()

    # ============== DEVTOOLS & LOGY ==============
    st.subheader("🧰 DevTools & logy")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.done["tools_devtools"] = st.checkbox(
            "Chrome/Edge DevTools (Network, Console, Storage, Cookies)",
            value=st.session_state.done["tools_devtools"]
        )
    with c2:
        st.session_state.done["tools_logs"] = st.checkbox(
            "Logy: application/system/security (např. logcat, journald, server logy)",
            value=st.session_state.done["tools_logs"]
        )
    with st.expander("🎓 K čemu logy?"):
        st.markdown("""
- **Application**: stack trace, chybové hlášky, custom logy  
- **System/journald**: služby, paměť, síť  
- **Security**: přihlášení, 403/401, audit
""")

    st.divider()

    # ============== CI/CD ==============
    st.subheader("⚙️ CI/CD")
    st.session_state.done["tools_cicd"] = st.checkbox(
        "GitHub Actions / GitLab CI – spouštět testy po commitu",
        value=st.session_state.done["tools_cicd"]
    )
    with st.expander("🎓 Příklad (GitHub Actions – pytest)"):
        st.code("""# .github/workflows/tests.yml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: pytest -q
""", language="yaml")

    st.divider()

    # ============== DATABÁZE ==============
    st.subheader("🗄️ Databáze")
    st.session_state.done["tools_db_clients"] = st.checkbox(
        "DBeaver / pgAdmin / MySQL Workbench (GUI pro SQL)",
        value=st.session_state.done["tools_db_clients"]
    )
    with st.expander("🎓 Jak do toho zapadá MySQL, MS SQL, Oracle, PHP?"):
        st.markdown("""
- **MySQL, PostgreSQL, MS SQL, Oracle** = **SŘBD** (databázové servery).  
- **DBeaver/pgAdmin/MySQL Workbench** = **GUI klienti** pro práci s těmito DB.  
- **SQL** je jazyk dotazů (SELECT/INSERT/UPDATE/DELETE, JOINy).  
- **PHP** je **programovací jazyk** pro backend – může se přes **SQL driver** připojit k DB (stejně jako Python/Java/JS).
""")

    st.divider()

    # ============== DOPLŇKOVÉ ==============
    st.subheader("🧩 Doplňkové")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.done["tools_docker"] = st.checkbox(
            "Docker – lokální dev/test prostředí",
            value=st.session_state.done["tools_docker"]
        )
    with c2:
        st.session_state.done["tools_ide"] = st.checkbox(
            "IDE: VS Code / PyCharm (debugging, linting)",
            value=st.session_state.done["tools_ide"]
        )
    with c3:
        st.session_state.done["tools_perf"] = st.checkbox(
            "Výkonnostní testy: JMeter / k6 (aspoň základy)",
            value=st.session_state.done["tools_perf"]
        )

    st.divider()

    # ============== Export checklistu ==============
    chosen = [label for label, done in st.session_state.done.items()
              if label.startswith("tools_") and done]
    text = "Nástroje – splněno:\n" + "\n".join(f"- {x}" for x in chosen) if chosen else "Zatím nic nezaškrtnuto."
    st.download_button("⬇️ Stáhnout checklist nástrojů (TXT)", text, "nastroje-checklist.txt")


def page_portfolio():
    st.header("3) Portfolio a práce")

    # --- tvoje původní checkboxy (bezpečné čtení přes .get) ---
    st.session_state.done["projects"] = st.checkbox(
        "Miniprojekty na GitHubu",
        value=st.session_state.done.get("projects", False),
    )
    st.session_state.done["readme"] = st.checkbox(
        "README a ukázkové bug reporty",
        value=st.session_state.done.get("readme", False),
    )
    st.session_state.done["cv"] = st.checkbox(
        "CV + LinkedIn – zdůraznit praxi",
        value=st.session_state.done.get("cv", False),
    )

    st.info(
        "Tip: Každý projekt = jeden konkrétní skill. Krátký, ale čitelný README a pár kvalitních bug reportů "
        "mají větší hodnotu než obří repo bez popisu."
    )

    st.divider()

    # --- Týdenní plán (TVŮJ PŮVODNÍ KÓD – nechaný beze změn) ---
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

    st.divider()

    # --- Generátor README pro miniprojekt ---
    st.subheader("🧩 Generátor README.md pro miniprojekt")
    with st.form("readme_form"):
        proj = st.text_input("Název projektu", "qa-api-tests")
        popis = st.text_area("Krátký popis", "Sada API testů pro demo službu (REST).")
        technologie = st.text_input("Technologie", "Python, pytest, requests, Postman")
        kroky = st.text_area("Jak spustit", "pip install -r requirements.txt\npytest -q")
        co_testuju = st.text_area(
            "Co se testuje",
            "- Smoke testy endpointů\n- Pozitivní/negativní scénáře\n- Validace status kódů a JSON schema"
        )
        odkaz = st.text_input("Odkaz (repo / appka)", "https://github.com/uzivatel/qa-api-tests")
        submit_readme = st.form_submit_button("Vygenerovat README")
        if submit_readme:
            md = f"""# {proj}

{popis}

## Technologie
{technologie}

## Jak spustit

## Co se testuje
{co_testuju}

## Odkazy
- Repo/App: {odkaz}
"""
            st.code(md, language="markdown")
            st.download_button("⬇️ Stáhnout README.md", md, file_name="README.md")

    st.divider()

    # --- Šablony ke stažení (bug report, test case) ---
    st.subheader("📑 Šablony do portfolia")
    bug = """Název: [Checkout] 500 při prázdném košíku
Prostředí: test, v1.2.3 (build #456), Chrome 127
Kroky: 1) Otevřít /checkout 2) Kliknout „Zaplatit“ s prázdným košíkem
Očekávané: Validace „Košík je prázdný“
Aktuální: HTTP 500, bílá stránka
Důkazy: screenshot.png, network.har
Sev/Pri: High / P1  Pozn.: Regrese od v1.2.2
"""
    tc = """ID: TC-LOGIN-001
Cíl: Přihlášení validního uživatele
Kroky: 1) Otevřít /login  2) Vyplnit platné údaje  3) Odeslat
Očekávané: Přesměrování na /dashboard
Priorita: P1  Data: user@test.com / *****  Stav: PASS/FAIL
"""
    st.download_button("⬇️ Stáhnout Bug report (MD)", bug, file_name="bug-report.md")
    st.download_button("⬇️ Stáhnout Test Case (MD)", tc, file_name="test-case.md")

    st.divider()

    # --- Nápady na miniprojekty + checklist export ---
    st.subheader("💡 Nápady na miniprojekty")
    st.markdown("""
- **API testy**: kolekce v Postmanu + README (JSONPlaceholder/Swagger Petstore)  
- **UI testy**: 3–5 scénářů v Playwrightu (login, košík, vyhledávání)  
- **SQL cvičení**: složka `sql/` se záznamy dotazů + vysvětlení  
- **DevTools**: analýza `Network` pro 1 scénář (screenshoty, popis)  
- **Logy**: krátký článek „co jsem našla v application logu při chybě 500“
""")

    chosen = [k for k, v in st.session_state.done.items() if k in ("projects", "readme", "cv") and v]
    text = "Portfolio – splněno:\n" + "\n".join(f"- {x}" for x in chosen) if chosen else "Zatím nic nezaškrtnuto."
    st.download_button("⬇️ Stáhnout checklist portfolia (TXT)", text, "portfolio-checklist.txt")

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
    st.header("📚 Užitečné zdroje – kurátorský seznam")

    st.markdown("#### Git & GitHub")
    st.markdown("""
- [Pro Git (kniha zdarma)](https://git-scm.com/book/en/v2)  
- [Atlassian Git Tutorials (větve, rebase, workflow)](https://www.atlassian.com/git)  
- [GitHub Docs – Pull Requests](https://docs.github.com/pull-requests)  
- [Oh My Git! (interaktivní hra)](https://ohmygit.org/)  
- [Learn Git Branching (vizuální trénink větví)](https://learngitbranching.js.org/)
""")

    st.markdown("#### Markdown, README, dokumentace")
    st.markdown("""
- [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/)  
- [Readme.so (WYSIWYG editor README)](https://readme.so/)
""")

    st.markdown("#### Web základy (HTML/CSS/JS)")
    st.markdown("""
- [MDN Web Docs – HTML](https://developer.mozilla.org/docs/Web/HTML)  
- [MDN Web Docs – CSS](https://developer.mozilla.org/docs/Web/CSS)  
- [MDN Web Docs – JavaScript](https://developer.mozilla.org/docs/Web/JavaScript)  
- [Flexbox Froggy (hra na layout)](https://flexboxfroggy.com/)  
- [Grid Garden (CSS Grid)](https://cssgridgarden.com/)
""")

    st.markdown("#### SQL & databáze")
    st.markdown("""
- [SQLBolt (interaktivní lekce)](https://sqlbolt.com/)  
- [Mode SQL Tutorial (praktické dotazy)](https://mode.com/sql-tutorial/)  
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)  
- [Database Normalization (přehled)](https://www.guru99.com/database-normalization.html)
""")

    st.markdown("#### API, HTTP & Postman")
    st.markdown("""
- [HTTP status codes – přehled](https://httpstatuses.com/)  
- [Postman Learning Center](https://learning.postman.com/)  
- [JSONPlaceholder (testovací REST API)](https://jsonplaceholder.typicode.com/)  
- [Swagger Petstore (OpenAPI demo)](https://petstore.swagger.io/)  
- [SOAP UI – dokumentace](https://www.soapui.org/)
""")

    st.markdown("#### Python, testy a automatizace")
    st.markdown("""
- [Python Tutorial (oficiální)](https://docs.python.org/3/tutorial/)  
- [pytest – dokumentace](https://docs.pytest.org/)  
- [Playwright for Python](https://playwright.dev/python/)  
- [Selenium Docs](https://www.selenium.dev/documentation/)  
- [Awesome Python Testing (sbírka zdrojů)](https://github.com/atinfo/awesome-test-automation)
""")

    st.markdown("#### DevTools, logy, Linux")
    st.markdown("""
- [Chrome DevTools – Overview](https://developer.chrome.com/docs/devtools)  
- [Logy v Linuxu (journald)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html)  
- [Explainshell (co dělá příkaz)](https://explainshell.com/)
""")

    st.markdown("#### CI/CD")
    st.markdown("""
- [GitHub Actions – docs](https://docs.github.com/actions)  
- [GitLab CI/CD – docs](https://docs.gitlab.com/ee/ci/)
""")

    st.markdown("#### Docker & prostředí")
    st.markdown("""
- [Docker – Get Started](https://docs.docker.com/get-started/)  
- [Play with Docker (online sandbox)](https://labs.play-with-docker.com/)
""")

    st.markdown("#### Bezpečnost & výkon")
    st.markdown("""
- [PortSwigger Web Security Academy (XSS, SQLi…)](https://portswigger.net/web-security)  
- [OWASP Top 10 (nejčastější rizika)](https://owasp.org/www-project-top-ten/)  
- [k6 – performance testing](https://k6.io/docs/)  
- [Apache JMeter – User Manual](https://jmeter.apache.org/usermanual/)
""")

    st.markdown("#### Streamlit")
    st.markdown("""
- [Streamlit – dokumentace](https://docs.streamlit.io/)  
- [Gallery (inspirace aplikací)](https://streamlit.io/gallery)
""")

    # Volitelně: stáhnout si seznam jako Markdown
    resources_md = """
# Užitečné zdroje (QA starter pack)
- Git & GitHub: Pro Git, Atlassian Git Tutorials, PR workflow…
- Web: MDN (HTML/CSS/JS), Flexbox Froggy, Grid Garden
- SQL: SQLBolt, Mode SQL, Normalizace
- API: HTTP status codes, Postman LC, Swagger Petstore, JSONPlaceholder
- Python/Testing: Python tutorial, pytest, Playwright, Selenium
- DevTools/Logy: Chrome DevTools, journald
- CI/CD: GitHub Actions, GitLab CI
- Docker: Get Started, Play with Docker
- Security/Performance: PortSwigger Academy, OWASP Top 10, k6, JMeter
- Streamlit: Docs, Gallery
"""
    st.download_button("⬇️ Stáhnout seznam zdrojů (Markdown)", resources_md, file_name="uzitecne-zdroje.md")

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

