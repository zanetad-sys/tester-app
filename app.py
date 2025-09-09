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
  max-width: 1600px;
  padding-left: 2rem;
  padding-right: 2rem;
}
main .block-container {
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

# Sidebar
st.sidebar.markdown("<h2>📚 Navigace</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("", titles, index=0)

# === BANNER OBRÁZEK NAD OBSAHEM ===
st.image(
    "https://i.ibb.co/vZnMZ5X/junior-tester-banner.jpg",
    use_container_width=True
)
# ===================== STRÁNKY =====================
def page_uvod():
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
        value=st.session_state.done["manual_vs_auto"],
    )
    st.session_state.done["web_basics"] = st.checkbox(
        "Základy webu (HTML/CSS/JS)",
        value=st.session_state.done["web_basics"],
    )
    st.session_state.done["sql"] = st.checkbox(
        "Základy SQL",
        value=st.session_state.done["sql"],
    )
    st.session_state.done["git"] = st.checkbox(
        "Verzování (Git) a GitHub",
        value=st.session_state.done["git"],
    )
    st.session_state.done["testing_basics"] = st.checkbox(
        "Základy testování (bug, testcase, regression, smoke)",
        value=st.session_state.done.get("testing_basics", False),
    )
    st.session_state.done["sdlc"] = st.checkbox(
        "Životní cyklus SW (SDLC/STLC)",
        value=st.session_state.done.get("sdlc", False),
    )
    st.session_state.done["agile"] = st.checkbox(
        "Agile / Scrum základy",
        value=st.session_state.done.get("agile", False),
    )
    st.session_state.done["logs"] = st.checkbox(
        "Základy práce s logy",
        value=st.session_state.done.get("logs", False),
    )
    st.session_state.done["linux"] = st.checkbox(
        "Základy Linux/CLI",
        value=st.session_state.done.get("linux", False),
    )
    st.session_state.done["networks"] = st.checkbox(
        "Základy sítí (HTTP, DNS, IP)",
        value=st.session_state.done.get("networks", False),
    )
    st.session_state.done["static_dynamic"] = st.checkbox(
        "Statické vs. dynamické testování – chápu rozdíl",
        value=st.session_state.done.get("static_dynamic", False),
    )

def page_nastroje():
    st.header("2) Nástroje a praxe")

    st.subheader("Tracking & správa")
    st.session_state.done["jira"] = st.checkbox(
        "Jira / Trello – evidence úkolů a bugů",
        value=st.session_state.done["jira"],
    )
    st.session_state.done["testrail"] = st.checkbox(
        "TestRail / Zephyr – správa test cases",
        value=st.session_state.done.get("testrail", False),
    )
    st.session_state.done["confluence"] = st.checkbox(
        "Confluence / Notion – dokumentace",
        value=st.session_state.done.get("confluence", False),
    )

    st.subheader("API testování")
    st.session_state.done["api"] = st.checkbox(
        "Postman – tvorba a spouštění requestů",
        value=st.session_state.done["api"],
    )
    st.session_state.done["insomnia"] = st.checkbox(
        "Insomnia / alternativní API klient",
        value=st.session_state.done.get("insomnia", False),
    )

    st.subheader("Automatizace")
    st.session_state.done["auto"] = st.checkbox(
        "Automatizace – Python + Playwright/pytest",
        value=st.session_state.done["auto"],
    )
    st.session_state.done["selenium"] = st.checkbox(
        "Selenium – starší framework pro UI testy",
        value=st.session_state.done.get("selenium", False),
    )
    st.session_state.done["ci_cd"] = st.checkbox(
        "CI/CD (GitHub Actions, Jenkins) – spouštění testů",
        value=st.session_state.done.get("ci_cd", False),
    )

    st.subheader("Prostředí & ladění")
    st.session_state.done["devtools"] = st.checkbox(
        "Prohlížečové DevTools – inspekce, network, performance",
        value=st.session_state.done.get("devtools", False),
    )
    st.session_state.done["docker"] = st.checkbox(
        "Docker / VirtualBox – testovací prostředí",
        value=st.session_state.done.get("docker", False),
    )
    st.session_state.done["logs"] = st.checkbox(
        "Práce s logy a monitoring (Grafana, Kibana)",
        value=st.session_state.done.get("logs", False),
    )

    st.subheader("Komunikace")
    st.session_state.done["slack"] = st.checkbox(
        "Slack / MS Teams – týmová komunikace",
        value=st.session_state.done.get("slack", False),
    )

def page_portfolio():
    st.header("3) Portfolio a práce")

    st.subheader("GitHub projekty")
    st.session_state.done["projects"] = st.checkbox(
        "Miniprojekty na GitHubu (testovací skripty, ukázky)",
        value=st.session_state.done["projects"],
    )
    st.session_state.done["bug_reports"] = st.checkbox(
        "Ukázkové bug reporty v repozitáři",
        value=st.session_state.done.get("bug_reports", False),
    )
    st.session_state.done["testcases_repo"] = st.checkbox(
        "Test cases v repozitáři (např. XLSX/Markdown)",
        value=st.session_state.done.get("testcases_repo", False),
    )

    st.subheader("Dokumentace & ukázky")
    st.session_state.done["readme"] = st.checkbox(
        "README s popisem projektů a nástrojů",
        value=st.session_state.done["readme"],
    )
    st.session_state.done["templates"] = st.checkbox(
        "Šablony (bug report, test case, checklist)",
        value=st.session_state.done.get("templates", False),
    )

    st.subheader("Prezentace")
    st.session_state.done["cv"] = st.checkbox(
        "CV (zaměřené na QA) + LinkedIn profil",
        value=st.session_state.done["cv"],
    )
    st.session_state.done["blog"] = st.checkbox(
        "Sdílené poznámky / blog o testování",
        value=st.session_state.done.get("blog", False),
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
                "Základy": ["• 2 h Git + GitHub", "• 2 h HTML/CSS/JS", "• 1 h SQL"],
                "API testování": ["• 2 h Postman základy", "• 2 h psaní requestů", "• 1 h dokumentace"],
                "Automatizace": ["• 2 h Python", "• 2 h Playwright/pytest", "• 1 h refaktor"],
                "Portfolio/README": ["• 2 h README + ukázky", "• 2 h miniprojekt", "• 1 h polishing"],
            }
            st.success((f"{jmeno}, " if jmeno else "") + f"tvůj plán na {hodin} h/týden:")
            st.write("\n".join(body[fokus]))

def page_kviz():
    st.header("🧩 Mini kvíz – pohovorové otázky")
    q1 = st.radio("1) Jaký je rozdíl mezi verifikací a validací?", [
        "Verifikace = proti potřebám uživatele, Validace = proti specifikaci",
        "Verifikace = proti specifikaci, Validace = proti potřebám uživatele",
        "Žádný rozdíl",
    ], index=None)
    q2 = st.radio("2) Co je regresní testování?", [
        "Ověření, že opravy a nové funkce nerozbily starou funkčnost",
        "Testy výkonu pod zátěží",
        "Rychlé ověření, že konkrétní funkčnost funguje",
    ], index=None)
    q3 = st.radio("3) Jaký je rozdíl mezi severity a priority?", [
        "Severity = dopad na systém, Priority = kdy opravit",
        "Severity = kdo chybu nahlásil, Priority = kolik uživatelů ji má",
        "Žádný rozdíl",
    ], index=None)
    if st.button("Vyhodnotit"):
        score = 0
        if q1 == "Verifikace = proti specifikaci, Validace = proti potřebám uživatele": score += 1
        if q2 == "Ověření, že opravy a nové funkce nerozbily starou funkčnost": score += 1
        if q3 == "Severity = dopad na systém, Priority = kdy opravit": score += 1
        st.success(f"Skóre: {score}/3")
        if score == 3: st.balloons()

def page_timeline():
    st.header("🗓️ Doporučená timeline")
    timeline = pd.DataFrame({
        "Týden": ["1–2", "3–4", "5–6", "7–8", "9–10", "11–12"],
        "Fokus": [
            "Základy testování (manuál/auto, funkční vs. nefunkční, bug reporty)",
            "Git + GitHub, základy webu (HTML/CSS/JS), SQL",
            "Nástroje: Jira, Postman, TestRail",
            "Automatizace: Python, Playwright/pytest, CI/CD",
            "Miniprojekty na GitHubu, README, bug reporty, test cases",
            "Příprava na pohovor, CV + LinkedIn, praktické úkoly",
        ],
    })
    st.table(timeline)
    st.info("⏱️ Plán je orientační – uprav si ho podle možností.")

def page_zdroje():
    st.header("📚 Užitečné zdroje")
    st.markdown("""
### Manuální testování
- [Practice QA web](https://practice-qa.com)  
- [DemoQA](https://demoqa.com)

### Teorie testování (ISTQB základy)
- [ISTQB sylabus PDF](https://www.istqb.org/certifications/certified-tester-foundation-level)

### SQL základy
- [SQLZoo](https://sqlzoo.net/)  
- [W3Schools SQL](https://www.w3schools.com/sql/)

### Git a verzování
- [GitHub Learning Lab](https://lab.github.com/)  
- [Pro Git Book](https://git-scm.com/book/en/v2)

### API testování
- [Postman Learning Center](https://learning.postman.com/)  
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)

### Automatizace testů
- [Playwright docs](https://playwright.dev/python/docs/intro)  
- [pytest docs](https://docs.pytest.org/en/stable/)  
- [Selenium docs](https://www.selenium.dev/documentation/)

### CI/CD a DevOps
- [GitHub Actions](https://docs.github.com/en/actions)  
- [Jenkins Pipeline Tutorial](https://www.jenkins.io/doc/pipeline/tour/hello-world/)

### Agile / Scrum
- [Scrum Guide](https://scrumguides.org/)  
- [Atlassian Agile Coach](https://www.atlassian.com/agile)

### Nástroje
- [Jira Software Guide](https://www.atlassian.com/software/jira/guides)  
- [TestRail intro](https://www.gurock.com/testrail/)  
- [Confluence](https://www.atlassian.com/software/confluence)

### Prohlížečové DevTools
- [Chrome DevTools Guide](https://developer.chrome.com/docs/devtools/)

### Linux / CLI
- [Linux Journey](https://linuxjourney.com/)  
- [OverTheWire Bandit](https://overthewire.org/wargames/bandit/)

### Networking
- [MDN HTTP Basics](https://developer.mozilla.org/en-US/docs/Web/HTTP)  
- [How DNS works](https://howdns.works/)

### Security základy
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)  
- [PortSwigger Academy](https://portswigger.net/web-security)

### Python & projekty
- [Streamlit docs](https://docs.streamlit.io/)  
- [Awesome Streamlit](https://awesome-streamlit.org/)
""")

def page_teorie():
    st.header("📖 Základní teorie testování")

    st.subheader("Typy testů")
    st.markdown("""
### Funkční testy
- **Smoke** – základní ověření, že aplikace vůbec běží  
- **Sanity** – rychlé ověření, že konkrétní funkčnost funguje po změně  
- **Regresní** – ověření, že opravy/nové funkce nerozbily staré funkce  
- **Exploratory testing** – neformální testování bez scénáře, hledání neočekávaných chyb  
- **Ad-Hoc testing** – nahodilé testování bez přípravy, spíše intuitivní  
- **End-to-End testing** – ověřuje celý proces, např. od registrace po nákup  

### Nefunkční testy
- **Performance testy** – rychlost odezvy  
- **Load Testing** – výkon při zátěži  
- **Stress testy** – chování systému při extrémní zátěži  
- **Usability testy** – uživatelská přívětivost  
- **Security testy** – odolnost vůči útokům (SQL injection, XSS)  
- **Compatibility testy** – funkčnost v různých prohlížečích, zařízeních, OS  
- **Recovery testy** – chování při pádu systému a obnova po výpadku  

### Úrovně testování
- **Jednotkové (unit)** – testuje jednotlivé části kódu (metody, funkce, třídy)  
- **Integrační** – testuje propojení mezi moduly (např. Frontend–API)  
- **Systémové** – testuje se celý systém jako celek, funkční i nefunkční testy (ověření, zda splňuje požadavky)  
- **Akceptační** – provádí klient nebo koncový uživatel, testuje reálné scénáře použití, cílem je potvrdit, že je aplikace připravená k nasazení  
""")

    st.subheader("Verifikace vs. Validace")
    st.markdown("""
- **Verifikace** = Ověřuji, zda produkt odpovídá specifikaci (*Stavíme správně?*).  
- **Validace** = Ověřuji, zda produkt splňuje potřeby uživatele (*Stavíme správnou věc?*).
""")

    st.subheader("Severita vs. Priorita")
    st.markdown("""
### 🔹 Severita (Severity)
Udává **závažnost chyby z technického pohledu** – jak moc chyba ovlivňuje funkčnost systému.  
Obvykle ji určuje **tester/QA**.

**Úrovně:**
- 🟥 **Critical / Blocker** – aplikace je nepoužitelná (např. nelze se přihlásit, platby nefungují)  
- 🟧 **High / Major** – zásadní chyba, ale systém se dá částečně používat  
- 🟨 **Medium** – omezuje určitou funkčnost, existuje workaround  
- 🟩 **Low / Minor** – drobnost bez dopadu na hlavní funkčnost (např. překlep)  

---

### 🔹 Priorita (Priority)
Udává **pořadí, v jakém má být chyba opravena** – jak rychle se má řešit.  
Obvykle ji určuje **Product Owner / Project Manager**.

**Úrovně:**
- 🔴 **High** – musí být opraveno okamžitě (např. kritický bug na produkci)  
- 🟠 **Medium** – opravit před vydáním, ale není blocker  
- 🟢 **Low** – může počkat, nebrání release (např. kosmetická úprava)  

---

### 🔹 Rozdíl v praxi
- **Severita = dopad na systém**  
- **Priorita = kdy to opravíme (business pohled)**  

**Příklady:**
- ✅ Překlep v názvu aplikace: Severita Low, Priorita High  
- ✅ Platba kartou nefunguje: Severita Critical, Priorita High  
- ✅ Tlačítko padá jen v Edge: Severita Medium, Priorita Low  
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

    st.markdown("### 1) Příprava")
    st.write("- **Cíl & rozsah**, **Rizika/priorita**, **Prostředí & data**, **DoD**")

    st.markdown("### 2) Návrh testů")
    st.write("""
- Techniky: ekvivalence, hranice, stavové přechody, pairwise  
- Úrovně: unit/API/UI; typy: funkční, negativní, regresní, smoke  
- Minimal viable set: nejdřív **smoke**, pak kritické cesty, pak okraje  
""")

    st.markdown("### 3) Provedení")
    st.write("""
- Scripted + Exploratory ~ 70/30 (timebox 30–60 min)  
- Evidence: PASS/FAIL, screenshot/log/HAR u failů  
- Verzování: drž v Gitu (README, `tests/`, `testcases.xlsx`)  
""")

    st.markdown("### 4) Bug report – šablona")
    bug = """Název: [Checkout] 500 při prázdném košíku
Prostředí: test, v1.2.3 (build #456), Chrome 127
Kroky: 1) Otevřít /checkout  2) Kliknout „Zaplatit“ s prázdným košíkem
Očekávané: Validace „Košík je prázdný“
Aktuální: HTTP 500, bílá stránka
Důkazy: screenshot.png, network.har
Závažnost/Priorita: High / P1
Poznámka: Regrese od v1.2.2
Status: NEW
"""
    st.code(bug, language="markdown")
    st.download_button("⬇️ Stáhnout Bug report", bug, file_name="bug-report.md")

    st.markdown("### 5) Test case – šablona")
    tc = """ID: TC-LOGIN-001
Název: Přihlášení validního uživatele
Cíl: Ověřit, že uživatel s platnými údaji se úspěšně přihlásí
Prostředí: test, v1.2.3 (build #456), Chrome 127
Požadavky/Trace: REQ-LOGIN-001
Předpoklady / Data: user@test.com / *****

Kroky:
  1) Otevřít /login
  2) Vyplnit platné údaje
  3) Odeslat formulář

