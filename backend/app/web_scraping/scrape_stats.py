from enum import Enum
from typing import Dict, List
import requests
from bs4 import BeautifulSoup

from backend.app.web_scraping.stats_type import StatsType

# https://sports.yahoo.com/nba/teams/boston/stats/ -> team stats
# https://sports.yahoo.com/nba/teams/ -> divisions
# https://sports.yahoo.com/nba/standings/ -> standings
# https://sports.yahoo.com/nba/teams/boston/stats/?season=2023 -> stats for the celtics in 2023-2024
# https://sports.yahoo.com/nba/standings/?season=2021 -> record for the 2022 season
# https://sports.yahoo.com/nba/teams/miami/schedule/?season=2023&month=3 -> games miami heat played in april


class ScrapeNBAStats:
    def scrape_nba_statistics(self):
        raise NotImplementedError("subclasses will handle implementation")

    def json_body_to_return(self):
        raise NotImplementedError("subclasses will handle implementation")


class ScrapeConference(ScrapeNBAStats):
    # web scrapes all of the conferences in the NBA
    def scrape_nba_statistics(self):
        url = f"https://sports.yahoo.com/nba/{StatsType.TEAM.value}/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        list_of_conferences: List[str] = []
        for h3 in soup.findall("h3", attrs={"class": "Fz(16px) Pb(15px)"}):
            conference_name = h3.get_text().strip()
            list_of_conferences.append(conference_name)

        return list_of_conferences


class ScrapeDivisions(ScrapeNBAStats):
    # web scrapes all of the divisions in the NBA
    def scrape_nba_statistics(self) -> List[str]:
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

    # def json_body_to_return(self):
    #     return super().json_body_to_return()


class ScrapeTeams(ScrapeNBAStats):
    # web scrapes all of the teams in each division
    def scrape_nba_statistics(self) -> Dict[str, List[str]]:
        url = f"https://sports.yahoo.com/nba/{StatsType.TEAM.value}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        division_dict = {}

        list_of_divisions = ScrapeDivisions().scrape_nba_statistics()
        for division in list_of_divisions:
            list_of_teams: List[dict[str, str]] = []
            for div in soup.find_all(
                "div", attrs={"class": "Py(5px) Ta(start) Fw(400) Py(6px)"}
            ):
                team_name = div.div.div.div.div.a.get_text().strip()
                print(team_name)
                list_of_teams.append(team_name)
            division_dict[division] = list_of_teams

        return division_dict

    # def json_body_to_return(self):
    #     return super().json_body_to_return()


class ScrapeSeasons(ScrapeNBAStats):
    # web scrapes all of the seasons in the past 10 years
    def scrape_nba_statistics(self) -> List[str]:
        url = f"https://sports.yahoo.com/nba/{StatsType.SEASON.value}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        list_of_seasons: List[str] = []

        for select in soup.find("select", attrs={"data-tst": "season-dropdown"}):
            record = select.option.get_text().strip()
            list_of_seasons.append(record)

        return list_of_seasons

    # def json_body_to_return(self):
    #     return super().json_body_to_return()


class ScrapePlayers(ScrapeNBAStats):
    # web scrapes all of the players and their stats on each team
    def scrape_nba_statistics(self):
        list_of_nba_teams = ScrapeTeams().scrape_nba_statistics()
        for team in list_of_nba_teams:
            url = f"https://sports.yahoo.com/nba/teams/{team}/{StatsType.ROSTER.value}"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml")

    # def json_body_to_return(self):
    #     return super().json_body_to_return()


class ScrapeRecord(ScrapeNBAStats):
    # web scrapes the record of the specifed team in a specifed season
    def scrape_nba_statistics(self):
        pass

    # def json_body_to_return(self):
    #     return super().json_body_to_return()


class ScrapeGames(ScrapeNBAStats):
    # web scrapes the games of the specified team in a specified season
    def scrape_nba_statistics(self):
        pass

    # def json_body_to_return(self):
    #     return super().json_body_to_return()


statistics = {
    "Conference": ScrapeConference(),
    "Division": ScrapeDivisions(),
    "Team": ScrapeTeams(),
    "Season": ScrapeSeasons(),
    "Players": ScrapePlayers(),
    "Record": ScrapeRecord(),
    "Games": ScrapeGames(),
}


def send_data_to_api(statsType, returnSet):
    """
    1. requests.get to get the necessary ids needed for the response object
    2. abstract response object schema to a helper function
    """
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
