import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import (
    calculate_ts,
    calculate_per36,
    calculate_consistency,
    calculate_rolling_average
)

# Configure the webpage
st.set_page_config(
    page_title="NBA Player Analytics",
    layout="wide"
)

# Display the title
st.title("NBA Player Analytics Dashboard")

# Load our NBA dataset
df = pd.read_csv("data/nba_2025_26.csv")

# Convert dates to datetime objects
df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])


# Get a list of available players
players = sorted(df["PLAYER_NAME"].dropna().unique())

# Create a dropdown menu
selected_player = st.selectbox(
    "Select an NBA Player",
    players
)

# Filter statistics for the selected player
player_data = df[
    df["PLAYER_NAME"] == selected_player
]

ppg = player_data["PTS"].mean()
reb = player_data["REB"].mean()
ast = player_data["AST"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Points Per Game", f"{ppg:.1f}")
with col2:
    st.metric("Rebounds Per Game", f"{reb:.1f}")
with col3:
    st.metric("Assists Per Game", f"{ast:.1f}")

player_data = player_data.sort_values(
    by="GAME_DATE"
).copy()

stat_options = {
    "Points": "PTS",
    "Rebounds": "REB",
    "Assists": "AST"
}

selected_stat = st.selectbox(
    "Select a Statistic",
    list(stat_options.keys())
)

stat_column = stat_options[selected_stat]

player_data["LAST_5"] = calculate_rolling_average(
    player_data, stat_column, 5
)

player_data["LAST_10"] = calculate_rolling_average(
    player_data, stat_column, 10
)

fig = px.line(
    player_data,
    x="GAME_DATE",
    y=[stat_column, "LAST_5", "LAST_10"],
    title=f"{selected_player} {selected_stat} Performance",
    labels={
        "GAME_DATE": "Game Date",
        "value": selected_stat,
        "variable": "Statistic"
    }
)

st.plotly_chart(fig, use_container_width=True)

# Display the player's game statistics
st.subheader(f"{selected_player} Game Statistics")

st.dataframe(
    player_data[
        ["GAME_DATE", "PTS", "REB", "AST"]
    ].sort_values("GAME_DATE", ascending=False),
    hide_index=True
)


st.subheader("Player Comparison")

col1, col2 = st.columns(2)

with col1:
    compare_player1 = st.selectbox(
        "Select Player 1",
        players
    )

with col2:
    compare_player2 = st.selectbox(
        "Select Player 2",
        players,
        index=1
    )

# Filter statistics for the selected player
player_data1 = df[
    df["PLAYER_NAME"] == compare_player1
]

# Filter statistics for the selected player
player_data2 = df[
    df["PLAYER_NAME"] == compare_player2
]

if compare_player1 == compare_player2:
    st.warning("Please select two different players.")
    st.stop()

player1_ppg = player_data1["PTS"].mean()
player1_reb = player_data1["REB"].mean()
player1_ast = player_data1["AST"].mean()
player1_std = calculate_consistency(player_data1, "PTS")

player1_total_pts = player_data1["PTS"].sum()

player2_ppg = player_data2["PTS"].mean()
player2_reb = player_data2["REB"].mean()
player2_ast = player_data2["AST"].mean()
player2_std = calculate_consistency(player_data2, "PTS")

player2_total_pts = player_data2["PTS"].sum()

player1_total_min = player_data1["MIN"].sum()
player2_total_min = player_data2["MIN"].sum()

player1_total_reb = player_data1["REB"].sum()
player2_total_reb = player_data2["REB"].sum()

player1_total_ast = player_data1["AST"].sum()
player2_total_ast = player_data2["AST"].sum()

player1_mpg = player_data1["MIN"].mean()
player2_mpg = player_data2["MIN"].mean()


# Player 1 Per-36 statistics
player1_pts36 = calculate_per36(player_data1, "PTS")
player1_reb36 = calculate_per36(player_data1, "REB")
player1_ast36 = calculate_per36(player_data1, "AST")

# Player 2 Per-36 statistics
player2_pts36 = calculate_per36(player_data2, "PTS")
player2_reb36 = calculate_per36(player_data2, "REB")
player2_ast36 = calculate_per36(player_data2, "AST")


player1_TS = calculate_ts(player_data1)
player2_TS = calculate_ts(player_data2)

with col1:
    st.metric(f"{compare_player1} PPG", f"{player1_ppg:.1f}")
    st.metric(f"{compare_player1} RPG", f"{player1_reb:.1f}")
    st.metric(f"{compare_player1} APG", f"{player1_ast:.1f}")
    if pd.isna(player1_TS):
        st.metric("True Shooting %", "N/A")
    else:
        st.metric("True Shooting %", f"{player1_TS:.1f}%")
with col2:
    st.metric(f"{compare_player2} PPG", f"{player2_ppg:.1f}")
    st.metric(f"{compare_player2} RPG", f"{player2_reb:.1f}")
    st.metric(f"{compare_player2} APG", f"{player2_ast:.1f}")
    if pd.isna(player2_TS):
        st.metric("True Shooting %", "N/A")
    else:
        st.metric("True Shooting %", f"{player2_TS:.1f}%")

comparison_data = pd.DataFrame({
    "Player": [compare_player1, compare_player2],
    "PPG": [player1_ppg, player2_ppg],
    "RPG": [player1_reb, player2_reb],
    "APG": [player1_ast, player2_ast],
    "TS%": [player1_TS, player2_TS],
    "PTS/36": [player1_pts36, player2_pts36],
    "REB/36": [player1_reb36, player2_reb36],
    "AST/36": [player1_ast36, player2_ast36],
    "PTS STD": [player1_std, player2_std]
})

if (player1_ppg - player2_ppg) > 7.5 and (player1_mpg - player2_mpg) > 5:
    st.warning(
        f"{compare_player1} averages substantially more points "
        f"than {compare_player2}. "
        f"{compare_player1} has played substantially more minutes per game than {compare_player2}. "
        "Consider differences in playing time and offensive roles "
        "when interpreting their statistics."
    )
elif (player2_ppg - player1_ppg) > 7.5 and (player2_mpg - player1_mpg) > 5:
    st.warning(
        f"{compare_player2} averages substantially more points "
        f"than {compare_player1}. "
        f"{compare_player2} has played substantially more minutes per game than {compare_player1}. "
        "Consider differences in playing time and offensive roles "
        "when interpreting their statistics."
    )

comparison_stat = st.selectbox(
    "Select a Comparison Statistic",
    ["PPG", "RPG", "APG", "TS%", "PTS/36", "REB/36", "AST/36", "PTS STD"]
)

fig = px.bar(
    comparison_data,
    x= "Player", 
    y= comparison_stat,
    title=f"{comparison_stat} Comparison"
)

st.plotly_chart(fig, use_container_width=True)


for stat in [
    "PPG", "RPG", "APG", "TS%",
    "PTS/36", "REB/36", "AST/36", "PTS STD"
]:
    player1_value = comparison_data.loc[0, stat]
    player2_value = comparison_data.loc[1, stat]

    # Check for missing data
    if pd.isna(player1_value) or pd.isna(player2_value):
        st.info(f"{stat} comparison unavailable: missing data.")
        continue

    difference = abs(player1_value - player2_value)

    # Special logic for scoring consistency
    if stat == "PTS STD":
        if player1_value > player2_value:
            st.info(
                f"{compare_player2} has more consistent scoring "
                f"than {compare_player1}."
            )
        elif player1_value < player2_value:
            st.info(
                f"{compare_player1} has more consistent scoring "
                f"than {compare_player2}."
            )
        else:
            st.info("Both players have the same scoring variability.")

        continue

    # General statistical comparisons
    unit = " percentage points" if stat == "TS%" else ""

    if player1_value > player2_value:
        st.info(
            f"{compare_player1} leads in {stat} "
            f"by {difference:.1f}{unit}."
        )
    elif player1_value < player2_value:
        st.info(
            f"{compare_player2} leads in {stat} "
            f"by {difference:.1f}{unit}."
        )
    else:
        st.info(f"Both players have the same {stat}.")

