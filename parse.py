from datetime import datetime

from bs4 import BeautifulSoup
import tzlocal

from common import Match, LIQUIDPEDIA_SHORTCODE_TO_FULL_TEAM_NAME


def parse_match_data(html_data) -> list[Match]:
    matches: list[Match] = []
    soup = BeautifulSoup(html_data, "html.parser")

    for tag in soup.find_all(
        "table", class_="wikitable wikitable-striped infobox_matches_content"
    ):
        # If the tag does not contain "Upcoming Matches", skip it
        if "Upcoming Matches" not in tag.parent.text:
            continue

        # Get teams
        teams = []
        for tt in tag.find_all("span", class_="team-template-text"):
            if tt.text in LIQUIDPEDIA_SHORTCODE_TO_FULL_TEAM_NAME:
                teams.append(LIQUIDPEDIA_SHORTCODE_TO_FULL_TEAM_NAME[tt.text])
            else:
                teams.append(tt.text)
        assert len(teams) == 2

        # Get time
        for tt in tag.find_all("span", class_="timer-object"):
            start_time = datetime.fromtimestamp(
                int(tt["data-timestamp"])
            ).replace(
                tzinfo=tzlocal.get_localzone(),
            )

        # Get tournament
        for tt in tag.find_all("div", class_="tournament-text-flex"):
            tournament = tt.text

        matches.append(Match(teams[0], teams[1], start_time, tournament))

    return matches
