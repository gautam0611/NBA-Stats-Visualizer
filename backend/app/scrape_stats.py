from enum import Enum
import requests
from bs4 import BeautifulSoup

class StatsType(Enum):
    TEAM = "teams"
    DIVISION = "division"
    PLAYER = "player"
    ROSTER = "stats"
    GAMES = "games"
    RECORD = "record"
    SEASON = "season"

def scrape_nba_statistics(stats_type: StatsType):
    url = f"https://sports.yahoo.com/nba/{stats_type.value}/"
    print(url)
    r = requests.get(url)

    returnSet = []

    soup = BeautifulSoup(r.content, 'lxml')
    
    for div in soup.find_all('div', attrs={'class': 'Pb(40px)'}):
        divisionName = div.div.h5.get_text().strip()
        if divisionName in returnSet:
            continue
        else:
            returnSet.append(divisionName)
        
    return returnSet

def send_data_to_api(statsType, returnSet):
    api_url = f'http://127.0.0.1:8000/{statsType.value}/{1}'
    for value in returnSet:
        value_to_return = {
            "name": value,
            "conference_id": 1
        }
        response = requests.post(api_url, json=value_to_return)
        if response.status_code == 200:
            print(f"Successfully added {statsType}")
        else:
            print(f"Failed to add {statsType}: {response.text}")


# playerData = scrape_nba_statistics(stats_type=StatsType.PLAYER)
divisionData = scrape_nba_statistics(stats_type=StatsType.TEAM)
# print(divisionData)
print(send_data_to_api(statsType=StatsType.DIVISION, returnSet=divisionData))
# print(scrape_nba_statistics(stats_type=StatsType.TEAM))
