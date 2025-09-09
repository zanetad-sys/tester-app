
## Co se testuje
{co_testuju}

## Odkazy
- Repo/App: {odkaz}
"""
            st.session_state["generated_readme"] = md

    if st.session_state.get("generated_readme"):
        st.code(st.session_state["generated_readme"], language="markdown")
        st.download_button("⬇️ Stáhnout README.md",
                           st.session_state["generated_readme"],
                           file_name="README.md")
        if st.button("Vymazat výsledek"):
            st.session_state["generated_readme"] = None
            st.rerun()

    st.divider()

    # Šablony
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

    # Export checklistu
    chosen = [k for k, v in st.session_state.done.items() if k in ("projects", "readme", "cv") and v]
    text = "Portfolio – splněno:\n" + "\n".join(f"- {x}" for x in chosen) if chosen else "Zatím nic nezaškrtnuto."
    st.download_button("⬇️ Stáhnout checklist portfolia", text, "portfolio-checklist.txt")


def page_kviz():
    st.header("🧩 Mini kvíz")
    odp = st.radio(
        "Co je Pull Request (PR) na GitHubu?",
        ["Přímé nahrání kódu do main",
         "Návrh změn z větve, který ostatní zkontrolují a sloučí",
         "Záloha repozitáře"]
    )
    if st.button("Vyhodnotit"):
        if odp == "Návrh změn z větve, který ostatní zkontrolují a sloučí":
            st.success("Správně! 👍")
        else:
            st.error("Ještě jednou: PR je návrh změn z větve, který se po schválení mergne do main.")


def page_timeline():
    st.header("🗓️ Doporučená timeline")
    timeline = pd.DataFrame({"Týden": ["1", "2", "3", "4"],
                             "Fokus": ["Základy + Git", "API testování", "Automatizace", "Portfolio/README"]})
    st.table(timeline)


def page_zdroje():
    st.header("📚 Užitečné zdroje – kurátorský seznam")

    st.markdown("#### Git & GitHub")
    st.markdown("""
