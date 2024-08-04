from decimal import Decimal
from enum import Enum
from typing import Dict, List
import requests
from bs4 import BeautifulSoup

from .stats_type import StatsType

# https://sports.yahoo.com/nba/teams/boston/stats/ -> team stats
# https://sports.yahoo.com/nba/teams/ -> divisions
# https://sports.yahoo.com/nba/standings/ -> standings
# https://sports.yahoo.com/nba/teams/boston/stats/?season=2023 -> stats for the celtics in 2023-2024
# https://sports.yahoo.com/nba/standings/?season=2021&selectedTab=1 -> eastern conference records for the 2022 season
# https://sports.yahoo.com/nba/teams/miami/schedule/?season=2023&month=3 -> games miami heat played in april


class ScrapeNBAStats:
    def __init__(self, team_name, season) -> None:
        self.team_name = team_name
        self.season = season

    def scrape_nba_statistics(self):
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


class ScrapePlayers(ScrapeNBAStats):
    def __init__(self, team_name, season) -> None:
        super().__init__(team_name, season)

    # web scrapes all of the players and their stats on each team
    def scrape_nba_statistics(self) -> dict[str, dict[str, Decimal]]:
        # get a list of all the players on specified team in a season
        for player in self.team_name:
            player_dict: dict[str, dict[str, Decimal]]
            url = f"https://sports.yahoo.com/nba/teams/{self.team_name}/{StatsType.ROSTER.value}?season={self.season}"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml")

            for tr in soup.find_all(
                "tr",
                class_=["Bgc(table-hover):h", "Bgc(table-hover):h Bgc(fuji-secondary)"],
            ):
                stats_dict: dict[str, Decimal] = {}
                points = Decimal(tr.td[13].get_text().strip())
                assists = Decimal(tr.td[17].get_text().strip())
                rebounds = Decimal(tr.td[16].get_text().strip())

                # add our stats to a dictionary for this player
                stats_dict["points"] = points
                stats_dict["assists"] = assists
                stats_dict["rebounds"] = rebounds
            # add the player and their stats to our dictionary
            player_dict[player] = stats_dict
        return player_dict


class ScrapeRecord(ScrapeNBAStats):
    def __init__(self, team_name, season, conference) -> None:
        super().__init__(team_name, season)
        self.conference = conference

    # web scrapes the record of the specifed team in a specifed season
    def scrape_nba_statistics(self):
        record_dict: dict[str, str] = {}
        # the url has a "1" or "2" in it depending on the conference
        if self.conference.lower() == "eastern":
            selected_tab = 1
        elif self.conference.lower() == "western":
            selected_tab = 2
        else:
            raise NameError("not a valid conference name")

        url = f"https://sports.yahoo.com/nba/standings/?season={self.season}&selectedTab={selected_tab}"  # eastern conference is "1" and western conference is "2"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        # getting all of the divisions
        division_divs = soup.find_all("div", attrs={"data-tst": "group-table"})

        for division_div in division_divs:
            team_rows = division_div.tbody.find_all("tr")
            for team in team_rows:
                team_name = team.th.div.div.a.span[2].get_text().lower()
                win = team.td[1]
                loss = team.td[2]
                format_record = f"{win}-{loss}"
                record_dict[team_name] = format_record

        return record_dict


class ScrapeGames(ScrapeNBAStats):
    def __init__(self, team_name, season) -> None:
        super().__init__(team_name, season)

    # web scrapes the games of the specified team in a specified season
    def scrape_nba_statistics(self) -> dict[str, dict[str, str]]:
        games_dict = {}
        url = f"https://sports.yahoo.com/nba/teams/{self.team_name}/schedule/?season={self.season}&month=3&scheduleType=list"  # eastern conference is "1" and western conference is "2"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        for tr in soup.find_all(
            "tr", attrs={"class": "Bgc(bg-mod) Pos(r) H(45px) Bgc(secondary):h Cur(p)"}
        ):
            stats_dict = {}
            # scrape all of data
            game_date = tr.td[1].a.span.span.get_text().strip()
            opponent = tr.td[3].span.span.get_text().strip()
            result = tr.td[4].span.get_text().strip()
            score_winner = tr.td[5].span[1].get_text().strip()
            score_dash = tr.td[5].span[2].get_text().strip()
            score_loser = tr.td[5].span[3].get_text().strip()
            score = score_winner + score_dash + score_loser

            # add our data to a dictionary
            stats_dict["game_date"] = game_date
            stats_dict["opponent"] = opponent
            stats_dict["result"] = result
            stats_dict["score"] = score

            # add to our dict of dicts
            games_dict[f'{self.team_name} vs {stats_dict["opponent"]}'] = stats_dict
        return games_dict
