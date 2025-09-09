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

# pomocný stav pro výstup README generátoru
st.session_state.setdefault("generated_readme", None)

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

    # ============ BLOK 1: Co je QA ============
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


def page_portfolio():
    st.header("3) Portfolio a práce")

    # --- checkboxy ---
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

    # --- Týdenní plán ---
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

    # --- Generátor README (opraveno: download mimo form) ---
    st.subheader("🧩 Generátor README.md pro miniprojekt")
    with st.form("readme_form", clear_on_submit=False):
        proj = st.text_input("Název projektu", "qa-api-tests")
        popis = st.text_area("Krátký popis", "Sada API testů pro demo službu (REST).")
        technologie = st.text_input("Technologie", "Python, pytest, requests, Postman")
        kroky = st.text_area("Jak spustit", "pip install -r requirements.txt\npytest -q")
        co_testuju = st.text_area(
            "Co se testuje",
            "- Smoke testy endpointů\n- Pozitivní/negativní scénáře\n- Validace status kódů a JSON schema"
        )
        odkaz = st.text_input("Odkaz (repo / appka)", "https://github.com/uzivatel/qa-api-tests")

        submitted = st.form_submit_button("Vygenerovat README")
        if submitted:
            md = f"""# {proj}

{popis}

## Technologie
{technologie}

## Jak spustit

