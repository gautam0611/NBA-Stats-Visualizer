from enum import Enum
import requests
from bs4 import BeautifulSoup

class StatsType(Enum):
    TEAM = "team"
    PLAYER = "player"
    ROSTER = "stats"
    GAMES = "games"
    RECORD = "record"
    SEASON = "season"

def scrape_nba_statistics(stats_type: StatsType):
    url = f"https://sports.yahoo.com/nba/teams/boston/{stats_type.value}/"
    print(url)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'lxml')

    table = soup.find('div', attrs={'class': 'Ovx(s)'})
    print(table)


# playerData = scrape_nba_statistics(stats_type=StatsType.PLAYER)
print(scrape_nba_statistics(stats_type=StatsType.ROSTER))
