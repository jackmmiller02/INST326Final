from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import re

class NBADataFetcher:
    def validate_player_name(self, player_name):
        """Uses regex to validate player names and characters."""
        if not re.match(r"^[a-zA-Z\s\-.]+$", player_name):
            raise ValueError(f"Invalid player name: {player_name}. Only letters, spaces, hyphens, and periods are allowed.")
    
    def get_player_id(self, player_name):
        self.validate_player_name(player_name)
        nba_players = players.get_players()
        player = next((player for player in nba_players if player['full_name'].lower() == player_name.lower()), None)
        if player:
            return player['id']
        else:
            raise ValueError(f"Player {player_name} not found.")

    def get_player_stats(self, player_name):
        player_id = self.get_player_id(player_name)
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        stats = career_stats.get_data_frames()[0]
        return stats


fetcher = NBADataFetcher()
ae_stats = fetcher.get_player_stats("Anthony Edwards") #Anthony Edwards stats as example
print(ae_stats)
