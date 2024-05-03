import pytest

import pandas as pd

from usports_basketball import usports_team_stats, usports_player_stats

def test_usports_team_stats_returns_dataframe():
    team_stats_df = usports_team_stats('men')
    assert isinstance(team_stats_df, pd.DataFrame)

def test_usports_player_stats_returns_dataframe():
    player_stats_df = usports_player_stats('women')
    assert isinstance(player_stats_df, pd.DataFrame)

def test_usports_team_stats_non_empty():
    team_stats_df = usports_team_stats('women')
    assert not team_stats_df.empty, "Team statistics DataFrame is empty"

def test_usports_player_stats_non_empty():
    player_stats_df = usports_player_stats('men')
    assert not player_stats_df.empty, "Player statistics DataFrame is empty"

def test_usports_team_stats_columns():
    team_stats_df = usports_team_stats('men')
    expected_columns = [
        'team_name',
        'games_played',
        # Add more expected columns as needed
    ]
    assert all(column in team_stats_df.columns for column in expected_columns), "Missing columns in team statistics DataFrame"

def test_usports_player_stats_columns():
    player_stats_df = usports_player_stats('men')
    expected_columns = [
        'lastname_initials',
        'first_name',
        # Add more expected columns as needed
    ]
    assert all(column in player_stats_df.columns for column in expected_columns), "Missing columns in player statistics DataFrame"

