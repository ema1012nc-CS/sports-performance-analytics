def calculate_ts(player_data):
    # Calculate total points
    total_pts = player_data["PTS"].sum()
    # Calculate total FGA
    total_fga = player_data["FGA"].sum()

    # Calculate total FTA
    total_fta = player_data["FTA"].sum()

    # Calculate the TS% denominator
    denominator = 2 * (total_fga + 0.44 * total_fta)

    # Check for division by zero
    if denominator <= 0:
        return float("nan")

    # Return TS%
    return (total_pts / denominator) * 100

def calculate_per36(player_data, stat):
    total_stat = player_data[stat].sum()
    total_min = player_data["MIN"].sum()

    if total_min > 0:
        return (total_stat / total_min) * 36
    else:
        return float("nan")

def calculate_consistency(player_data, stat):
    # Calculate the standard deviation
    std_dev = player_data[stat].std()
    # Return the result
    return std_dev

def calculate_rolling_average(player_data, stat, window):
    # Select the specified statistic
    stat_series = player_data[stat]
    # Calculate a rolling average using the window parameter
    rolling_avg = stat_series.rolling(window=window).mean()

    # Return the rolling averages
    return rolling_avg