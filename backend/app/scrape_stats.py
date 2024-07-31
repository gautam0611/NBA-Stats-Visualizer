from enum import Enum
from typing import List
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


# https://sports.yahoo.com/nba/teams/boston/stats/ -> team stats
# https://sports.yahoo.com/nba/teams/ -> divisions
# https://sports.yahoo.com/nba/teams/boston/stats/?season=2023 -> stats for the celtics in 2023-2024
# https://sports.yahoo.com/nba/standings/?season=2021 -> record for the 2022 season
# https://sports.yahoo.com/nba/teams/miami/schedule/?season=2023&month=3 -> games miami heat played in april


class ScrapeNBAStats:
    def scrape_nba_statistics(self):
        raise NotImplementedError("subclasses will handle implementation")


class ScrapeDivisions(ScrapeNBAStats):
    # web scrapes all of the divisions in the NBA
    def scrape_nba_statistics(self):
        url = f"https://sports.yahoo.com/nba/{StatsType.TEAM.value}/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        list_of_divisions: List[str] = []
        for div in soup.find_all("div", attrs={"class": "Pb(40px)"}):
            divisionName = div.div.h5.get_text().strip()
            if divisionName in list_of_divisions:
                continue
            else:
                list_of_divisions.append(divisionName)
        return list_of_divisions


class ScrapeTeams(ScrapeNBAStats):
    # web scrapes all of the teams in the specified division
    def scrape_nba_statistics(self):
        url = f"https://sports.yahoo.com/nba/{StatsType.TEAM.value}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        list_of_teams: List[dict[str, str]] = []

        list_of_divisions = ScrapeDivisions()
        for division in list_of_divisions:
            division_dict = {}
            for div in soup.find_all(
                "div", attrs={"class": "Py(5px) Ta(start) Fw(400) Py(6px)"}
            ):
                team_name = div.div.div.div.div.a.get_text().strip()
                print(team_name)
                division_dict[division] = team_name
            list_of_teams.append(division_dict)


class ScrapeSeasons(ScrapeNBAStats):
    # web scrapes all of the seasons in the past 5 years
    def scrape_seasons(self) -> List[str]:
        pass


class ScrapePlayers(ScrapeNBAStats):
    # web scrapes all of the players and their stats on the specified team
    def scrape_players(self) -> List[str]:
        pass


class ScrapeRecord(ScrapeNBAStats):
    # web scrapes the record of the specifed team in a specifed season
    def scrape_nba_statistics(self):
        return super().scrape_nba_statistics()


class ScrapeGames(ScrapeNBAStats):
    # web scrapes the games of the specified team in a specified season
    def scrape_games(self) -> List[str]:
        pass


statistics = {}


def send_data_to_api(statsType, returnSet):
    # @FIXME change this to an argument
    api_url = f"http://127.0.0.1:8000/{statsType.value}/{1}"
    for value in returnSet:
        value_to_return = {"name": value, "conference_id": 1}
        response = requests.post(api_url, json=value_to_return)
        if response.status_code == 200:
            print(f"Successfully added {statsType}")
        else:
            print(f"Failed to add {statsType}: {response.text}")


# playerData = scrape_nba_statistics(stats_type=StatsType.PLAYER)
# get_division_data = ScrapeNBAStats().scrape_divisions(stats_type=StatsType.TEAM)
divisionData = ScrapeNBAStats().scrape_nba_statistics(
    stats_type=StatsType.TEAM, scrape_nba_stats=get_division_data
)


# print(divisionData)
print(send_data_to_api(statsType=StatsType.DIVISION, returnSet=divisionData))
# print(scrape_nba_statistics(stats_type=StatsType.TEAM))
