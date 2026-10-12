import pandas as pd
import plotly.express as px

df = pd.read_csv("data/nba_2025_26.csv")

df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])

df = df.sort_values(
    by=["PLAYER_ID", "GAME_DATE"]
)

df["PPG_LAST_5"] = (
    df.groupby("PLAYER_ID")["PTS"]
    .transform(lambda games: games.rolling(5, min_periods=5).mean())
)
#Takes PPG for the last 10 games a player played and calculates the average. If a player has played less than 10 games, it will return NaN for those games.
df["PPG_LAST_10"] = (
    df.groupby("PLAYER_ID")["PTS"]
    .transform(lambda games: games.rolling(10, min_periods=10).mean())
)

df["SEASON_PPG"] = (
    df.groupby("PLAYER_ID")["PTS"]
    .transform("mean")
)

df["PPG_DIFF_5"] = df["PPG_LAST_5"] - df["SEASON_PPG"]
df["PPG_DIFF_10"] = df["PPG_LAST_10"] - df["SEASON_PPG"]

# df["RECENT_PERFORMANCE"] = (
#     df.groupby("PLAYER_ID").tail(1)["PPG_DIFF_5"]
#     .sort_values(ascending=False)
# )

recent_performance = (
    df.groupby("PLAYER_ID")
    .tail(1)
    .dropna(subset=["PPG_DIFF_5"])
    .sort_values(by="PPG_DIFF_5", ascending=False)
    .head(10)
)

print(
    recent_performance[
        ["PLAYER_NAME", "SEASON_PPG", "PPG_LAST_5", "PPG_DIFF_5"]
    ].round(1).to_string(index=False)
)

declining_performance = (
    df.groupby("PLAYER_ID")
    .tail(1)
    .dropna(subset=["PPG_DIFF_5"])
    .sort_values(by="PPG_DIFF_5", ascending=True)
    .head(10)
)

print(
    declining_performance[
        ["PLAYER_NAME", "SEASON_PPG", "PPG_LAST_5", "PPG_DIFF_5"]
    ].round(1).to_string(index=False)
)

# player_data = df[df["PLAYER_NAME"] == "Stephen Curry"]

# fig = px.line(
#     player_data,
#     x="GAME_DATE",
#     y=["PTS", "PPG_LAST_5", "PPG_LAST_10"],
#     title="Stephen Curry Scoring Performance",
#     labels={
#         "GAME_DATE": "Game Date",
#         "value": "Points",
#         "variable": "Statistic"
#     }
# )

# fig.show()

player_input = (input("Enter a player's name: ")).strip()
input_data = df[df["PLAYER_NAME"].str.lower() == player_input.lower()]

if input_data.empty:
    print("No data found for player:", player_input)
else:
    fig = px.line(
    input_data,
    x="GAME_DATE",
    y=["PTS", "PPG_LAST_5", "PPG_LAST_10"],
    title=player_input + " Scoring Performance",
    labels={
        "GAME_DATE": "Game Date",
        "value": "Points",
        "variable": "Statistic"
    }
)
    fig.show()

