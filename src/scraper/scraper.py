"""Draft main.py"""

import time
from csv import QUOTE_ALL
from random import randint

import pandas as pd
from tqdm import tqdm

from src.scraper.get_historical_values import GetPlayersHistoricalStats
from src.scraper.get_players_links import GetPlayersLinks
from src.scraper.get_players_seasonal_attributes import GetPlayersAttributes

# set up main function and config file

# Get Players links and define a unique ID
players_links = GetPlayersLinks(year="2023-24")
players_links.get_links().add_ids().save_csv()


# Get Players attributes
# FIXME: the path to the csv has to be automatically determined
df_links = pd.read_csv("data/players_links_2023-24.csv")

player_data = []
# FIXME: [:10] is just to test, later it has to be removed
for link, player_id in tqdm(
    zip(df_links.link[:10], df_links.player_id[:10]),
    total=len(df_links.link[:10]),
    desc="Downloading players attributes",
):
    player_attrs = GetPlayersAttributes(link)
    player_data.append(
        {
            "id": player_id,
            "avg_grade": player_attrs.avg_grade,
            "fanta_avg_grade": player_attrs.avg_fanta_grade,
            "role": player_attrs.role,
            "role_mantra": player_attrs.role_mantra,
            "played_matches": player_attrs.played_matches,
            "goals": player_attrs.goals,
            "assists": player_attrs.assists,
            "goals_home_game": player_attrs.goals_home_game,
            "goals_away_game": player_attrs.goals_away_games,
            "penalties_scored": player_attrs.penalties_scored,
            "penalties_shot": player_attrs.penalties_shot,
            "penalties_ratio": player_attrs.penalties_ratio,
            "autogoals": player_attrs.autogoals,
            "yellow_cards": player_attrs.yellow_cards,
            "red_cards": player_attrs.red_cards,
            "team": player_attrs.team,
        }
    )
    time.sleep(randint(0, 300) / 100)
df = pd.DataFrame(player_data)
df.to_csv(
    "data/provola_attributes.csv",
    index=False,
    quotechar='"',
    quoting=QUOTE_ALL,
)


# Get players descriptions
# FIXME: split descriptions in a different class
# otherwise all the class is initiazlized, and uselessly scraps two times all data
# FIXME: [:10] is just to test, later it has to be removed
player_data = []
for link, player_id in tqdm(
    zip(df_links.link[:10], df_links.player_id[:10]),
    total=len(df_links.link[:10]),
    desc="Downloading players descriptions",
):
    player_attrs = GetPlayersAttributes(link)
    player_data.append(
        {
            "id": player_id,
            "description": player_attrs.description,
            "fanta_description": player_attrs.fanta_description,
        }
    )
    time.sleep(randint(0, 300) / 100)
df = pd.DataFrame(player_data)
df.to_csv(
    "data/provola_descriptions.csv",
    index=False,
    quotechar='"',
    quoting=QUOTE_ALL,
)


# Get players historical variables
# FIXME: [:10] is just to test, later it has to be removed
player_data = []
for link, player_id in tqdm(
    zip(df_links.link[:10], df_links.player_id[:10]),
    total=len(df_links.link[:10]),
    desc="Downloading players historical values",
):
    player_attrs = GetPlayersHistoricalStats(player_link=link, year="2023-24")
    player_data.append(
        {
            "id": player_id,
            "game_day": player_attrs.game_day,
            "grade": player_attrs.grade,
            "fanta_grade": player_attrs.fanta_grade,
            "bonus": player_attrs.bonus,
            "malus": player_attrs.malus,
            "home_team": player_attrs.home_team,
            "match_score": player_attrs.match_score,
            "away_team": player_attrs.away_team,
            "minute_in": player_attrs.minute_in,
            "minute_out": player_attrs.minute_out,
        }
    )
    time.sleep(randint(0, 300) / 100)
df = pd.DataFrame(player_data)
df.to_csv(
    "data/provola_historical.csv",
    index=False,
    quotechar='"',
    quoting=QUOTE_ALL,
)
