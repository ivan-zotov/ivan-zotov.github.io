import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


URL = "https://one-vv0203.com/v3/7001/promo-ipl-india?p=jsz5"
FILE_NAME = "matches.json"


def create_driver():
    options = Options()

    # 🔥 КЛЮЧЕВОЙ ФИКС: НЕ используем новый headless
    options.add_argument("--headless=old")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # 🔥 маскируем как обычный браузер
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def parse_matches():
    driver = create_driver()
    driver.get(URL)

    time.sleep(10)

    # 🔥 ПРОКРУТКА (обязательно)
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # 🔥 ищем ВСЕ блоки с текстом
    elements = driver.find_elements(By.XPATH, "//div")

    matches = []

    for el in elements:
        text = el.text.strip()

        if "vs" in text.lower():
            lines = text.split("\n")

            if len(lines) >= 2:
                try:
                    teams_line = lines[0]

                    if "vs" in teams_line.lower():
                        parts = teams_line.split("vs")

                        team1 = parts[0].strip()
                        team2 = parts[1].strip()

                        matches.append({
                            "team1": team1,
                            "team2": team2,
                            "raw": lines
                        })

                except:
                    continue

    driver.quit()

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