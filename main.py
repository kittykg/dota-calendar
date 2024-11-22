import hydra
from omegaconf import DictConfig

from common import Config
from ical_management import *
from liquidpedia_api import get_team_page_html
from parse import parse_match_data


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    config = Config.hydra_config_to_dataclass_config(cfg)
    cal = load_cal_from_path(config.target_cal_path)

    all_matches: list[Match] = []
    for team in config.interested_teams:
        html_data = get_team_page_html(team)
        if html_data is None:
            print(f"Failed to get data for {team}, skipping...")
            continue

        all_matches += parse_match_data(html_data)

    all_matches.sort(key=lambda x: x.start_timestamp)
    add_matches_to_ical(cal, all_matches)
    write_cal_to_path(cal, config.target_cal_path)


if __name__ == "__main__":
    main()
