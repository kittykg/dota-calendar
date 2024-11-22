from datetime import datetime, timedelta
from pathlib import Path

from icalendar import Calendar, Component, Event

from common import Match

DEFAULT_EVENT_LENGTH_HR = 1


def match_to_ical_event(match: Match) -> Event:
    """
    Convert a match to an ical event.

    Args:
        match: The match to convert.

    Returns:
        The ical event.
    """
    event = Event()
    event.add("SUMMARY", f"{match.team_1} vs {match.team_2}")
    event.add("DTSTART", match.start_timestamp)
    event.add(
        "DTEND",
        match.start_timestamp + timedelta(hours=DEFAULT_EVENT_LENGTH_HR),
    )
    event.add("LOCATION", match.tournament)

    return event


def add_matches_to_ical(cal: Component, matches: list[Match]):
    """
    Append matches to the ical file.

    Assume the matches is sorted by start_timestamp. If the last event in the
    calendar `cal` ends after the first match in `matches` starts, then no
    writing is done.

    Args:
        cal: The calendar to write to.
        matches: The matches to write.
    """
    last_event = cal.walk("VEVENT")[-1]
    last_event_end: datetime = last_event.get("DTEND").dt

    if last_event_end > matches[0].start_timestamp:
        print(f"Last event ends after the first match starts, skipping...")
        return

    for match in matches:
        event = match_to_ical_event(match)
        cal.add_component(event)
    print(f"Added {len(matches)} matches to the calendar.")


def load_cal_from_path(cal_path: Path) -> Component:
    """
    Load a calendar from a path.

    Args:
        cal_path: Path to the calendar file.

    Returns:
        The calendar component.
    """
    with open(cal_path, "r") as f:
        cal = Calendar.from_ical(f.read())
    return cal


def write_cal_to_path(cal: Component, cal_path: Path):
    """
    Write a calendar to a path.

    Args:
        cal: The calendar to write.
        cal_path: Path to write the calendar to.
    """
    with open(cal_path, "wb") as f:
        f.write(cal.to_ical())
