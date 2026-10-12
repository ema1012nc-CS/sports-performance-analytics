import pandas as pd

# Read the CSV file
df = pd.read_csv("data/nba_2025_26.csv")

# Display the first five rows
print(df.head())

# Display the column names
print(df.columns.tolist())

player_stats = df.groupby(
    ["PLAYER_ID", "PLAYER_NAME"]
).agg(
    GP=("GAME_ID", "nunique"),
    PPG=("PTS", "mean"),
    RPG=("REB", "mean"),
    APG=("AST", "mean"),
    TOTAL_POINTS = ("PTS", "sum"),
    TOTAL_FGA = ("FGA", "sum"),
    TOTAL_FTA = ("FTA", "sum")
).reset_index()

# Require at least 20 games played
player_stats = player_stats[player_stats["GP"] >= 20]

player_stats = player_stats[player_stats["TOTAL_FGA"] >= 300]

denominator = 2 * (
    player_stats["TOTAL_FGA"] + 0.44 * player_stats["TOTAL_FTA"]
)

player_stats["TS%"] = (
    player_stats["TOTAL_POINTS"] / denominator.where(denominator != 0) * 100
)




# Sort by highest PPG
# player_stats = player_stats.sort_values(
#     by="PPG",
#     ascending=False
# )

# Sort by highest TS%
player_stats = player_stats.sort_values(
    by="TS%",
    ascending=False
)

# Round averages to one decimal
player_stats = player_stats.round(1)

print(
    player_stats[
        ["PLAYER_NAME", "GP", "PPG", "RPG", "APG", "TS%"]
    ].head(10).to_string(index=False)
)

# Save our calculated statistics
player_stats.to_csv(
    "data/player_stats.csv",
    index=False
)

print(df["MIN"].head(10))