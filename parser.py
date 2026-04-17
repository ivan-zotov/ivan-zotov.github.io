import requests
import json
from datetime import datetime

URL = "https://match-storage-partners.top-parser.com/lp-feed?&lang=en&service=PREMATCH&sportId=25&startCoefficient=1.01&tournamentId=41745&endDate=1779213117"
FILE_NAME = "matches.json"


def parse_matches():
    response = requests.get(URL)
    data = response.json()

    matches_data = []

    for sport in data.get("feed", []):
        for match in sport.get("matches", []):

            # команды
            team1 = match.get("homeTeamName")
            team2 = match.get("awayTeamName")

            # дата (timestamp → нормальный формат)
            timestamp = match.get("dateOfMatch")
            date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

            # коэффициенты
            odds = []

            for group in match.get("oddGroups", []):
                if group.get("name") == "Победитель":
                    for o in group.get("odds", []):
                        odds.append({
                            "team": o.get("name"),
                            "coef": o.get("coefficient")
                        })

            matches_data.append({
                "team1": team1,
                "team2": team2,
                "date": date,
                "odds": odds
            })

    print("Найдено матчей:", len(matches_data))

    return matches_data


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