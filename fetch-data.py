
import pandas as pd
from nba_api.stats.endpoints import playergamelogs
from pathlib import Path

# Request all player game logs for the 2025-26 season
response = playergamelogs.PlayerGameLogs(
    season_nullable="2025-26",
    season_type_nullable="Regular Season"
)

# Convert the API response into a Pandas DataFrame
df = response.get_data_frames()[0]

# Inspect our data
print(df.head())
print("Number of records:", len(df))
print("Columns:", df.columns.tolist())

# Save the data locally
Path("data").mkdir(exist_ok=True)
df.to_csv("data/nba_2025_26.csv", index=False)
