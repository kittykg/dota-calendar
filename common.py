from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from omegaconf import DictConfig


@dataclass
class Team:
    team_name: str
    team_short_name: str


@dataclass
class Config:
    target_cal_path: Path
    interested_teams: list[Team]

    @staticmethod
    def hydra_config_to_dataclass_config(cfg: DictConfig) -> "Config":
        interested_teams = []
        for t in cfg["interested_teams"]:
            if t not in TEAM_NAME_TO_DATACLASS_TEAM:
                raise ValueError(f"Unknown team name: {t}")
            interested_teams.append(TEAM_NAME_TO_DATACLASS_TEAM[t])

        return Config(
            target_cal_path=Path(cfg["target_cal_path"]),
            interested_teams=interested_teams,
        )


@dataclass
class Match:
    team_1: str
    team_2: str
    start_timestamp: datetime
    tournament: str
    expected_match_length: int = 60 * 2


LIQUIDPEDIA_SHORTCODE_TO_FULL_TEAM_NAME = {
    "TSpirit": "Team Spirit",
}

DATA_CLASS_TEAM_SPIRIT = Team(
    team_name="Team Spirit",
    team_short_name="Team_Spirit",
)

TEAM_NAME_TO_DATACLASS_TEAM = {
    "spirit": DATA_CLASS_TEAM_SPIRIT,
    "team_spirit": DATA_CLASS_TEAM_SPIRIT,
    "team spirit": DATA_CLASS_TEAM_SPIRIT,
    "ts": DATA_CLASS_TEAM_SPIRIT,
    "tspirit": DATA_CLASS_TEAM_SPIRIT,
}