Očekávaný výsledek:
  - Uživatel je přesměrován na /dashboard
  - Zobrazí se uživatelské jméno v headeru

Aktuální výsledek:
  - [doplnit po provedení testu]

Status: NOT RUN / PASS / FAIL / BLOCKED
Priorita: P1
Tagy: @smoke @regression
Evidence: screenshot.png, log.txt, network.har
Poznámky:
"""
    st.code(tc, language="markdown")
    st.download_button("⬇️ Stáhnout Test Case", tc, file_name="test-case.md")

    st.markdown("### 6) PR checklist")
    pr = """PR checklist:
- [ ] Projde lokální smoke
- [ ] Test data/seed aktualizovány
- [ ] Přidané/změněné testy
- [ ] Bezpečnostní dopad zhodnocen
- [ ] Aktualizován README/CHANGELOG
"""
    st.code(pr, language="markdown")
    st.download_button("⬇️ Stáhnout PR checklist", pr, file_name="pr-checklist.md")

    with st.expander("Legenda statusů pro test case"):
        st.markdown("""
- **NOT RUN** – test zatím neproběhl  
- **PASS** – očekávané = aktuální  
- **FAIL** – odchylka od očekávaného výsledku  
- **BLOCKED** – test nelze provést (závislost, prostředí, blocker bug)
""")

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

    headers_text = st.text_area("HTTP headers (Klíč: Hodnota na řádek)", "Content-Type: application/json", height=80)
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
                    try: st.json(r.json())
                    except Exception: st.text(r.text[:2000])
                else:
                    st.text(r.text[:2000])

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


