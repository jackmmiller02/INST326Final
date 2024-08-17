from nba_api.stats.endpoints import leaguedashplayerstats
import sqlite3

class PlayerDB:
    def __init__(self):
        """
        Initializes, connects to SQLite3
        """
        self.conn = sqlite3.connect('nba_players.db')
        self.create_table()

    def create_table(self):
        """
        Creates players database table
        """
        with self.conn:
            self.conn.execute("DROP TABLE IF EXISTS players")
            self.conn.execute('''CREATE TABLE IF NOT EXISTS players 
                                 (name TEXT, ppg REAL, rpg REAL, apg REAL, spg REAL, bpg REAL)''')

    def insert_player(self, name, ppg, rpg, apg, spg, bpg):
        """
        Inserts player stats into database table.
        Args:
            name (str): Player name.
            ppg (float): Points per game.
            rpg (float): Rebounds per game.
            apg (float): Assists per game.
            spg (float): Steals per game.
            bpg (float): Blocks per game. 
        """
        with self.conn:
            self.conn.execute(
                "INSERT INTO players (name, ppg, rpg, apg, spg, bpg) VALUES (?, ?, ?, ?, ?, ?)", 
                (name, ppg, rpg, apg, spg, bpg)
            )

    def get_sorted_by_stat(self, stat):
        """
        Sorts the top 10 in a stat in descending order.

        Args:
        stat(str): The statistic (e.g. ppg, apg, etc.)
        """
        with self.conn:
            return self.conn.execute(f"SELECT name, {stat} FROM players ORDER BY {stat} DESC LIMIT 10").fetchall()

class NBADataFetcher:
    def fetch_all_player_stats(self):
        league_stats = leaguedashplayerstats.LeagueDashPlayerStats(season='2023-24').get_normalized_dict()
        players_data = []
        for player in league_stats['LeagueDashPlayerStats']:
            player_name = player['PLAYER_NAME']
            games_played = player.get('GP', 1)
            ppg = player.get('PTS', 0) / games_played  
            rpg = player.get('REB', 0) / games_played  
            apg = player.get('AST', 0) / games_played  
            spg = player.get('STL', 0) / games_played  
            bpg = player.get('BLK', 0) / games_played  

            players_data.append((player_name, ppg, rpg, apg, spg, bpg))
        return players_data

def display_top_players(stat, top_players):
    """
    Displays the top players in each stat
    """
    print(f"Top 10 players by {stat.upper()}:")
    for player in top_players:
        name, value = player
        print(f"{name}: {value:.2f}")
    print("\n") 

db = PlayerDB()
fetcher = NBADataFetcher()
all_players_stats = fetcher.fetch_all_player_stats()
for player_data in all_players_stats:
    db.insert_player(*player_data)

top_scorers = db.get_sorted_by_stat('ppg')
display_top_players('ppg', top_scorers)
top_rebounders = db.get_sorted_by_stat('rpg')
display_top_players('rpg', top_rebounders)
top_assists = db.get_sorted_by_stat('apg')
display_top_players('apg', top_assists)
top_steals = db.get_sorted_by_stat('spg')
display_top_players('spg', top_steals)
top_blocks = db.get_sorted_by_stat('bpg')
display_top_players('bpg', top_blocks)
