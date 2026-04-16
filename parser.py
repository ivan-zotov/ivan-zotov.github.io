import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

import schedule
import os

os.system("git add .")
os.system("git commit -m 'update matches'")
os.system("git push")


def parse_matches():
    driver = webdriver.Chrome()
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


# запуск каждые 4 часа
schedule.every(4).hours.do(update_data)

# первый запуск сразу
update_data()

while True:
    schedule.run_pending()
    time.sleep(60)
