import unit_laliga

leagues = ["La Liga", "Premier League", "Serie A"]


def load_teams_name():
    teams_names = []
    for data in unit_laliga.table_data:
        teams_names.append(data[0])
    teams_names.sort()
    return teams_names


def print_teams_name(teams_names):
    i = 1
    for team in teams_names:
        print(f"{i}. {team}")
        i += 1


def get_user_choose():
    team = int(input("your choose: ")) - 1
    if team < 0 or team > 19:
        print(f"Wrong input! \n Please try again...")
        team = get_user_choose()
    return team


def choose_league():
    """print the league options and get the user choose"""
    print("Please select the league (1-4): \n")
    i = 1
    for option in leagues:
        print(f"{i}. {option}\n")
        i += 1
    choose = int(input("your choose: "))
    while choose < 1 or choose > 3:
        choose = int(input("wrong input! \nplease choose again(1-4): "))
    league = leagues[choose - 1]
    return league


def menu(league):
    """menu for user:
    the user has to choose two different team, first home team and secent away team,
    return the names of the teams that user choose"""

    home_team, away_team = 0, 0
    while home_team == away_team:
        print(f"{league} teams: ")
        teams_names = load_teams_name()
        print_teams_name(teams_names)
        print(f"Please choose the home team: ")
        home_team = get_user_choose()
        print(f"Please choose the away team: ")
        away_team = get_user_choose()
        if home_team == away_team:
            print("Error! You have to choose different teams! \nPlease try again...")
    home_team = teams_names[home_team]
    away_team = teams_names[away_team]
    return home_team, away_team


if __name__ == '__main__':
    """main:
    call to choose league,
    load league data, 
    call to load data from url,
    call to menu function and get the names of the teams that user choose
    call to function from unit_laliga to start predict the win chances"""
    league = choose_league()
    unit_laliga.league_data(league)
    url = {"La Liga": "https://www.skysports.com/la-liga-table",
           "Premier League": "https://www.skysports.com/premier-league-table",
           "Serie A": "https://www.skysports.com/serie-a-table"}
    unit_laliga.load_data_from_website(url[league])
    home_team, away_team = menu(league)
    unit_laliga.select_teams(home_team, away_team)
