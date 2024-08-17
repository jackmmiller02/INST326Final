from MVP import NBADataFetcher as MVPFetcher, AwardPredictor as MVPPredictor
from DPOY import NBADataFetcher as DPOYFetcher, AwardPredictor as DPOYPredictor

def test_mvp_efficiency(): #test for mvp
    mvp_fetcher = MVPFetcher()
    mvp_fetcher.fetch_all_player_stats()
    mvp_player_stats = mvp_fetcher.get_player_stats()
    mvp_thresholds = {'PTS': 20, 'REB': 4, 'AST': 4, 'STL': 0.5, 'BLK': 0.1}
    mvp_predictor = MVPPredictor()
    mvp_predictor.filter_candidates(mvp_player_stats, mvp_thresholds)
    mvp_predictor.predict_mvp(top_n=5)

    assert mvp_predictor.mvp_candidates[0][0] == "Nikola Jokic", "First player: Nikola Jokic" #assert first place for MVP based on eff rating
    assert abs(mvp_predictor.mvp_candidates[0][1] - 4611.5) < 0.1, "Efficiency for Nikola Jokic: 4611.5"
    
    assert mvp_predictor.mvp_candidates[1][0] == "Luka Doncic", "Second player: Luka Doncic"
    assert abs(mvp_predictor.mvp_candidates[1][1] - 4245.0) < 0.1, "Efficiency for Luka Doncic: 4245.0"
    
    assert mvp_predictor.mvp_candidates[2][0] == "Giannis Antetokounmpo", "Third place: Giannis Antetokounmpo"
    assert abs(mvp_predictor.mvp_candidates[2][1] - 4170.0) < 0.1, "Efficiency for Giannis Antetokounmpo: 4170.0"
    
    assert mvp_predictor.mvp_candidates[3][0] == "Shai Gilgeous-Alexander", "Fourth place: Shai Gilgeous-Alexander"
    assert abs(mvp_predictor.mvp_candidates[3][1] - 3992.5) < 0.1, "Efficiency for Shai Gilgeous-Alexander: 3992.5"
    
    assert mvp_predictor.mvp_candidates[4][0] == "Domantas Sabonis", "Fifth place: Domantas Sabonis"
    assert abs(mvp_predictor.mvp_candidates[4][1] - 3934.0) < 0.1, "Efficiency for Domantas Sabonis: 3934.0"

def test_dpoy_efficiency(): #test for dpoy
    dpoy_fetcher = DPOYFetcher()
    dpoy_fetcher.fetch_all_player_stats()
    dpoy_player_stats = dpoy_fetcher.get_player_stats()
    dpoy_thresholds = {'REB': 8, 'STL': 0.8, 'BLK': 2}
    dpoy_predictor = DPOYPredictor()
    dpoy_predictor.filter_candidates(dpoy_player_stats, dpoy_thresholds)
    dpoy_predictor.predict_dpoy(top_n=5)

    assert dpoy_predictor.dpoy_candidates[0][0] == "Rudy Gobert", "First place: Rudy Gobert" #assert first place for DPOY
    assert abs(dpoy_predictor.dpoy_candidates[0][1] - 2689.5) < 0.1, "Efficiency for Rudy Gobert: 2689.5"
    
    assert dpoy_predictor.dpoy_candidates[1][0] == "Anthony Davis", "Second place: Anthony Davis"
    assert abs(dpoy_predictor.dpoy_candidates[1][1] - 2684.5) < 0.1, "Efficiency for Anthony Davis: 2684.5"
    
    assert dpoy_predictor.dpoy_candidates[2][0] == "Victor Wembanyama", "Third place: Victor Wembanyama"
    assert abs(dpoy_predictor.dpoy_candidates[2][1] - 2517.0) < 0.1, "Efficiency for Victor Wembanyama: 2517.0"
    
    assert dpoy_predictor.dpoy_candidates[3][0] == "Domantas Sabonis", "Fourth place: Domantas Sabonis"
    assert abs(dpoy_predictor.dpoy_candidates[3][1] - 2225.5) < 0.1, "Efficiency for Domantas Sabonis: 2225.5"
    
    assert dpoy_predictor.dpoy_candidates[4][0] == "Nikola Jokic", "Fifth place: Nikola Jokic"
    assert abs(dpoy_predictor.dpoy_candidates[4][1] - 2152.5) < 0.1, "Efficiency for Nikola Jokic: 2152.5"

if __name__ == "__main__":
    test_mvp_efficiency()
    test_dpoy_efficiency()
    print("Test passed, player efficiency ratings are correct.")
