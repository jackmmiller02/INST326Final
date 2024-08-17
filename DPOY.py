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

class AwardPredictor:
    def __init__(self):
        self.dpoy_candidates = []

    def meets_threshold(self, stats, thresholds):
        return (stats.get('REB', 0) >= thresholds['REB'] and
                stats.get('STL', 0) >= thresholds['STL'] and
                stats.get('BLK', 0) >= thresholds['BLK'])

    def calculate_defensive_efficiency(self, stats): 
        eff = (
            stats.get('REB', 0) * 2 +
            stats.get('STL', 0) * 4 +
            stats.get('BLK', 0) * 5 -
            stats.get('Missed FG', 0) * 0.5 -
            stats.get('Missed FT', 0) * 0.5 -
            stats.get('TO', 0))
        return eff

    def filter_candidates(self, players_stats, thresholds):
        for player_name, stats in players_stats.items():
            if self.meets_threshold(stats, thresholds):
                eff = self.calculate_defensive_efficiency(stats)
                print(f"Player {player_name} meets defensive threshold with Efficiency: {eff}")
                self.dpoy_candidates.append((player_name, eff))
        if not self.dpoy_candidates:
            print("No players met the defensive threshold.")

    def predict_dpoy(self, top_n=5):
        self.dpoy_candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = self.dpoy_candidates[:top_n]
        print(f"Found {len(top_candidates)} DPOY candidates.")
        if not top_candidates:
            print("No players are available for DPOY prediction.")
        else:
            for int, (player, eff) in enumerate(top_candidates, start=1):
                likelihood = 1 - (int / len(top_candidates))  
                print(f"{int}. {player} DPOY Likelihood: {likelihood * 100:.2f}% (Defensive Efficiency: {eff})")
fetcher = NBADataFetcher()
fetcher.fetch_all_player_stats()
players_stats = fetcher.get_player_stats()
thresholds = {'REB': 8, 'STL': 0.8, 'BLK': 2}

predictor = AwardPredictor()
predictor.filter_candidates(players_stats, thresholds)
predictor.predict_dpoy(top_n=5)
