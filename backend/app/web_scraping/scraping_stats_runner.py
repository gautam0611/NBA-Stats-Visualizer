import requests

from .scrape_stats import (
    ScrapeConference,
    ScrapeDivisions,
    ScrapeTeams,
    ScrapeSeasons,
    ScrapePlayers,
    ScrapeRecord,
    ScrapeGames,
    ScrapeNBAStats,
    StatsType,
)


class ScrapeStatsRunner(ScrapeNBAStats):
    # NOTE: we use this constructor for data that doesn't require a team name or season
    def __init__(self, arg_stats_type: str):
        self.arg_stats_type = arg_stats_type

    def __init__(self, arg_stats_type: str, team_name: str, season: str) -> None:
        super().__init__(team_name=team_name, season=season)
        self.arg_stats_type = arg_stats_type

    def team_dict(self) -> dict[str, str]:
        team_lower = self.team_name.lower().strip()

        # ensure that user did not enter "Miami Heat"
        if len(team_lower.split("")) > 1:
            raise NameError("Not a valid team entry. Must be in the format 'celtics' ")

        team_dict = {
            "celtics": "boston",
            "heat": "miami",
            "nets": "brooklyn",
            "knicks": "new-york",
            "76ers": "philadelphia",
            "raptors": "toronto",
            "bulls": "chicago",
            "cavaliers": "cleveland",  # could also be "cavs"
            "pistons": "detroit",
            "pistons": "indiana",
            "bucks": "milwaukee",
            "hawks": "atlanta",
            "hornets": "charlotte",
            "magic": "orlando",
            "wizards": "washington",
            "warriors": "golden-state",
            "clippers": "la-clippers",
            "lakers": "la-lakers",
            "suns": "phoenix",
            "kings": "sacramento",
            "mavericks": "dallas",  # could also be "mavs"
            "rockets": "houston",
            "grizzlies": "memphis",
            "pelicans": "new-orleans",
            "spurs": "san-antonio",
            "nuggets": "denver",
            "wolves": "minnesota",  # could also be "timberwolves"
            "thunder": "oklahoma-city",
            "blazers": "portland",
            "jazz": "utah",
        }
        return team_dict

    def season_dict(self) -> dict[str, str]:
        season_dict = {
            "2023-2024": "2024",
            "2022-2023": "2023",
            "2021-2022": "2022",
            "2020-2021": "2021",
            "2019-2020": "2020",
            "2018-2019": "2019",
            "2017-2018": "2018",
            "2016-2017": "2017",
            "2015-2016": "2016",
            "2014-2015": "2015",
            "2013-2014": "2014",
        }
        return season_dict

    def get_stats_type(self):
        statistics = {
            "Conference": ScrapeConference().scrape_nba_statistics(),
            "Division": ScrapeDivisions().scrape_nba_statistics(),
            "Team": ScrapeTeams().scrape_nba_statistics(),
            "Season": ScrapeSeasons().scrape_nba_statistics(),
            "Players": ScrapePlayers(
                self.team_dict[self.team_name], self.season_dict[self.season]
            ).scrape_nba_statistics(),
            "Record": ScrapeRecord(
                "eastern",
                self.team_dict[self.team_name],
                self.season_dict[
                    self.season
                ],  # @FIXME "eastern" is not ideal but can't think of anything else atm
            ).scrape_nba_statistics(),
            "Games": ScrapeGames(
                self.team_dict[self.team_name], self.season_dict[self.season]
            ).scrape_nba_statistics(),
        }

        # return the correct stats
        if self.arg_stats_type in statistics:
            return statistics[self.arg_stats_type]
        else:
            raise TypeError(
                "not a valid stats-type. Must be like 'Conference', 'Division', etc."
            )

    def json_body_to_return(self):
        """
        1. scrape the data via "scrapeNBAStatistics()
        2. store in a list and iterate through each value
        3. call "requests.get()" and pass in the url and data to get return body
        """
        base_url = "http://127.0.0.1:8000/"
        list_of_stats_types = self.get_stats_type()
        list_of_responses = []
        for item in list_of_stats_types:

            stats_type_json_body = {
                "Conference": {
                    "url": f"{base_url}/{StatsType.CONFERENCE.value}",  # @FIXME add the value we want to get back
                    "data": item,
                },
                "Division": {},
                "Team": {},
                "Season": {},
                "Players": {},
                "Record": {},
                "Games": {},
            }

            list_of_responses.append(
                requests.get(
                    url=stats_type_json_body[self.arg_stats_type]["url"],
                    data=stats_type_json_body[self.arg_stats_type]["item"],
                )
            )
        return list_of_responses


"""
1. for each corresponding datatype, we need to GET the foreign key's response body 
- remove the id of that response body
- store that response body and return it for use of POST
- also return the URL needed 
"""


def send_data_to_api(statsType, returnSet):
    """
    1. requests.get to get the necessary ids needed for the response object
    2. abstract response object schema to a helper function
    """
    api_url = f"http://127.0.0.1:8000/{statsType.value}/{1}"  # need to pass in url which contains stats type and
    for value in returnSet:
        value_to_return = {
            "name": value,
            "conference_id": 1,
        }  # need to pass in json body
        response = requests.post(api_url, json=value_to_return)
        if response.status_code == 200:
            print(f"Successfully added {statsType}")
        else:
            print(f"Failed to add {statsType}: {response.text}")


# playerData = scrape_nba_statistics(stats_type=StatsType.PLAYER)
# get_division_data = ScrapeNBAStats().scrape_divisions(stats_type=StatsType.TEAM)
# divisionData = ScrapeNBAStats().scrape_nba_statistics(
#     stats_type=StatsType.TEAM, scrape_nba_stats=get_division_data
# )


# print(divisionData)
print(send_data_to_api(statsType=StatsType.DIVISION, returnSet=divisionData))
# print(scrape_nba_statistics(stats_type=StatsType.TEAM))
