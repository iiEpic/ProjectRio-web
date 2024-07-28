
def calculate_era(earned_runs, innings_pitched, game_innings=3):
    """
    :param earned_runs: Integer, Runs allowed
    :param innings_pitched: Integer, This could be a whole number (2) or decimal (2.6) to signify 2 2/3 innings (2 outs)
    :param game_innings: Integer, by default this is set to (3) but can be changed if needed
    :return: Decimal, 1, 1.40, etc
    """
    return round((earned_runs / innings_pitched) * game_innings, 2)

