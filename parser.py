import json
from playwright.sync_api import sync_playwright

URL = "https://one-vv0203.com/v3/7001/promo-ipl-india?p=jsz5"
FILE_NAME = "matches.json"


def parse_matches():
    matches = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        page = context.new_page()

        # 🔥 ОЧЕНЬ ВАЖНО
        page.goto(URL, timeout=60000)

        # 🔥 ждём загрузку JS
        page.wait_for_load_state("networkidle")

        # 🔥 скролл (данные подгружаются)
        for _ in range(5):
            page.mouse.wheel(0, 5000)
            page.wait_for_timeout(2000)

        # 🔥 берём весь текст страницы
        content = page.inner_text("body")

        lines = content.split("\n")

        for i in range(len(lines)):
            line = lines[i].strip()

            if " vs " in line.lower():
                try:
                    teams = line.split("vs")

                    team1 = teams[0].strip()
                    team2 = teams[1].strip()

                    matches.append({
                        "team1": team1,
                        "team2": team2
                    })

                except:
                    continue

        browser.close()

    print("Найдено матчей:", len(matches))

    return matches


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def update_data():
    print("Обновление данных...")

    data = parse_matches()
    save_data(data)

    print("Готово!")


if __name__ == "__main__":
    update_data()