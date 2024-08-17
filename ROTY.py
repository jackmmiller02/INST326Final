import requests
from bs4 import BeautifulSoup
from nba_api.stats.endpoints import leaguedashplayerstats

class NBADataFetcher:
    def __init__(self):
        self.player_stats = {}

    def fetch_all_player_stats(self):
        league_stats = leaguedashplayerstats.LeagueDashPlayerStats(season='2023-24').get_normalized_dict()
        for player in league_stats['LeagueDashPlayerStats']:
            player_name = player['PLAYER_NAME']
            self.player_stats[player_name] = {
                'PTS': player.get('PTS', 0),
                'REB': player.get('REB', 0),
                'AST': player.get('AST', 0),
                'STL': player.get('STL', 0),
                'BLK': player.get('BLK', 0),
                'Missed FG': player.get('FGA', 0) - player.get('FGM', 0),
                'Missed FT': player.get('FTA', 0) - player.get('FTM', 0),
                'TO': player.get('TOV', 0)}

    def get_player_stats(self):
        return self.player_stats

class RookieScraper: #scraping rookies from html, no rookie categorization in the api
    def __init__(self, url):
        """
        Initializes scraping with URL

        Args:
        url(str): URL to Basketball Reference rookie page.
        """
        self.url = url
        self.rookie_names = []

    def scrape_rookie_names(self):
        """
        Scrapes rookie names from the season using the Basketball Reference website rookies list.
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'sortable stats_table'})
        for row in table.find_all('tr')[1:]: 
            player_cell = row.find('td', {'data-stat': 'player'})
            if player_cell:
                name = player_cell.get_text(strip=True)
                self.rookie_names.append(name)

    def get_rookie_names(self): 
        """
        Returns: Rookie names scraped from Basketball Reference
        """
        return self.rookie_names

class AwardPredictor:
    def __init__(self):
        self.roty_candidates = []

    def meets_threshold(self, stats, thresholds):
        return (stats.get('PTS', 0) >= thresholds['PTS'] and
                stats.get('REB', 0) >= thresholds['REB'] and
                stats.get('AST', 0) >= thresholds['AST'] and
                stats.get('STL', 0) >= thresholds['STL'] and
                stats.get('BLK', 0) >= thresholds['BLK'])

    def calculate_efficiency(self, stats):
        eff = (
            stats.get('PTS', 0) * 1.5 +
            stats.get('REB', 0) +
            stats.get('AST', 0) * 1.5 +
            stats.get('STL', 0) * 2 +
            stats.get('BLK', 0) * 2 -
            stats.get('Missed FG', 0) -
            stats.get('Missed FT', 0) -
            stats.get('TO', 0))
        return eff

    def filter_candidates(self, players_stats, rookie_names, thresholds):
        for player_name, stats in players_stats.items():
            if player_name in rookie_names and self.meets_threshold(stats, thresholds):
                eff = self.calculate_efficiency(stats)
                print(f"Rookie {player_name} meets threshold with Efficiency: {eff}")
                self.roty_candidates.append((player_name, eff))
        if not self.roty_candidates:
            print("No rookies met the threshold.")

    def predict_roty(self, top_n=5):
        self.roty_candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = self.roty_candidates[:top_n]
        print(f"Found {len(top_candidates)} ROTY candidates.")
        if not top_candidates:
            print("No rookies available for ROTY prediction.")
        else:
            for int, (player, eff) in enumerate(top_candidates, start=1):
                likelihood = 1 - (int / len(top_candidates))
                print(f"{int}. {player} ROTY Likelihood: {likelihood * 100:.2f}% (Efficiency: {eff})")

rookie_scraper = RookieScraper("https://www.basketball-reference.com/leagues/NBA_2024_rookies.html")
rookie_scraper.scrape_rookie_names()
rookie_names = rookie_scraper.get_rookie_names()
fetcher = NBADataFetcher()
fetcher.fetch_all_player_stats()
players_stats = fetcher.get_player_stats()
roty_thresholds = {
    'PTS': 6, 'REB': 0.5, 'AST': 0.5, 'STL': 0.2, 'BLK': 0.2}

predictor = AwardPredictor()
predictor.filter_candidates(players_stats, rookie_names, roty_thresholds)
predictor.predict_roty(top_n=5)
