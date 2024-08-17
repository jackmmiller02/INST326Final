from nba_api.stats.endpoints import leaguedashplayerstats

class NBADataFetcher:
    def __init__(self):
        """
        Initializes data fetcher with an empty dict for player stats.
        """
        self.player_stats = {}

    def fetch_all_player_stats(self):
        """
        Fetches points, rebounds, assists, steals, blocks, missed field goals and missed free throws. Populates the dictionary.
        """
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
        """
        Returns the dictionary of player stats.
        
        Returns:
        dict: Dictionary where keys are player names and values are dictionaries of their stats.
        """
        return self.player_stats

class AwardPredictor:
    def __init__(self):
        """
        Initializes the predictor with an empty list for candidates.
        """
        self.mvp_candidates = []

    def meets_threshold(self, stats, thresholds):
        """
        Checks if the player meets the MVP thresholds for key stats.
        
        Args:
        stats (dict): Dictionary of player stats.
        thresholds (dict): Dictionary of thresholds for points, rebounds, assists, steals, and blocks.

        Returns:
        bool: True if the player meets the thresholds, false otherwise.
        """
        return (stats.get('PTS', 0) >= thresholds['PTS'] and
                stats.get('REB', 0) >= thresholds['REB'] and
                stats.get('AST', 0) >= thresholds['AST'] and
                stats.get('STL', 0) >= thresholds['STL'] and
                stats.get('BLK', 0) >= thresholds['BLK'])

    def calculate_efficiency(self, stats):
        """
        Calculates the efficiency of a player based on their stats.
        
        Args:
        stats (dict): Dictionary player stats.

        Returns:
        float: The calculated efficiency rating.
        """
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

    def filter_candidates(self, players_stats, thresholds):
        """
        Filters players who meet threshold to calculate their efficiency rating.
        
        Args:
        players_stats (dict): Dictionary of players' stats.
        thresholds (dict): Dictionary of thresholds for points, rebounds, assists, steals, and blocks.
        """
        for player_name, stats in players_stats.items():
            if self.meets_threshold(stats, thresholds):
                eff = self.calculate_efficiency(stats)
                print(f"Player {player_name} meets threshold with Efficiency: {eff}")
                self.mvp_candidates.append((player_name, eff))
        if not self.mvp_candidates:
            print("No players met the threshold.")

    def predict_mvp(self, top_n=5):
        """
        Ranks MVP candidates by efficiency and predicts the top N MVP candidates.
        
        Args:
        top_n (int): Number of top candidates to predict. Default is 5.
        """
        self.mvp_candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = self.mvp_candidates[:top_n]
        print(f"Found {len(top_candidates)} MVP candidates.")
        if not top_candidates:
            print("No players are available for MVP prediction.")
        else:
            for int, (player, eff) in enumerate(top_candidates, start=1):
                likelihood = 1 - (int / len(top_candidates)) 
                print(f"{int}. {player} MVP Likelihood: {likelihood * 100:.2f}% (Efficiency: {eff})")

fetcher = NBADataFetcher()
fetcher.fetch_all_player_stats()
players_stats = fetcher.get_player_stats()
thresholds = {
    'PTS': 20, 'REB': 4, 'AST': 4, 'STL': 0.5, 'BLK': 0.1}

predictor = AwardPredictor()
predictor.filter_candidates(players_stats, thresholds)
predictor.predict_mvp(top_n=5)
