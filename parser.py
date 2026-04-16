import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_driver():
    options = Options()

    # 🔥 ОБЯЗАТЕЛЬНО ДЛЯ GITHUB ACTIONS
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver


# --- URL ---
URL = "https://one-vv0203.com/v3/7001/promo-ipl-india?p=jsz5"
FILE_NAME = "matches.json"


def parse_matches():
    driver = create_driver()
    driver.get(URL)

    time.sleep(10)  # ждём загрузку JS

    matches_data = []

    matches = driver.find_elements(By.CSS_SELECTOR, ".calendar-card.calendar-table__item")  # потом уточним селектор

    for match in matches:
        try:
            text = match.text

            # 🔥 ВАЖНО: здесь нужно подогнать под реальную верстку
            if "vs" in text.lower():
                lines = text.split("\n")

                teams = match.find_elements(By.CSS_SELECTOR, ".calendar-card__team-name")
                team1 = teams[0].text
                team2 = teams[1].text

                date = match.find_element(By.CSS_SELECTOR, ".calendar-card__date").text

                odds_elements = match.find_elements(By.CSS_SELECTOR, ".calendar-card__odd-value")
                odds = [o.text for o in odds_elements]

                matches_data.append({
                    "team1": team1,
                    "team2": team2,
                    "date": date,
                    "odds": odds
                })

        except:
            continue

    driver.quit()

    return matches_data


def load_old_data():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def update_data():
    print("Обновление данных...")

    new_data = parse_matches()
    old_data = load_old_data()

    updated = []

    for new_match in new_data:
        found = False

        for old_match in old_data:
            if (new_match["team1"] == old_match["team1"] and
                new_match["team2"] == old_match["team2"]):

                # обновляем коэффициенты
                old_match["odds"] = new_match["odds"]
                updated.append(old_match)
                found = True
                break

        if not found:
            # новый матч
            updated.append(new_match)

    # удаляем завершенные (если нет в новом списке)
    save_data(updated)

    print("Готово!")


if __name__ == "__main__":
    update_data()