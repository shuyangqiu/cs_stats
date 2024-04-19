from typing import List, Any, Dict
from pathlib import Path
import json
import re
import undetected_chromedriver as uc
from selenium.webdriver import Chrome, ChromeOptions
from urllib.parse import urljoin, urlencode
from bs4 import BeautifulSoup
from time import sleep

class Player:
    '''A data structure representing a CS player.
    '''
    path: str
    win = -1
    loss = -1
    kills = -1
    deaths = -1
    headshot = -1
    adr = -1
    rounds = -1

    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"{self.path}, {self.win}, {self.loss}, {self.kills}, {self.deaths}, {self.headshot}, {self.adr}, {self.rounds}"

class HLTVScraper:
    '''A class containing methods to scrape HLTV.org.
    '''
    _config: Dict[str, Any]
    _browser: Chrome

    def __init__(self) -> None:
        # Read config
        config_path = (Path(__file__).parent / "config.json").resolve()
        with open(config_path) as f:
            self._config = json.load(f)

        # Init webdriver
        options = ChromeOptions()
        #options.add_argument("--headless=new")
        self._browser = uc.Chrome(options)

    def __get_html(self, path: str, params: Dict[str, Any] = None) -> str:
        """Returns html at path with params included.
        """
        # Construct url
        url = f"{self._config['BASE']}/{path}"
        if params is not None:
            url = urljoin(url, f"?{urlencode(params)}")

        self._browser.get(url)
        sleep(self._config["DELAY"])
        return self._browser.page_source
        

    def get_events(self, startDate: str, endDate: str, prizePool: int) -> List[str]:
        """Returns a list of event ids within a date range with at least the specified prize pool.
        """
        params = {"startDate": startDate, "endDate": endDate, "prizeMin": prizePool, "prizeMax": 2000000}
        html = self.__get_html(self._config["ARCHIVE"], params)
        soup = BeautifulSoup(html, "html.parser")

        results = soup.find("div", "events-page")
        events = results.find_all("a", href = re.compile("\/events\/\d+\/")) # Find all links with '/events/####'

        eventIds = []
        for event in events:
            eventIds.append(event["href"].split('/')[2])

        return(eventIds)
    
    def get_event_matches(self, eventId: str) -> List[str]:
        """Returns a list of paths to matches in event.
        """
        params = {"event": eventId}
        html = self.__get_html(self._config["RESULTS"], params)
        soup = BeautifulSoup(html, "html.parser")

        results = soup.find("div", "results-all")
        matches = results.find_all("a", href = re.compile("\/matches\/\d+\/")) # Find all links with '/matches/####'

        matchIds = []
        for match in matches:
            matchIds.append(match["href"].split('/', 2)[2])
        return matchIds
    
    def get_players_in_match(self, matchPath: str) -> List[Player]:
        """Returns a list of players in a match with the number of maps won and lost.
        """
        html = self.__get_html(f"{self._config['MATCH']}/{matchPath}")
        soup = BeautifulSoup(html, "html.parser")

        # Get team results
        teams = soup.find_all("div", re.compile("team\d\-gradient")) # Find all divs with class team#-gradient
        teamScore = [int(teams[0].find("div", re.compile("won|lost")).text), int(teams[1].find("div", re.compile("won|lost")).text)]
        if teamScore[0] >= 13 or teamScore[1] >= 13: # Best of 1 match
            if teamScore[0] > teamScore[1]:
                teamScore = [1, 0]
            else:
                teamScore = [0, 1]

        # Get players
        results = []

        playerTables = soup.find("div", {"class": "stats-content", "id": "all-content"}).find_all("table", "table totalstats")
        for i in range(len(playerTables)):
            players = playerTables[i].find_all("a", href = re.compile("\/player\/\d+\/")) # Find all links with '/player/####'
            for player in players:
                p = Player(player["href"].split('/', 2)[2])
                p.win = teamScore[i]
                p.loss = teamScore[(i + 1) % 2]
                results.append(p)

        return results

    def get_players_in_event(self, eventId: str) -> Dict[str, Player]:
        '''Returns a list of players in an event with their win/loss records.
        '''
        matches = self.get_event_matches(eventId)

        players = {}
        for match in matches:
            for p in self.get_players_in_match(match):
                if p.path not in players.keys():
                    players[p.path] = p
                else:
                    players[p.path].win += p.win
                    players[p.path].loss += p.loss

        return players

    def get_player_stats(self, player: Player) -> None:
        '''Scrapes and sets a player's stats.
        '''
        html = self.__get_html(f"{self._config['PLAYER']}/{player.path}")
        soup = BeautifulSoup(html, "html.parser")

        stats = soup.find_all("div", "stats-row")

        player.kills = stats[0].find_all("span")[1].text
        player.headshot = stats[1].find_all("span")[1].text
        player.deaths = stats[2].find_all("span")[1].text
        player.adr = stats[4].find_all("span")[1].text
        player.rounds = stats[7].find_all("span")[1].text


    def close(self) -> None:
        '''Closes the webdriver.
        '''
        self._browser.close()