import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


URL = "https://one-vv0203.com/v3/7001/promo-ipl-india?p=jsz5"
FILE_NAME = "matches.json"


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def parse_matches():
    driver = create_driver()
    driver.get(URL)

    # 🔥 ждём загрузку React приложения
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(5)

    # 🔥 прокрутка (часто нужно)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # 🔥 берём ВСЕ текстовые блоки
    elements = driver.find_elements(By.XPATH, "//*[text()]")

    matches = []

    for el in elements:
        text = el.text.strip()

        # фильтр матчей
        if " vs " in text.lower():
            parts = text.split("\n")

            if len(parts) >= 2:
                try:
                    team_line = parts[0]

                    if "vs" in team_line.lower():
                        teams = team_line.split("vs")

                        team1 = teams[0].strip()
                        team2 = teams[1].strip()

                        matches.append({
                            "team1": team1,
                            "team2": team2,
                            "raw": parts
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