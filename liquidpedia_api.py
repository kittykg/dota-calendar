import requests

from common import Team

BASE_API_URL = (
    "https://liquipedia.net/dota2/api.php?action=parse&origin=*&format=json"
)


def get_team_page_html(team: Team) -> str | None:
    api_url = f"{BASE_API_URL}&page={team.team_short_name}"
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Failed to get data for {team.team_name}")
        return None

    return response.json()["parse"]["text"]["*"]