- [Pro Git (kniha zdarma)](https://git-scm.com/book/en/v2)  
- [Atlassian Git Tutorials](https://www.atlassian.com/git)  
- [GitHub Docs – Pull Requests](https://docs.github.com/pull-requests)  
- [Oh My Git!](https://ohmygit.org/)  
- [Learn Git Branching](https://learngitbranching.js.org/)
""")

    st.markdown("#### Markdown / README")
    st.markdown("""
- [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/)  
- [readme.so – editor](https://readme.so/)
""")

    st.markdown("#### Web základy")
    st.markdown("""
- [MDN – HTML](https://developer.mozilla.org/docs/Web/HTML)  
- [MDN – CSS](https://developer.mozilla.org/docs/Web/CSS)  
- [MDN – JavaScript](https://developer.mozilla.org/docs/Web/JavaScript)  
- [Flexbox Froggy](https://flexboxfroggy.com/)  
- [Grid Garden](https://cssgridgarden.com/)
""")

    st.markdown("#### SQL & databáze")
    st.markdown("""
- [SQLBolt](https://sqlbolt.com/)  
- [Mode SQL Tutorial](https://mode.com/sql-tutorial/)  
- [Database Normalization](https://www.guru99.com/database-normalization.html)
""")

    st.markdown("#### API / HTTP / Postman")
    st.markdown("""
- [HTTP status codes](https://httpstatuses.com/)  
- [Postman Learning Center](https://learning.postman.com/)  
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/)  
- [Swagger Petstore](https://petstore.swagger.io/)  
- [SOAP UI Docs](https://www.soapui.org/)
""")

    st.markdown("#### Python, testy a automatizace")
    st.markdown("""
- [Python Tutorial](https://docs.python.org/3/tutorial/)  
- [pytest Docs](https://docs.pytest.org/)  
- [Playwright for Python](https://playwright.dev/python/)  
- [Selenium Docs](https://www.selenium.dev/documentation/)
""")

    st.markdown("#### DevTools, logy, Linux")
    st.markdown("""
- [Chrome DevTools – Overview](https://developer.chrome.com/docs/devtools)  
- [journalctl / systemd-journald](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html)  
- [Explainshell](https://explainshell.com/)
""")

    st.markdown("#### CI/CD")
    st.markdown("""
- [GitHub Actions – docs](https://docs.github.com/actions)  
- [GitLab CI/CD – docs](https://docs.gitlab.com/ee/ci/)
""")

    st.markdown("#### Docker & prostředí")
    st.markdown("""
- [Docker – Get Started](https://docs.docker.com/get-started/)  
- [Play with Docker](https://labs.play-with-docker.com/)
""")

    st.markdown("#### Bezpečnost & výkon")
    st.markdown("""
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)  
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)  
- [k6 – performance testing](https://k6.io/docs/)  
- [Apache JMeter – User Manual](https://jmeter.apache.org/usermanual/)
""")

    # Stáhnout jako MD
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
"""
    st.download_button("⬇️ Stáhnout seznam zdrojů (Markdown)", resources_md, file_name="uzitecne-zdroje.md")


def page_teorie():
    st.header("📖 Základní teorie testování")

    st.subheader("Typy testů")
    st.markdown("""
- Funkční vs. Nefunkční  
- Smoke, Sanity, Regresní  
- Jednotkové (unit), Integrační, Systémové, Akceptační
""")

    st.subheader("Verifikace vs. Validace")
    st.markdown("""
- **Verifikace** = děláme věci správně  
- **Validace** = děláme správné věci (uživatelská hodnota)
""")

    st.subheader("Severity vs. Priorita")
    st.markdown("""
- **Severity** = dopad chyby  
- **Priorita** = pořadí/rychlost opravy
""")

    st.subheader("Bug vs. Defect vs. Failure")
    st.markdown("""
- **Bug** = chyba nalezená při testování  
- **Defect** = nesoulad se specifikací  
- **Failure** = projev chyby v běžícím systému
""")

    st.subheader("API základy")
    st.markdown("""
- **HTTP metody**: GET, POST, PUT, PATCH, DELETE  
- **Status kódy**: 200, 201, 204, 400, 401, 403, 404, 500  
- **REST + JSON**, **SOAP + XML**
""")

    st.subheader("Metody testování (Black/White/Gray box)")
    st.markdown("""
- **Blackbox** – neznám implementaci, zkoumám vstupy/výstupy  
- **Whitebox** – znám kód/strukturu  
- **Graybox** – něco mezi
""")

    st.subheader("SQL – základy")
    st.markdown("""
- **DDL**: CREATE, ALTER, DROP  
- **DML**: INSERT, UPDATE, DELETE  
- **DQL**: SELECT  
- **DCL**: GRANT, REVOKE  
- **JOIN**: INNER, LEFT, RIGHT  
- **PK/FK**: primární a cizí klíč
""")

    st.subheader("Logy – typy")
    st.markdown("""
- Application log, System log, Security log
""")

    st.subheader("BDD – Given/When/Then")
    st.markdown("""
*Given uživatel je přihlášen* → *When klikne na „Odhlásit“* → *Then je odhlášen a přesměrován na login*.
""")


def page_qatahaky():
    st.header("🧭 QA tahák (proces + šablony)")
    st.markdown("Rychlé taháky pro praxi testera. Stáhni si šablony a používej ve svých projektech.")

    st.markdown("### 0) Příprava")
    st.write("- Cíl & rozsah, Rizika/priorita, Prostředí & data, DoD")

    st.markdown("### 1) Návrh testů")
    st.write("- Ekvivalence, hranice, stavové přechody, pairwise; Smoke → kritické cesty → okraje")

    st.markdown("### 2) Provedení")
    st.write("- Scripted + Exploratory 70/30; Evidence PASS/FAIL + screenshot/log/HAR; verzovat v Gitu")

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
**Todos API** – GET /todos, GET /todos/1, POST /todos  
**Users API** – GET /users, GET /users/1  
Base URL: `https://jsonplaceholder.typicode.com`
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
