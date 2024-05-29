"""Draft main.py"""

import time
from random import randint

import pandas as pd
from tqdm import tqdm

from src.utils.get_players_data import GetPlayersAttributes, GetPlayersLinks

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
    player_attr = GetPlayersAttributes(link)
    player_data.append(
        {
            "id": player_id,
            "avg": player_attr.avg_grade,
            "fanta_avg": player_attr.avg_fanta_grade,
        }
    )
    time.sleep(randint(0, 3000) / 1000)
df = pd.DataFrame(player_data)
print(df)
