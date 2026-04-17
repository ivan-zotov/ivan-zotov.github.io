import json
from playwright.sync_api import sync_playwright

URL = "https://one-vv0203.com/v3/7001/promo-ipl-india?p=jsz5"
FILE_NAME = "matches.json"


def parse_matches():
    matches = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        context = browser.new_context()
        page = context.new_page()

        responses = []

        # 🔥 ПЕРЕХВАТ ВСЕХ API ЗАПРОСОВ
        def handle_response(response):
            if "api" in response.url or "event" in response.url:
                try:
                    data = response.json()
                    responses.append(data)
                except:
                    pass

        page.on("response", handle_response)

        page.goto(URL, timeout=60000)

        page.wait_for_load_state("networkidle")

        # немного ждём
        page.wait_for_timeout(5000)

        browser.close()

    # 🔥 ПАРСИМ ПОЛУЧЕННЫЕ ДАННЫЕ
    for resp in responses:
        if isinstance(resp, dict):
            for key, value in resp.items():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            team1 = item.get("team1") or item.get("home")
                            team2 = item.get("team2") or item.get("away")

                            if team1 and team2:
                                matches.append({
                                    "team1": team1,
                                    "team2": team2,
                                    "raw": item
                                })

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