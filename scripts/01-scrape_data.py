#### Preamble ####
# Purpose: Scrapes Counter-Strike player statistics from HLTV.org
# Author: Shuyang Qiu
# Date: 17 April 2024
# Contact: shuyang.qiu@mail.utoronto.ca
# License: MIT
# Pre-requisites: Requires BeautifulSoup and undetected_chromedriver Python libraries.

from hltv_scraper.hltv_scaper import HLTVScraper

scraper = HLTVScraper()

events = scraper.get_events("2023-10-16", "2024-04-17", 100000)
players = {}
for event in events:
    for p in scraper.get_players_in_event(event).values():
            if p.path not in players.keys():
                players[p.path] = p
            else:
                players[p.path].win += p.win
                players[p.path].loss += p.loss

for player in players.values():
    scraper.get_player_stats(player)

with open("../data/raw_data/raw_data.csv", "a") as f:
    f.seek(0)
    f.truncate()
    for player in players.values():
        f.write(f"{str(player)}\n")


scraper.close()